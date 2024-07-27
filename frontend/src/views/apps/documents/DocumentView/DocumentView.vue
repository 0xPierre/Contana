<script setup lang="ts">
import BackButton from '@/components/back-button/BackButton.vue'
import { onMounted, ref } from 'vue'
import { notify, swalAlert } from '@/helpers/notify.ts'
import { useDocumentsStore } from '@/stores/apps/Documents.ts'
import { useRoute, useRouter } from 'vue-router'
import { DocumentModel, DocumentsState } from '@/types/documents.types.ts'
import { DocumentStateBadgeInfo } from '@/helpers/documents.ts'
import DocumentStateBadge from '@/components/document-stage-badge/DocumentStateBadge.vue'
import { strftimeFR } from '@/helpers/utils.ts'
import { DocumentsType } from '@/types/core.types.ts'
import ProduceAcompte from '@/views/apps/documents/DocumentView/ProduceAcompte.vue'

const isLoading = ref(false)
const documentStore = useDocumentsStore()
const route = useRoute()
const router = useRouter()

const document = ref<DocumentModel | null>(null)

onMounted(async () => {
  isLoading.value = true

  try {
    const { data } = await documentStore.getDocument(
      route.params.documentId as number
    )
    document.value = data.data
  } catch {
    notify('Une erreur est survenue', 'danger')
    router.push({ name: 'entreprise-documents' })
  }

  isLoading.value = false
})

const deleteDocument = async () => {
  const { value } = await swalAlert(
    'Êtes-vous sûr de vouloir supprimer ce document ?'
  )
  if (!value) return

  isLoading.value = true

  try {
    await documentStore.deleteDocument(route.params.documentId as number)

    router.push({ name: 'entreprise-documents' })
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}

const duplicateDocument = async () => {
  isLoading.value = true

  try {
    const {
      data: { data }
    } = await documentStore.duplicateDocument(
      route.params.documentId as number
    )

    router.push({
      name: 'entreprise-constructor-draft',
      params: { documentId: data.id, documentNumber: data.document_number }
    })
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}

const changeDocumentState = async (state: DocumentsState) => {
  isLoading.value = true

  try {
    await documentStore.changeDocumentState(
      route.params.documentId as number,
      state
    )

    document.value!.state = state
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}

const produceFacture = async () => {
  const { value } = await swalAlert(
    'Êtes-vous sûr de vouloir produire une facture à partir de ce devis ?'
  )
  if (!value) return
  isLoading.value = true

  try {
    const { data } = await documentStore.produceFactureFromDevis(
      route.params.documentId as number
    )
    if (data.status === 'success') {
      router.push({
        name: 'entreprise-document-view',
        params: {
          documentId: data.data.document_id,
          documentNumber: data.data.document_number
        }
      })
    } else {
      notify(data.error, 'danger')
    }
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}

// Not working for now
const printDocument = () => {
  window.frames['documentPdfView'].focus()
  window.frames['documentPdfView'].print()
}
</script>

<template>
  <b-overlay :show="isLoading">
    <b-row v-if="document">
      <b-col md="8" style="min-height: 85vh">
        <!--          :src="`${document.file}#toolbar=0&navpanes=0&scrollbar=1`"-->
        <iframe
          v-if="document.file"
          :src="`${document.file}#navpanes=0&scrollbar=1`"
          width="100%"
          height="100%"
          name="documentPdfView"
        />
      </b-col>
      <b-col md="4">
        <vue-perfect-scrollbar tagname="div" class="actions-col">
          <b-card>
            <BackButton
              text="Liste des documents"
              :to="{ name: 'entreprise-documents' }"
            />

            <div class="d-flex align-items-center justify-content-between">
              <div>
                <h4 class="text-capitalize mt-75 mb-0">
                  {{ document.forme }}
                  <span
                    class="font-weight-bolder"
                    :class="
                      DocumentStateBadgeInfo[document.state].textColor
                    "
                  >
                    - #{{ document.document_number }}
                  </span>
                </h4>
                <span class="text-small text-muted">
                  Fait le
                  {{
                    strftimeFR('%d %B %Y', new Date(document.created_at))
                  }}
                </span>
              </div>
              <DocumentStateBadge :state="document.state" />
            </div>
            <b-row class="mt-1">
              <b-col md="6">
                <b-button
                  variant="outline-primary"
                  block
                  v-ripple
                  class="btn-with-icon justify-content-center"
                  @click="printDocument"
                  disabled
                >
                  <vue-feather type="printer" size="18" class="mr-50" />
                  Imprimer
                </b-button>
              </b-col>
              <b-col md="6">
                <a
                  download
                  v-ripple
                  class="btn btn-outline-primary btn-with-icon justify-content-center mt-1 mt-md-0"
                  target="_blank"
                  :href="document.file"
                >
                  <vue-feather type="download" size="18" class="mr-50" />
                  Télécharger
                </a>
              </b-col>
            </b-row>
          </b-card>

          <b-card>
            <template
              v-if="
                document.forme === DocumentsType.Devis &&
                document.state === DocumentsState.Produced
              "
            >
              <b-button
                variant="success"
                block
                v-ripple
                class="btn-with-icon justify-content-center"
                @click="changeDocumentState(DocumentsState.DevisAccepted)"
              >
                <vue-feather type="check-circle" size="18" class="mr-50" />
                Devis accepté
              </b-button>

              <b-button
                variant="danger"
                block
                v-ripple
                class="btn-with-icon justify-content-center mt-1"
                @click="changeDocumentState(DocumentsState.DevisRefused)"
              >
                <vue-feather type="x-circle" size="18" class="mr-50" />
                Devis refusé
              </b-button>
              <hr />
            </template>

            <template
              v-if="
                document.forme === DocumentsType.Devis &&
                document.state === DocumentsState.DevisAccepted &&
                !document.linked_facture
              "
            >
              <b-button
                variant="primary"
                block
                v-ripple
                class="btn-with-icon justify-content-center"
                @click="produceFacture"
              >
                <vue-feather type="file-text" size="18" class="mr-50" />
                Produire la facture
              </b-button>

              <ProduceAcompte :document="document" />
              <hr />
            </template>

            <b-button
              v-if="
                (document.forme === DocumentsType.Facture ||
                  document.forme == DocumentsType.Acompte) &&
                document.state === DocumentsState.Produced
              "
              variant="dark"
              block
              v-ripple
              class="btn-with-icon justify-content-center mb-50"
              @click="changeDocumentState(DocumentsState.Paid)"
            >
              <vue-feather type="check-circle" size="18" class="mr-50" />
              {{
                document.forme === DocumentsType.Facture
                  ? 'Facture payée'
                  : 'Acompte payé'
              }}
            </b-button>

            <b-button
              v-if="
                document.forme === DocumentsType.Facture &&
                document.state === DocumentsState.Paid
              "
              variant="warning"
              block
              v-ripple
              class="btn-with-icon justify-content-center"
              :to="{
                name: 'entreprise-constructor-avoir',
                params: {
                  documentNumber: document.document_number
                }
              }"
            >
              <vue-feather type="corner-up-left" size="18" class="mr-50" />
              Créer un avoir
            </b-button>

            <b-button
              v-if="
                document.forme !== DocumentsType.Avoir &&
                document.forme !== DocumentsType.Acompte
              "
              variant="outline-secondary"
              block
              v-ripple
              class="btn-with-icon justify-content-center"
              @click="duplicateDocument"
            >
              <vue-feather type="copy" size="18" class="mr-50" />
              Dupliquer
            </b-button>

            <b-button
              v-if="
                document.forme === DocumentsType.Devis &&
                document.state === DocumentsState.Produced
              "
              variant="outline-danger"
              block
              v-ripple
              class="btn-with-icon justify-content-center"
              @click="deleteDocument"
            >
              <vue-feather type="trash-2" size="18" class="mr-50" />
              Supprimer
            </b-button>

            <template v-if="document.linked_facture">
              <hr />

              <p class="text-center mb-0">Facture liée :</p>
              <b-button
                variant="flat-primary"
                block
                v-ripple
                class="btn-with-icon justify-content-center mt-25"
                :to="{
                  name: 'entreprise-document-view',
                  params: {
                    documentId: document.linked_facture.id,
                    documentNumber: document.linked_facture.document_number
                  }
                }"
              >
                <vue-feather type="file-text" size="18" class="mr-50" />
                Facture {{ document.linked_facture.document_number }}
              </b-button>
            </template>

            <template v-if="document.linked_parent_facture">
              <p class="text-center mb-0">Facture liée :</p>
              <b-button
                variant="flat-primary"
                block
                v-ripple
                class="btn-with-icon justify-content-center mt-25"
                :to="{
                  name: 'entreprise-document-view',
                  params: {
                    documentId: document.linked_parent_facture.id,
                    documentNumber:
                      document.linked_parent_facture.document_number
                  }
                }"
              >
                <vue-feather type="file-text" size="18" class="mr-50" />
                Facture
                {{ document.linked_parent_facture.document_number }}
              </b-button>
            </template>

            <template v-if="document.linked_avoirs.length > 0">
              <hr />

              <p class="text-center mb-0">Avoirs liés :</p>
              <b-button
                v-for="avoir in document.linked_avoirs"
                :key="`acompte-${avoir.id}`"
                variant="flat-dark"
                block
                v-ripple
                class="btn-with-icon justify-content-center mt-25"
                :to="{
                  name: 'entreprise-document-view',
                  params: {
                    documentId: avoir.id,
                    documentNumber: avoir.document_number
                  }
                }"
              >
                <vue-feather type="file-text" size="18" class="mr-50" />
                Avoir {{ avoir.document_number }}
              </b-button>
            </template>

            <template v-if="document.linked_parent_devis">
              <hr v-if="document.forme !== DocumentsType.Acompte" />

              <p class="text-center mb-0">Devis lié:</p>
              <b-button
                variant="flat-success"
                block
                v-ripple
                class="btn-with-icon justify-content-center mt-25"
                :to="{
                  name: 'entreprise-document-view',
                  params: {
                    documentId: document.linked_parent_devis.id,
                    documentNumber:
                      document.linked_parent_devis.document_number
                  }
                }"
              >
                <vue-feather type="file-text" size="18" class="mr-50" />
                Devis {{ document.linked_parent_devis.document_number }}
              </b-button>
            </template>

            <template v-if="document.linked_acomptes.length > 0">
              <hr />

              <p class="text-center mb-0">Acomptes liés :</p>
              <b-button
                v-for="acompte in document.linked_acomptes"
                :key="`acompte-${acompte.id}`"
                variant="flat-primary"
                block
                v-ripple
                class="btn-with-icon justify-content-center mt-25"
                :to="{
                  name: 'entreprise-document-view',
                  params: {
                    documentId: acompte.id,
                    documentNumber: acompte.document_number
                  }
                }"
              >
                <vue-feather type="file-text" size="18" class="mr-50" />
                Acompte {{ acompte.document_number }}
              </b-button>
            </template>

            <template v-if="document.linked_devis">
              <hr />

              <p class="text-center mb-0">Devis liée :</p>
              <b-button
                variant="flat-success"
                block
                v-ripple
                class="btn-with-icon justify-content-center mt-25"
                :to="{
                  name: 'entreprise-document-view',
                  params: {
                    documentId: document.linked_devis.id,
                    documentNumber: document.linked_devis.document_number
                  }
                }"
              >
                <vue-feather type="file-text" size="18" class="mr-50" />
                Devis {{ document.linked_devis.document_number }}
              </b-button>
            </template>
          </b-card>

          <b-card>
            <div class="d-flex justify-content-between">
              <h4 class="mb-25">Client</h4>
              <h4 class="mb-25 ml-1 text-primary">
                {{ document.client.client_number }}
              </h4>
            </div>
            <p>
              {{ document.client.socialreasonorname }}
            </p>

            <b-button
              variant="primary"
              v-ripple
              block
              class="btn-with-icon"
              :to="{
                name: 'entreprise-client-view',
                params: {
                  clientId: document.client.id,
                  clientNumber: document.client.client_number
                }
              }"
            >
              <vue-feather type="user" size="18" class="mr-50" />
              Voir la fiche client
            </b-button>
          </b-card>
        </vue-perfect-scrollbar>
      </b-col>
    </b-row>
    <!-- height is used to avoid a UI bug for loader being positioned on the top of the page-->
    <div v-else style="height: 50vh" />
  </b-overlay>
</template>

<style lang="scss" scoped>
.actions-col {
  max-height: calc(100vh - 102px - 1rem);
  overflow-y: hidden;
}
</style>

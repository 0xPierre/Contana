<script lang="ts" setup>
import { onBeforeMount, ref } from 'vue'
import ConstructorClient from './ConstructorClient.vue'
import ConstructorComplementaryInfos from './ConstructorComplementaryInfos.vue'
import ConstructorCatalogue from '@/views/apps/constructor/Catalog/ConstructorCatalog.vue'
import { useConstructorStore } from '@/stores/apps/Constructor'
import { DocumentsType, PaymentsMethod } from '@/types/core.types'
import draggable from 'vuedraggable'
import { v4 as uuidv4 } from 'uuid'
import { Section, SectionsType } from '@/types/constructor.types.ts'
import SectionTitle from '@/components/constructor/sections/SectionTitle.vue'
import SectionSubtotal from '@/components/constructor/sections/SectionSubtotal.vue'
import SectionArticle from '@/components/constructor/sections/SectionArticle.vue'
import { storeToRefs } from 'pinia'
import { notify, swalAlert } from '@/helpers/notify.ts'
import strftime from 'strftime'
import { useRoute, useRouter } from 'vue-router'
import { useDocumentsStore } from '@/stores/apps/Documents.ts'
import { useClientsStore } from '@/stores/apps/Clients.ts'
import ConstructorPreview from '@/views/apps/constructor/ConstructorPreview.vue'

draggable.compatConfig = { MODE: 3 }
const constructorStore = useConstructorStore()
const { sections } = storeToRefs(constructorStore)
const isLoading = ref(false)
const isClientLoading = ref(false)
const route = useRoute()
const router = useRouter()
/**
 * Sections available in the constructor
 */
const availableSections = [
  {
    title: 'Article',
    type: 'section-article',
    values: {
      title: '',
      description: '',

      unitPriceHT: 0,
      vatRate: 20,
      quantity: 1,

      articleType: 'service',

      discount: 0,
      discountType: null,
      discountDescription: '',

      unit: '',

      displayPriceInfos: true
    },
    component: SectionArticle
  },
  {
    title: 'Titre',
    type: 'section-title',
    values: {
      title: ''
    },
    component: SectionTitle
  },
  {
    title: 'Sous-total',
    type: 'section-subtotal',
    values: {
      title: ''
    },
    component: SectionSubtotal
  }
]
const dragging = ref(false)

onBeforeMount(async () => {
  constructorStore.client = null
  constructorStore.paymentMethod = PaymentsMethod.BankTransfer
  constructorStore.forme = DocumentsType.Devis

  if (route.query.hasOwnProperty('forme')) {
    constructorStore.forme = route.query.forme as DocumentsType
  }

  if (route.query.hasOwnProperty('client')) {
    isClientLoading.value = true
    try {
      const clientStore = useClientsStore()
      const {
        data: { data }
      } = await clientStore.getClient(route.query.client as string)
      constructorStore.client = {
        id: data.id,
        client_number: data.client_number,
        socialreasonorname: data.socialreasonorname,
        country: data.country,
        city: data.city,
        zip_code: data.zip_code,
        address: data.address
      }
    } catch {
      notify('Impossible de charger le client', 'danger')
    }
    isClientLoading.value = false
  }
  constructorStore.validityDate = strftime(
    '%d/%m/%Y',
    new Date(new Date().setDate(new Date().getDate() + 90))
  )
  constructorStore.paymentMention = 'À réception de la facture'
  constructorStore.vatPayer = true
  constructorStore.notes =
    'En cas de retard de paiement, il sera appliqué des pénalités et intérêts de retard suivant le taux minimum légal en vigueur, par mois de retard. En outre, une indemnité forfaitaire pour frais de recouvrement de 40€ sera due.'
  constructorStore.otherMention = ''
  constructorStore.sections = []
  constructorStore.subject = ''
  constructorStore.documentNumber = ''
  constructorStore.isDraft = false
  constructorStore.isAvoir = false

  if (route.name === 'entreprise-constructor-draft') {
    isLoading.value = true
    try {
      // Store is initialized in the action
      await constructorStore.getDraft(
        route.params.documentNumber as string
      )
    } catch {
      notify('Impossible de charger le brouillon', 'danger')
      router.push({
        name: 'entreprise-documents'
      })
    }

    isLoading.value = false
  } else if (route.name === 'entreprise-constructor-avoir') {
    constructorStore.isAvoir = true
    constructorStore.forme = DocumentsType.Avoir
    constructorStore.documentNumber = route.params.documentNumber as string
    constructorStore.sections = [
      {
        id: uuidv4(),
        type: 'section-article',
        values: availableSections.find(
          (section) => section.type === 'section-article'
        )?.values,
        component: SectionArticle
      } as Section<SectionArticle>
    ]
  }
})

/**
 * Used to clone/deepclone section to the constructor
 */
const clone = (
  section: Omit<
    Section<
      SectionsType.Article | SectionsType.Title | SectionsType.Subtotal
    >,
    'id'
  >
): Section<
  SectionsType.Article | SectionsType.Title | SectionsType.Subtotal
> => {
  return {
    id: uuidv4(),
    type: section.type,
    values: { ...section.values },
    component: section.component
  }
}

const saveDraft = async () => {
  isLoading.value = true

  try {
    const { data } = await constructorStore.saveDraft()

    if (data.status === 'success') {
      notify('Brouillon enregistré avec succès')
    } else {
      notify(data.error, 'danger')
    }
  } catch {
    notify(
      "Une erreur est survenue lors de l'enregistrement du brouillon",
      'danger'
    )
  }

  isLoading.value = false
}

const produceDocument = async () => {
  isLoading.value = true

  try {
    const { data } = await constructorStore.produceDocument()

    if (data.status === 'success') {
      notify('Document produit avec succès')
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
  } catch (e) {
    console.log(e)
    notify(
      'Une erreur est survenue lors de la production du document',
      'danger'
    )
  }

  isLoading.value = false
}

const deleteDraft = async () => {
  const { value } = await swalAlert(
    'Êtes-vous sûr de vouloir supprimer ce brouillon ?'
  )
  if (!value) return

  isLoading.value = true

  try {
    const documentStore = useDocumentsStore()
    await documentStore.deleteDocument(route.params.documentId as number)

    router.push({ name: 'entreprise-documents' })
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}
</script>

<template>
  <div>
    <b-overlay :show="isLoading">
      <b-row>
        <b-col md="9" class="pr-md-50">
          <b-card class="mb-1 p-1" no-body>
            <b-row>
              <b-col cols="4">
                <v-select
                  :options="
                    constructorStore.isAvoir
                      ? [{ label: 'Avoir', value: DocumentsType.Avoir }]
                      : [
                          {
                            label: 'Devis',
                            value: DocumentsType.Devis
                          },
                          {
                            label: 'Facture',
                            value: DocumentsType.Facture
                          }
                        ]
                  "
                  :clearable="false"
                  v-model="constructorStore.forme"
                  :reduce="(option) => option.value"
                  label="label"
                  block
                />
              </b-col>
              <b-col cols="4">
                <b-form-input
                  :placeholder="`Objet ${constructorStore.formeSentence.second}`"
                  type="text"
                  v-model="constructorStore.subject"
                />
              </b-col>
              <b-col cols="4">
                <ConstructorComplementaryInfos />
              </b-col>
            </b-row>
          </b-card>

          <b-card no-body>
            <div class="area">
              <draggable
                v-model="sections"
                item-key="id"
                class="sections"
                :group="{ name: 'sections' }"
                :scroll-sensitivity="200"
              >
                <template #item="{ element }">
                  <div>
                    <component
                      :is="element.component"
                      :section="element"
                    />
                  </div>
                </template>

                <template #footer>
                  <div
                    class="area dropping-area d-flex justify-content-center align-items-center"
                    :class="{
                      dragging,
                      'empty-area': sections.length === 0
                    }"
                  >
                    <vue-feather type="move" size="28" />
                    <span class="ml-1 font-medium-1">
                      Glissez et déposez des élements ici
                    </span>
                  </div>
                </template>
              </draggable>
            </div>
          </b-card>
        </b-col>
        <b-col md="3" class="pl-md-50">
          <vue-perfect-scrollbar class="actions-col" tagname="div">
            <b-overlay :show="isClientLoading">
              <ConstructorClient v-if="!constructorStore.isAvoir" />
            </b-overlay>
            <b-card class="mb-1 user-select-none p-1" no-body>
              <draggable
                :list="availableSections"
                item-key="type"
                div="div"
                :group="{
                  name: 'sections',
                  pull: 'clone',
                  put: false,
                  sort: false
                }"
                @start="dragging = true"
                @end="dragging = false"
                :clone="clone"
              >
                <template #item="{ element }">
                  <div class="draggable article mx-75">
                    <vue-feather
                      type="move"
                      size="16"
                      class="cursor-pointer"
                    />
                    <span>{{ element.title }}</span>
                  </div>
                </template>
              </draggable>
              <hr class="px-2" />
              <ConstructorCatalogue
                :clone="clone"
                @update-dragging="dragging = $event"
              />
            </b-card>

            <b-card class="p-1" no-body>
              <div>
                <div
                  class="d-flex justify-content-between font-weight-bolder"
                >
                  <span>Total HT</span>
                  <span
                    >{{ constructorStore.isAvoir ? '-' : ''
                    }}{{ constructorStore.totalHT.format() }} €</span
                  >
                </div>
                <div
                  v-if="constructorStore.vatPayer"
                  class="d-flex justify-content-between"
                >
                  <span>TVA</span>
                  <span
                    >{{ constructorStore.isAvoir ? '-' : ''
                    }}{{ constructorStore.totalTVA.format() }} €</span
                  >
                </div>
                <div class="d-flex justify-content-between">
                  <span>Total TTC</span>
                  <span
                    >{{ constructorStore.isAvoir ? '-' : ''
                    }}{{ constructorStore.totalTTC.format() }} €</span
                  >
                </div>
              </div>

              <hr />
              <b-button
                v-ripple
                variant="success"
                block
                class="btn-with-icon mb-50"
                @click="produceDocument"
              >
                <vue-feather type="file-plus" class="mr-50" size="16" />
                Produire {{ constructorStore.formeSentence.first }}
              </b-button>
              <ConstructorPreview />
              <b-button
                v-if="!constructorStore.isAvoir"
                v-ripple
                variant="outline-secondary"
                block
                class="btn-with-icon mt-50"
                @click="saveDraft"
              >
                <vue-feather type="save" class="mr-50" size="16" />
                Enregistrer
                {{ constructorStore.documentNumber ? 'le' : 'en' }}
                brouillon
              </b-button>
              <b-button
                v-if="
                  constructorStore.documentNumber &&
                  constructorStore.isDraft
                "
                v-ripple
                variant="outline-danger"
                block
                class="btn-with-icon"
                @click="deleteDraft"
              >
                <vue-feather type="trash" class="mr-50" size="16" />
                Supprimer le brouillon
              </b-button>
            </b-card>
          </vue-perfect-scrollbar>
        </b-col>
      </b-row>
    </b-overlay>
  </div>
</template>

<style lang="scss">
.actions-col {
  max-height: calc(100vh - 102px - 1rem);
  // overflow-y: auto;
}

.articles-list {
  margin-top: 1rem;
  max-height: 200px;
}
.article {
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: var(--white);
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 10px;
  padding: 13px 15px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);

  span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 80%;
  }
}

.dark-layout {
  .area {
    .dropping-area {
      border-color: #d0d2d6;
    }
  }
  .draggable.article {
    background-color: #161d31;
  }

  .draggable.article:hover {
    background-color: #1f2a48;
  }
}

.area {
  max-height: calc(100vh - 102px - 1rem - 100px - 1rem);
  overflow: auto;

  .dropping-area {
    min-height: 200px;
    border: 2px dashed rgba(0, 0, 0, 0.1);
    border-radius: 5px;
  }

  .empty-area {
    min-height: 350px;

    &.dragging {
      background-color: rgba(0, 0, 0, 0.1);
    }
  }
}

.sections {
  min-height: 350px;
  padding: 1.5rem;
  .section {
    margin: 0 0 1rem 0;
    user-select: none;
    cursor: move;
    padding: 1.2rem;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 5px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  }
}

.dark-layout {
  .section {
    box-shadow: 0 1px 10px rgba(0, 0, 0, 0.2);
  }
}

.flip-list-move {
  transition: transform 0.5s;
}

.no-move {
  transition: transform 0s;
}
</style>

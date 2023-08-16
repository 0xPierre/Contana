<script lang="ts" setup>
import { ref, onBeforeMount } from 'vue'
import { useClientsStore } from '@/stores/apps/Clients'
import { useRoute, useRouter } from 'vue-router'
import BackButton from '@/components/back-button/BackButton.vue'
import type { ClientModel } from '@/types/clients.types'
import { notify, notifyApiError, swalAlert } from '@/helpers/notify'
import { AxiosError } from 'axios'
import FileUploadManager from '@/components/file-upload-manager/FileUploadManager.vue'

const clientsStore = useClientsStore()
const client = ref<ClientModel>({
  id: 0,
  socialreasonorname: '',
  email: '',
  phone: '',
  country: '',
  city: '',
  zip_code: '',
  address: '',
  vat_number: '',
  siret: '',
  note: '',
  type: 'professionnel',
  website: '',
  archived: false,
  created_at: '',
  updated_at: '',
  client_number: '',
  files: []
})
const route = useRoute()
const router = useRouter()
const isLoading = ref(false)

onBeforeMount(async () => {
  isLoading.value = true

  const { data } = await clientsStore.getClient(
    route.params.clientId as string
  )
  client.value = data.data

  document.title = `Client ${client.value.client_number} - Contana`

  isLoading.value = false
})

const updateClient = async () => {
  isLoading.value = true

  try {
    await clientsStore.updateClient({
      ...client.value,
      files: undefined
    })

    notify('Client mis à jour', 'success')
  } catch (e) {
    if (e instanceof AxiosError && e.response?.status === 400)
      notifyApiError(e.response.data)
    else notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}

const filesUpdate = (newFiles: any[]) => {
  client.value.files = newFiles
}

const saveFiles = async () => {
  isLoading.value = true

  try {
    await clientsStore.saveClientFiles(client.value.id, client.value.files)

    notify('Fichiers mis à jour', 'success')
  } catch (e) {
    if (e instanceof AxiosError && e.response?.status === 400)
      notifyApiError(e.response.data)
    else notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}

const archiveClient = async () => {
  const { value } = await swalAlert(
    'Attention',
    'warning',
    `Êtes vous sûr de vouloir archiver ce client ?`
  )

  if (!value) return

  isLoading.value = true

  try {
    await clientsStore.archiveClient(client.value)

    notify('Client archivé', 'success')

    router.push({ name: 'entreprise-clients' })
  } catch (e) {
    if (e instanceof AxiosError && e.response?.status === 400)
      notifyApiError(e.response.data)
    else notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}

const unarchiveClient = async () => {
  const { value } = await swalAlert(
    'Attention',
    'warning',
    `Êtes vous sûr de vouloir désarchiver ce client ?`
  )

  if (!value) return

  isLoading.value = true

  try {
    await clientsStore.unarchiveClient(client.value)

    notify('Client désarchiver', 'success')

    router.push({ name: 'entreprise-clients' })
  } catch (e) {
    if (e instanceof AxiosError && e.response?.status === 400)
      notifyApiError(e.response.data)
    else notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}
</script>

<template>
  <b-overlay :show="isLoading">
    <b-card>
      <div class="d-flex justify-content-md-between">
        <div class="d-flex">
          <BackButton
            text="Liste des clients"
            :to="{ name: 'entreprise-clients' }"
          />
          <h4 class="ml-2 mt-50">
            Client n°{{ client.client_number }}
            <span
              v-if="client.archived"
              class="font-weight-bolder text-dark"
            >
              - archivé
            </span>
          </h4>
        </div>

        <div>
          <b-button
            v-if="!client.archived"
            variant="flat-secondary"
            v-ripple
            @click="archiveClient"
          >
            Archiver le client
          </b-button>
          <b-button
            v-else
            variant="flat-secondary"
            v-ripple
            @click="unarchiveClient"
          >
            Désarchiver le client
          </b-button>
        </div>
      </div>
    </b-card>

    <b-row>
      <b-col md="8">
        <b-card>
          <div class="d-flex">
            <vue-feather type="user" />
            <h3 class="ml-50">Informations générales</h3>
          </div>
          <b-row>
            <b-col md="6">
              <b-form-group label="Raison sociale ou nom">
                <b-form-input
                  v-model="client.socialreasonorname"
                  placeholder="Entreprise Dupond"
                />
              </b-form-group>

              <b-form-group label="Téléphone">
                <b-form-input
                  v-model="client.phone"
                  placeholder="06 12 34 56 78"
                />
              </b-form-group>

              <b-form-group
                v-show="client.type === 'professionnel'"
                label="Siret"
              >
                <b-input
                  v-model="client.siret"
                  placeholder="97245934"
                  type="text"
                />
              </b-form-group>

              <b-form-group label="Site internet">
                <b-input
                  v-model="client.website"
                  placeholder="https://entreprise-dupond.fr"
                  type="url"
                />
              </b-form-group>
            </b-col>
            <b-col md="6">
              <b-form-group label="Adresse email">
                <b-form-input
                  v-model="client.email"
                  placeholder="contact@dupond.fr"
                />
              </b-form-group>

              <b-form-group label="Type">
                <v-select
                  label="label"
                  v-model="client.type"
                  :options="[
                    { label: 'Professionnel', value: 'professionnel' },
                    { label: 'Particulier', value: 'particulier' }
                  ]"
                  :reduce="(option: any) => option.value"
                  :clearable="false"
                />
              </b-form-group>

              <b-form-group
                v-show="client.type === 'professionnel'"
                label="N° de TVA intracommunautaire"
              >
                <b-input
                  v-model="client.vat_number"
                  placeholder="FR 00 000 000 000"
                  type="text"
                />
              </b-form-group>
            </b-col>
          </b-row>

          <hr />

          <div class="d-flex mt-1 mb-50">
            <vue-feather type="map-pin" size="22" class="mr-1" />
            <h3>Localisation</h3>
          </div>
          <b-row>
            <b-col md="6">
              <b-form-group label="Adresse">
                <b-input
                  v-model="client.address"
                  placeholder="11 rue des champs élysées"
                />
              </b-form-group>

              <b-form-group label="Code postal">
                <b-input v-model="client.zip_code" placeholder="71000" />
              </b-form-group>
            </b-col>
            <b-col md="6">
              <b-form-group label="Ville">
                <b-input v-model="client.city" placeholder="Paris" />
              </b-form-group>

              <b-form-group label="Pays">
                <b-input v-model="client.country" placeholder="France" />
              </b-form-group>
            </b-col>
          </b-row>

          <hr />

          <div class="d-flex mt-1 mb-50">
            <vue-feather type="info" size="22" class="mr-1" />
            <h3>Autre</h3>
          </div>

          <b-form-group label="Commentaire">
            <b-textarea
              v-model="client.note"
              placeholder="Commentaire sur le client"
              rows="3"
              max-rows="10"
            />
          </b-form-group>

          <b-button
            variant="primary"
            v-ripple
            @click="updateClient"
            :disabled="client.archived"
          >
            Enregistrer
          </b-button>
        </b-card>
      </b-col>

      <b-col md="4">
        <b-card classs>
          <div class="d-flex">
            <vue-feather type="file-text" size="22" class="mr-1" />
            <h3 class="m-0">Documents</h3>
          </div>
          <span class="text-muted"> 0 document(s) enregistré(s) </span>

          <div v-if="true" class="mt-1">
            <b-button
              variant="flat-success"
              class="btn-with-icon"
              block
              v-ripple
              :disabled="client.archived"
            >
              <vue-feather type="file-plus" size="18" class="mr-50" />
              Créer une facture
            </b-button>

            <b-button
              variant="flat-info"
              class="btn-with-icon"
              block
              v-ripple
              :disabled="client.archived"
            >
              <vue-feather type="file-plus" size="18" class="mr-50" />
              Créer un devis
            </b-button>

            <b-button
              variant="flat-dark"
              class="btn-with-icon"
              block
              v-ripple
              :disabled="client.archived"
            >
              <vue-feather type="file-plus" size="18" class="mr-50" />
              Créer un avoir
            </b-button>
          </div>
        </b-card>

        <b-card>
          <div class="d-flex">
            <vue-feather type="file" size="22" class="mr-1" />
            <h3 class="mb-50">Fichiers</h3>
          </div>

          <file-upload-manager
            :files="client.files"
            :preview="true"
            :multiple="true"
            @update-files="filesUpdate"
            :disabled="client.archived"
            label="Ajouter des fichiers liés au client"
          />

          <b-button
            class="mt-1"
            variant="primary"
            v-ripple
            :disabled="client.archived"
            @click="saveFiles"
          >
            Enregistrer les fichiers
          </b-button>
        </b-card>
      </b-col>
    </b-row>
  </b-overlay>
</template>

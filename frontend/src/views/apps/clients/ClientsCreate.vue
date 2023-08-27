<script lang="ts" setup>
import { reactive, ref, watch } from 'vue'
import type { ClientCreationForm } from '@/types/clients.types'
import { useClientsStore } from '@/stores/apps/Clients'
import { notify, notifyApiError } from '@/helpers/notify'
import { AxiosError } from 'axios'
import router from '@/router'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'

const clientStore = useClientsStore()
const entrepriseStore = useEntrepriseStore()

const entrepriseSearchString = ref('')
const entreprisesFound = ref<any[]>([])
const isEntrepriseSearchLoading = ref(false)

const showClientFields = ref(false)

const isLoading = ref(false)

const clientInitialData: ClientCreationForm = {
  socialreasonorname: '',
  email: '',
  phone: '',
  country: '',
  city: '',
  zip_code: '',
  address: '',
  vat_number: '',
  siren: '',
  note: '',
  type: 'professionnel',
  website: ''
}

const client = reactive<ClientCreationForm>({ ...clientInitialData })

watch(entrepriseSearchString, async () => {
  if (entrepriseSearchString.value.length < 3) {
    entreprisesFound.value = []
    return
  }

  isEntrepriseSearchLoading.value = true
  try {
    const response = await fetch(
      `https://recherche-entreprises.api.gouv.fr/search?q=${entrepriseSearchString.value}&per_page=3`
    )
    entreprisesFound.value = (await response.json()).results
  } finally {
    isEntrepriseSearchLoading.value = false
  }
})

const clearClientModal = () => {
  entreprisesFound.value = []
  entrepriseSearchString.value = ''
  Object.assign(client, clientInitialData)
}

const fillManually = () => {
  clearClientModal()

  showClientFields.value = true
}

const fillAutomatically = () => {
  clearClientModal()

  showClientFields.value = false
}

const createClientModal = ref<any>(null)

const openModal = () => {
  createClientModal.value.show()

  clearClientModal()
  showClientFields.value = false
}

const selectEntreprise = (entreprise: any) => {
  client.socialreasonorname = entreprise.nom_complet
  client.siren = entreprise.siren
  client.address = entreprise.siege.libelle_voie
  client.zip_code = entreprise.siege.code_postal
  client.city = entreprise.siege.libelle_commune
  // Country is always France when using the API because the API only returns french companies
  client.country = 'France'

  showClientFields.value = true
}

const createClient = async () => {
  isLoading.value = true
  try {
    const { data } = await clientStore.createClient(client)

    notify('Client créé avec succès', 'success')

    createClientModal.value.hide()

    router.push({
      name: 'entreprise-client-view',
      params: {
        clientNumber: data.data.client_number,
        clientId: data.data.id,
        entrepriseSlug: entrepriseStore.entreprise?.slug
      }
    })
  } catch (e) {
    if (e instanceof AxiosError && e.response?.status === 400)
      notifyApiError(e.response.data)
    else notify('Une erreur est survenue', 'danger')
    console.log(e)
  }

  isLoading.value = false
}
</script>

<template>
  <b-button
    variant="primary"
    class="btn-with-icon"
    v-ripple
    @click="openModal"
  >
    <vue-feather type="user-plus" size="18" class="mr-1" />
    <span class="align-middle"> Créer un client </span>
  </b-button>

  <b-modal
    ref="createClientModal"
    title="Créer un nouveau client"
    size="lg"
    id="modal-create-client"
  >
    <b-overlay :show="isLoading">
      <div v-if="!showClientFields">
        <b-overlay :show="isEntrepriseSearchLoading">
          <b-form-group
            label="Recherche automatique de l'entreprise par nom,siren,adresse..."
          >
            <b-input
              v-model="entrepriseSearchString"
              debounce="300"
              placeholder="Rechercher une entreprise par nom, siren ou adresse"
            />
          </b-form-group>

          <b-list-group>
            <b-list-group-item
              v-for="entreprise in entreprisesFound"
              :key="entreprise.siren"
              class="d-flex justify-content-between align-items-center cursor-pointer"
              @click="selectEntreprise(entreprise)"
            >
              <div>
                <b
                  >{{ entreprise.nom_complet }} ( Siren :
                  {{ entreprise.siren }} )</b
                >
                <br />
                <small class="text-muted">
                  {{ entreprise.siege.libelle_voie }}
                  <br />
                  {{ entreprise.siege.code_postal }}
                  {{ entreprise.siege.libelle_commune }}
                </small>
              </div>
              <b-button variant="outline-primary" size="sm" v-ripple>
                Sélectionner
              </b-button>
            </b-list-group-item>
          </b-list-group>

          <div
            v-if="
              entreprisesFound.length === 0 &&
              entrepriseSearchString.length > 2 &&
              !isEntrepriseSearchLoading
            "
          >
            Aucune entreprise trouvée
          </div>
        </b-overlay>

        <b-button
          variant="outline-primary"
          class="mt-1"
          size="sm"
          v-ripple
          @click="fillManually"
        >
          Remplir manuellement
        </b-button>
      </div>

      <div v-else>
        <b-button
          variant="outline-secondary"
          class="mb-1"
          size="sm"
          v-ripple
          @click="fillAutomatically"
        >
          Rechercher une autre entreprise
        </b-button>

        <div class="d-flex mt-1 mb-50">
          <vue-feather type="user" size="22" class="mr-1" />
          <h3>Informations du client</h3>
        </div>
        <b-row>
          <b-col md="6">
            <b-form-group label="Raison sociale ou nom">
              <b-input
                v-model="client.socialreasonorname"
                placeholder="Entreprise Dupond"
              />
            </b-form-group>

            <b-form-group label="Téléphone">
              <b-input
                v-model="client.phone"
                placeholder="06 12 34 56 78"
                type="tel"
              />
            </b-form-group>

            <b-form-group
              v-show="client.type === 'professionnel'"
              label="Siren"
            >
              <b-input
                v-model="client.siren"
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
          <b-col>
            <b-form-group label="Adesse email">
              <b-input
                v-model="client.email"
                placeholder="contact@dupond.fr"
                type="email"
              />
            </b-form-group>

            <b-form-group label="Type">
              <v-select
                v-model="client.type"
                :options="[
                  { label: 'Professionnel', value: 'professionnel' },
                  { label: 'Particulier', value: 'particulier' }
                ]"
                :reduce="(option: any) => option.value"
                label="label"
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
      </div>
    </b-overlay>
    <template #modal-footer="{ cancel }">
      <template v-if="showClientFields">
        <b-button
          variant="outline-secondary"
          v-ripple
          @click="cancel"
          :disabled="isLoading"
        >
          Annuler
        </b-button>
        <b-button
          variant="primary"
          v-ripple
          :disabled="isLoading"
          @click="createClient"
        >
          Créer
        </b-button>
      </template>
    </template>
  </b-modal>
</template>
@/types/clients.types

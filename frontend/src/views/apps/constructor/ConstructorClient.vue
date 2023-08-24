<script lang="ts" setup>
import { useConstructorStore } from '@/stores/apps/Constructor'
import { useClientsStore } from '@/stores/apps/Clients'
import { ref, reactive, watch, onMounted } from 'vue'
import { notify, notifyApiError } from '@/helpers/notify'
import { AxiosError } from 'axios'
import type { ClientConstructor, ClientModel } from '@/types/clients.types'
import { useRoute } from 'vue-router'

const constructorStore = useConstructorStore()
const clientsStore = useClientsStore()
const route = useRoute()

const isLoading = ref(false)
const isListingLoading = ref(false)
const clientListingModal = ref<HTMLElement | null>(null)
const addNewClientModal = ref<HTMLElement | null>(null)
const selectedClient = ref<ClientConstructor | null>(null)
const defaultFilters = {
  perPage: 5,
  currentPage: 1,
  search: '',
  archived: false,
  sortBy: 'id',
  sortDesc: true
}
const filters = reactive({ ...defaultFilters })
const newClientData: ClientConstructor = {
  id: -1,
  socialreasonorname: '',
  country: '',
  city: '',
  zip_code: '',
  address: '',
  client_number: ''
}
const newClient = reactive({ ...newClientData })

const openClientListingModal = () => {
  getClients()
  Object.assign(filters, defaultFilters)
  clientListingModal.value.show()
  selectedClient.value = null
}

const openAddNewClientModal = () => {
  Object.assign(newClient, newClientData)
  addNewClientModal.value.show()
}

const createClient = async () => {
  isLoading.value = true
  try {
    let { data } = await clientsStore.createClient(newClient)
    data = data.data

    clientListingModal.value.hide()
    addNewClientModal.value.hide()

    constructorStore.client = {
      id: data.id,
      client_number: data.client_number,
      socialreasonorname: data.socialreasonorname,
      country: data.country,
      city: data.city,
      zip_code: data.zip_code,
      address: data.address
    }
  } catch (e) {
    if (e instanceof AxiosError && e.response?.status === 400)
      notifyApiError(e.response.data)
    else notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}

const getClients = async () => {
  isListingLoading.value = true

  try {
    await clientsStore.getClients(filters)
  } catch {
    notify(
      'Une erreur est survenue lors du chargement des clients',
      'danger'
    )
  }

  isListingLoading.value = false
}

watch(
  [
    () => filters.perPage,
    () => filters.search,
    () => filters.archived,
    () => filters.sortBy,
    () => filters.sortDesc
  ],
  () => {
    filters.currentPage = 1
    getClients()
  }
)
watch(
  () => filters.currentPage,
  () => {
    getClients()
  }
)

const selectTemporaryClient = (client: ClientConstructor[]) => {
  if (client.length === 0) selectedClient.value = null
  else {
    selectedClient.value = {
      id: client[0].id,
      client_number: client[0].client_number,
      socialreasonorname: client[0].socialreasonorname,
      country: client[0].country,
      city: client[0].city,
      zip_code: client[0].zip_code,
      address: client[0].address
    }
  }
}

const selectClient = (client: ClientConstructor) => {
  if (client) {
    /**
     * Used when double-clicking on a client in the listing modal
     */
    selectTemporaryClient([client])
  }

  if (selectedClient.value) {
    constructorStore.client = selectedClient.value
    clientListingModal.value.hide()
  }
}

onMounted(() => {
  if (route.name === 'entreprise-constructor') {
    openClientListingModal()
  }
})
</script>

<template>
  <div>
    <b-card class="mb-1 p-1" no-body>
      <div
        class="d-flex justify-content-between align-items-center flex-row"
        :class="{ 'cursor-pointer': constructorStore.client }"
        @click="constructorStore.client ? openClientListingModal() : null"
      >
        <div>
          <h4 v-if="constructorStore.client" class="font-medium-1">
            Client
            <span class="font-weight-bolder text-primary">
              {{ constructorStore.client.client_number }}
            </span>
          </h4>

          <div v-if="!constructorStore.client">
            <b-button
              variant="primary"
              block
              v-ripple
              @click="openClientListingModal"
            >
              Sélectionner un client
            </b-button>
          </div>

          <div v-else class="font-small-3">
            <h4 class="mb-0 font-medium-1">
              {{ constructorStore.client.socialreasonorname }}
            </h4>
          </div>
        </div>
        <div v-show="constructorStore.client">
          <vue-feather
            type="edit"
            class="cursor-pointer"
            @click="openClientListingModal"
          />
        </div>
      </div>
    </b-card>

    <b-modal
      ref="clientListingModal"
      title="Sélectionner un client"
      size="md"
    >
      <b-form-group label="Rechercher un client">
        <b-form-input
          v-model="filters.search"
          debounce="300"
          placeholder="Entreprise Dupo..."
          type="search"
          autocomplete="off"
          :disabled="isLoading"
        />
      </b-form-group>
      <b-overlay :show="isListingLoading">
        <b-table
          hover
          :items="clientsStore.listing.clients"
          :fields="[
            {
              key: 'socialreasonorname',
              label: 'Raison social',
              sortable: true
            },
            { key: 'address', label: 'Adresse', sortable: false }
          ]"
          v-model:sort-by="filters.sortBy"
          v-model:sort-desc="filters.sortDesc"
          primary-key="id"
          :no-local-sorting="true"
          show-empty
          empty-text="Aucun client trouvé"
          class="position-relative mb-1 mt-50"
          selectable
          select-mode="single"
          @row-selected="selectTemporaryClient"
          @row-dblclicked="selectClient"
        >
          <template #cell(address)="row">
            {{ row.item.address }} {{ row.item.zip_code }}
            {{ row.item.city }}
          </template>
        </b-table>
      </b-overlay>
      <div class="d-flex align-items-center justify-content-center">
        <b-pagination
          v-model="filters.currentPage"
          :total-rows="clientsStore.listing.total"
          :per-page="filters.perPage"
          first-number
          last-number
          prev-class="prev-item"
          next-class="next-item"
        >
          <template #prev-text>
            <vue-feather type="chevron-left" size="18" />
          </template>
          <template #next-text>
            <vue-feather type="chevron-right" size="18" />
          </template>
        </b-pagination>
      </div>
      <template #modal-footer="{ cancel }">
        <b-button
          variant="outline-secondary"
          v-ripple
          @click="cancel"
          :disabled="isLoading"
        >
          Annuler
        </b-button>
        <b-button
          variant="outline-primary"
          v-ripple
          :disabled="isLoading"
          @click="openAddNewClientModal"
        >
          Ajouter un client
        </b-button>
        <b-button
          variant="primary"
          v-ripple
          :disabled="isLoading || selectedClient === null"
          @click="selectClient(null)"
        >
          Sélectionner
        </b-button>
      </template>
    </b-modal>

    <b-modal
      ref="addNewClientModal"
      title="Ajouter un nouveau client"
      size="md"
    >
      <b-overlay :show="isLoading">
        <b-form-group label="Raison sociale ou nom">
          <b-form-input
            v-model="newClient.socialreasonorname"
            placeholder="Entreprise Dupond"
          />
        </b-form-group>

        <b-form-group label="Adresse">
          <b-form-input
            v-model="newClient.address"
            placeholder="1 rue de la paix"
          />
        </b-form-group>

        <b-form-group label="Code postal">
          <b-form-input v-model="newClient.zip_code" placeholder="75000" />
        </b-form-group>

        <b-form-group label="Ville">
          <b-form-input v-model="newClient.city" placeholder="Paris" />
        </b-form-group>

        <b-form-group label="Pays">
          <b-form-input v-model="newClient.country" placeholder="France" />
        </b-form-group>
      </b-overlay>

      <template #modal-footer="{ cancel }">
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
          Ajouter
        </b-button>
      </template>
    </b-modal>
  </div>
</template>

<style lang="scss">
.b-table-row-selected {
  font-weight: bold;
}

body.dark-layout .b-table-row-selected td {
  background-color: #161d31 !important;
}
body.dark-layout .b-table tbody tr:hover td {
  background-color: #161d31 !important;
  background-image: none !important;
}
</style>

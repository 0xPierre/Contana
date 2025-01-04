<script lang="ts" setup>
import { onBeforeMount, reactive, ref, watch } from 'vue'
import ClientsCreate from './ClientsCreate.vue'
import { useClientsStore } from '@/stores/apps/Clients'
import { notify } from '@/helpers/notify'
import router from '@/router'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'
import { useUserStore } from '@/stores/apps/User'
import type { EntrepriseUser } from '@/types/entreprise.types'
import { can } from '@/helpers/permissions.ts'

const entrepriseStore = useEntrepriseStore()
const userStore = useUserStore()
const clientsStore = useClientsStore()
const isListingLoading = ref(false)
const isFiltersUpdateFromQuery = ref(false)
const filters = reactive({
  perPage: 25,
  currentPage: 1,
  search: '',
  archived: false,
  createdBy: userStore.data?.id || -1,
  sortBy: 'id',
  sortDesc: true
})

const setClientsListingArchivedFilter = (archived: boolean) => {
  filters.archived = archived
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
  isFiltersUpdateFromQuery.value = false
}

const saveFiltersInQuery = () => {
  router.push({
    query: {
      perPage: filters.perPage,
      currentPage: filters.currentPage,
      search: filters.search,
      archived: filters.archived.toString(),
      createdBy: filters.createdBy?.toString(),
      sortBy: filters.sortBy,
      sortDesc: filters.sortDesc.toString()
    }
  })
}

watch(
  [
    () => filters.perPage,
    () => filters.search,
    () => filters.archived,
    () => filters.sortBy,
    () => filters.sortDesc,
    () => filters.createdBy
  ],
  () => {
    if (!isFiltersUpdateFromQuery.value) {
      filters.currentPage = 1
      getClients()
      saveFiltersInQuery()
    } else isFiltersUpdateFromQuery.value = false
  }
)

watch(
  () => filters.currentPage,
  () => {
    getClients()
    saveFiltersInQuery()
  }
)

const rowClicked = (item: any) => {
  router.push({
    name: 'entreprise-client-view',
    params: { clientId: item.id, clientNumber: item.client_number }
  })
}

onBeforeMount(() => {
  const url = new URL(window.location.href)
  const searchParams = url.searchParams

  if (searchParams.get('perPage')) {
    filters.perPage = parseInt(searchParams.get('perPage') as string)
    filters.currentPage = parseInt(
      searchParams.get('currentPage') as string
    )
    filters.search = searchParams.get('search') as string
    filters.archived = searchParams.get('archived') === 'true'
    filters.createdBy = parseInt(searchParams.get('createdBy') || ''),
    filters.sortBy = searchParams.get('sortBy') as string
    filters.sortDesc = searchParams.get('sortDesc') === 'true'

    isFiltersUpdateFromQuery.value = true
  }
  getClients()
})
</script>

<template>
  <div>
    <div class="d-flex justify-content-between">
      <ul class="nav nav-pills">
        <li class="nav-item">
          <a
            href="#"
            class="nav-link"
            :class="{ active: !filters.archived }"
            @click="setClientsListingArchivedFilter(false)"
          >
            <vue-feather type="users" size="18" class="mr-50" />
            <span class="font-weight-bold">Clients actifs</span>
          </a>
        </li>
        <li class="nav-item">
          <a
            href="#"
            class="nav-link"
            :class="{ active: filters.archived }"
            @click="setClientsListingArchivedFilter(true)"
          >
            <vue-feather type="archive" size="18" class="mr-50" />
            <span class="font-weight-bold">Clients archivés</span>
          </a>
        </li>
      </ul>
      <div>
        <ClientsCreate />
      </div>
    </div>

    <b-card>
      <b-row>
        <b-col md="4">
          <b-form-group label="Recherche par texte">
            <b-form-input
              v-model="filters.search"
              placeholder="Entreprise Durand"
              debounce="300"
            />
          </b-form-group>
        </b-col>
        <b-col md="4">
          <b-form-group label="Clients par page">
            <v-select
              :options="[10, 25, 50, 100]"
              v-model="filters.perPage"
              :clearable="false"
            />
          </b-form-group>
        </b-col>
        <b-col v-if="can('administrate')" md="4">
          <b-form-group label="Créé par">
            <v-select
              v-model="filters.createdBy"
              :options="[{ full_name: 'Tous les utilisateurs', id: -1},  ...entrepriseStore.entreprise?.users]"
              label="full_name"
              :reduce="(option: EntrepriseUser) => option.id"
              placeholder="Tous les utilisateurs"
              :clearable="false"
            />
          </b-form-group>
        </b-col>
      </b-row>

      <b-overlay :show="isListingLoading">
        <b-table
          hover
          :items="clientsStore.listing.clients"
          :fields="[
            { key: 'client_number', label: 'Numéro', sortable: true },
            { key: 'status', label: 'Status', sortable: false },
            {
              key: 'socialreasonorname',
              label: 'Raison social',
              sortable: true
            },
            { key: 'phone', label: 'Téléphone', sortable: true },
            { key: 'email', label: 'Email', sortable: true },
            { key: 'address', label: 'Adresse', sortable: false },
            { key: 'created_by', label: 'Créé par', sortable: false }
          ]"
          v-model:sort-by="filters.sortBy"
          v-model:sort-desc="filters.sortDesc"
          primary-key="id"
          :no-local-sorting="true"
          show-empty
          empty-text="Aucun client trouvé"
          class="position-relative mb-1 mt-50"
          @row-clicked="rowClicked"
        >
          <template #cell(client_number)="row">
            <router-link
              :to="{
                name: 'entreprise-client-view',
                params: {
                  clientId: row.item.id,
                  clientNumber: row.item.client_number
                }
              }"
              class="font-weight-bolder"
            >
              {{ row.value }}
            </router-link>
          </template>

          <template #cell(socialreasonorname)="row">
            <span class="truncate-text-ellipsis" style="max-width: 250px">
              {{ row.value }}
            </span>
          </template>

          <template #cell(status)="row">
            <b-badge v-if="row.item.archived" variant="light-secondary">
              Archivé
            </b-badge>
            <b-badge v-else variant="light-success"> Actif </b-badge>
          </template>

          <template #cell(address)="row">
            <span
              v-if="row.item.address"
              class="truncate-text-ellipsis"
              style="max-width: 200px"
            >
              {{ row.item.address }} {{ row.item.zip_code }}
              {{ row.item.city }}
            </span>
          </template>

          <template #cell(created_by)="row">
            <span v-if="row.item.created_by">
              {{ row.item.created_by.full_name }}
            </span>
            <span v-else class="text-muted">
              -
            </span>
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
    </b-card>
  </div>
</template>

<style lang="scss">
.b-table-row-selected {
  font-weight: bold;
}
</style>

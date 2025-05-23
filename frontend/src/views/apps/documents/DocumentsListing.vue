<script lang="ts" setup>
import { onBeforeMount, reactive, ref, watch } from 'vue'
import { useDocumentsStore } from '@/stores/apps/Documents'
import { notify, swalAlert } from '@/helpers/notify'
import router from '@/router'
import { DocumentListingModel } from '@/types/documents.types.ts'
import { euro } from '../../../helpers/utils.ts'
import strftime from 'strftime'
import { can } from '@/helpers/permissions.ts'
import DocumentStateBadge from '@/components/document-stage-badge/DocumentStateBadge.vue'
import { DocumentStateBadgeInfo } from '@/helpers/documents.ts'

const documentsStore = useDocumentsStore()
const isListingLoading = ref(false)
const isFiltersUpdateFromQuery = ref(false)
const filters = reactive({
  perPage: 25,
  currentPage: 1,
  search: '',
  sortBy: 'created_at',
  sortDesc: true,
  forme: '',
  state: '',
  startDate: '',
  endDate: ''
})

const getDocuments = async () => {
  isListingLoading.value = true

  try {
    await documentsStore.getDocuments(filters)
  } catch {
    notify(
      'Une erreur est survenue lors du chargement des documents',
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
      sortBy: filters.sortBy,
      sortDesc: filters.sortDesc.toString(),
      forme: filters.forme,
      state: filters.state,
      startDate: filters.startDate,
      endDate: filters.endDate
    }
  })
}

watch(
  [
    () => filters.perPage,
    () => filters.sortBy,
    () => filters.sortDesc,
    () => filters.forme,
    () => filters.state,
    () => filters.startDate,
    () => filters.endDate
  ],
  () => {
    if (!isFiltersUpdateFromQuery.value) {
      filters.currentPage = 1
      getDocuments()
      saveFiltersInQuery()
    } else isFiltersUpdateFromQuery.value = false
  }
)

// Watch only for filters.search to avoid saving in query
watch([() => filters.search], () => {
  if (!isFiltersUpdateFromQuery.value) {
    filters.currentPage = 1
    getDocuments()
  } else isFiltersUpdateFromQuery.value = false
})

watch(
  () => filters.currentPage,
  () => {
    getDocuments()
    saveFiltersInQuery()
  }
)

const rowClicked = (item: DocumentListingModel) => {
  if (item.is_draft) {
    if (!can('access_constructor')) return
    router.push({
      name: 'entreprise-constructor-draft',
      params: {
        documentId: item.id,
        documentNumber: item.document_number
      }
    })
    return
  }

  router.push({
    name: 'entreprise-document-view',
    params: { documentId: item.id, documentNumber: item.document_number }
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
    filters.sortBy = searchParams.get('sortBy') as string
    filters.sortDesc = searchParams.get('sortDesc') === 'true'
    filters.forme = searchParams.get('forme') as string
    filters.state = searchParams.get('state') as string
    filters.startDate = searchParams.get('startDate') as string
    filters.endDate = searchParams.get('endDate') as string

    isFiltersUpdateFromQuery.value = true
  }
  getDocuments()
})

const deleteDocument = async (documentId: number) => {
  const { value } = await swalAlert(
    'Êtes-vous sûr de vouloir supprimer ce document ?'
  )
  if (!value) return

  try {
    await documentsStore.deleteDocument(documentId)
    getDocuments()
  } catch {
    notify(
      'Une erreur est survenue lors de la suppression du document',
      'danger'
    )
  }
}
</script>

<template>
  <div>
    <b-card>
      <b-row>
        <b-col md="3">
          <b-form-group label="Recherche par texte">
            <b-form-input
              v-model="filters.search"
              placeholder="Recherche par mots-clés..."
              debounce="300"
            />
          </b-form-group>
        </b-col>
        <b-col md="3">
          <b-form-group label="Datant dû">
            <flat-pickr
              :config="{
                mode: 'range',
                locale: 'fr',
                dateFormat: 'd/m/Y',
                altInput: true,
                altFormat: 'd/m/Y',
                allowInput: true,
                onChange: function (selectedDates) {
                  if (selectedDates[0]) {
                    filters.startDate = strftime(
                      '%d/%m/%Y',
                      selectedDates[0]
                    )
                  } else {
                    filters.startDate = ''
                  }

                  if (selectedDates[1]) {
                    filters.endDate = strftime(
                      '%d/%m/%Y',
                      selectedDates[1]
                    )
                  } else {
                    filters.endDate = ''
                  }
                }
              }"
              placeholder="Sélectionner une plage de dates"
            />
          </b-form-group>
        </b-col>
        <b-col md="2">
          <b-form-group label="Type de document">
            <v-select
              :options="[
                { label: 'Tous', value: '' },
                { label: 'Facture', value: 'facture' },
                { label: 'Devis', value: 'devis' },
                { label: 'Acompte', value: 'acompte' },
                { label: 'Avoir', value: 'avoir' }
              ]"
              v-model="filters.forme"
              :reduce="(option) => option.value"
              :clearable="false"
            />
          </b-form-group>
        </b-col>
        <b-col md="2">
          <b-form-group label="État de document">
            <v-select
              :options="[
                { label: 'Tous', value: '' },
                { label: 'Brouillon', value: 'draft' },
                { label: 'Produit', value: 'produced' },
                { label: 'Devis accepté', value: 'devis_accepted' },
                { label: 'Devis refusé', value: 'devis_refused' },
                { label: 'Devis expiré', value: 'devis_expired' },
                { label: 'Devis facturé', value: 'devis_invoiced' },
                { label: 'Payé', value: 'paid' }
              ]"
              v-model="filters.state"
              :reduce="(option) => option.value"
              :clearable="false"
            />
          </b-form-group>
        </b-col>
        <b-col md="2">
          <b-form-group label="Documents par page">
            <v-select
              :options="[10, 25, 50, 100]"
              v-model="filters.perPage"
              :clearable="false"
            />
          </b-form-group>
        </b-col>
      </b-row>

      <b-overlay :show="isListingLoading">
        <b-table
          hover
          :items="documentsStore.listing.documents"
          :fields="[
            { key: 'document_number', label: 'Numéro', sortable: true },
            {
              key: 'client',
              label: 'Client',
              sortable: false
            },
            { key: 'forme', label: 'Type', sortable: false },
            { key: 'state', label: 'État', sortable: false },
            { key: 'subject', label: 'Objet', sortable: false },
            { key: 'total_ht', label: 'Total HT', sortable: true },
            { key: 'created_at', label: 'Datant dû', sortable: true },
            { key: 'actions', label: 'Actions', sortable: false }
          ]"
          v-model:sort-by="filters.sortBy"
          v-model:sort-desc="filters.sortDesc"
          primary-key="id"
          :no-local-sorting="true"
          show-empty
          empty-text="Aucun document trouvé"
          class="position-relative mb-1 mt-50"
          @row-clicked="rowClicked"
        >
          <template #cell(document_number)="row">
            <router-link
              :to="
                row.item.is_draft
                  ? can('access_constructor')
                    ? {
                        name: 'entreprise-constructor-draft',
                        params: {
                          documentId: row.item.id,
                          documentNumber: row.item.document_number
                        }
                      }
                    : null
                  : {
                      name: 'entreprise-document-view',
                      params: {
                        documentId: row.item.id,
                        documentNumber: row.item.document_number
                      }
                    }
              "
              class="font-weight-bolder text-nowrap"
              :class="DocumentStateBadgeInfo[row.item.state].textColor"
            >
              #{{ row.value }}
            </router-link>
          </template>

          <template #cell(client)="row">
            <template v-if="row.value">
              <span
                class="font-weight-bold text-nowrap d-block text-truncate"
                style="max-width: 120px"
              >
                {{ row.value.socialreasonorname }}
              </span>
              <small class="text-muted">{{
                row.value.client_number
              }}</small>
            </template>
            <span v-else class="font-weight-bold"> Pas de client </span>
          </template>

          <template #cell(forme)="row">
            <span class="text-capitalize">
              {{ row.value }}
            </span>
          </template>

          <template #cell(state)="row">
            <document-state-badge :state="row.value" />
          </template>

          <template #cell(subject)="row">
            <span style="max-width: 100px" class="truncate-text-ellipsis">
              {{ row.value }}
            </span>
          </template>

          <template #cell(total_ht)="row">
            <span class="text-capitalize text-nowrap">
              {{ euro(row.value).format() }} €
            </span>
          </template>

          <template #cell(created_at)="row">
            <span>
              {{ strftime('%d/%m/%Y', new Date(row.value)) }}
            </span>
          </template>

          <template #cell(actions)="row">
            <div
              v-if="row.item.is_draft"
              class="d-flex justify-content-center"
            >
              <b-button
                class="btn-icon"
                variant="flat-danger"
                @click="deleteDocument(row.item.id)"
              >
                <vue-feather type="trash" size="18" />
              </b-button>
            </div>
            <div v-else class="text-nowrap">
              <b-button class="btn-icon" variant="flat-secondary">
                <vue-feather type="printer" size="18" />
              </b-button>

              <a
                download
                v-ripple
                class="btn btn-flat-secondary btn-icon"
                target="_blank"
                :href="row.item.file"
              >
                <vue-feather type="download" size="18" />
              </a>
            </div>
          </template>
        </b-table>
      </b-overlay>
      <div class="d-flex align-items-center justify-content-center">
        <b-pagination
          v-model="filters.currentPage"
          :total-rows="documentsStore.listing.total"
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

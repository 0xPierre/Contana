import { defineStore, acceptHMRUpdate } from 'pinia'
import http from '@/helpers/http'
import type {
  ClientConstructor,
  ClientCreationForm,
  ClientModel
} from '@/types/clients.types'
import type { ApiPaginatedResponse, ApiResponse } from '@/types/api.types'
import { useEntrepriseStore } from './Entreprise'

interface State {
  listing: {
    clients: ClientModel[]
    lastPage: number
    total: number
  }
}

export const useClientsStore = defineStore('clients', {
  state: (): State => {
    return {
      listing: {
        clients: [],
        lastPage: 0,
        total: 0
      }
    }
  },

  getters: {},

  actions: {
    async createClient(data: ClientCreationForm | ClientConstructor) {
      const entrepriseStore = useEntrepriseStore()

      return http.post<ApiResponse<ClientModel>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/clients/`,
        data
      )
    },

    async getClients(filters: {
      currentPage: number
      perPage: number
      search: string
      archived: boolean
      sortBy: string
      sortDesc: boolean
    }) {
      const entrepriseStore = useEntrepriseStore()

      const { data } = await http.get<ApiPaginatedResponse<ClientModel>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/clients/`,
        {
          params: {
            page: filters.currentPage,
            page_size: filters.perPage,
            search: filters.search,
            archived: filters.archived,
            sort_by: filters.sortBy,
            sort_desc: filters.sortDesc
          }
        }
      )

      this.listing.clients = data.results
      this.listing.lastPage = data.count / filters.perPage
      this.listing.total = data.count
    },

    async getClient(clientId: string | number) {
      const entrepriseStore = useEntrepriseStore()

      return await http.get<ApiResponse<ClientModel>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/clients/${clientId}/`
      )
    },

    async updateClient(client: Partial<ClientModel>) {
      const entrepriseStore = useEntrepriseStore()

      return http.put<ApiResponse<null>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/clients/${client.id}/`,
        client
      )
    },

    async saveClientFiles(
      clientId: number,
      files: (File | { id: number; url: string })[]
    ) {
      const formData = new FormData()
      files.forEach((file) => {
        if (file instanceof File) {
          formData.append('files', file)
        } else {
          formData.append('files_id', file.id.toString())
        }
      })

      const entrepriseStore = useEntrepriseStore()

      return http.post<ApiResponse<null>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/clients/${clientId}/files/`,
        formData
      )
    },

    async archiveClient(client: ClientModel) {
      const entrepriseStore = useEntrepriseStore()

      return http.post<ApiResponse<null>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/clients/${client.id}/archive/`
      )
    },

    async unarchiveClient(client: ClientModel) {
      const entrepriseStore = useEntrepriseStore()

      return http.post<ApiResponse<null>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/clients/${client.id}/unarchive/`
      )
    }
  },

  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useClientsStore, import.meta.hot))
}

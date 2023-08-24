import { defineStore, acceptHMRUpdate } from 'pinia'
import http from '@/helpers/http'
import type { ApiPaginatedResponse, ApiResponse } from '@/types/api.types'
import { useEntrepriseStore } from './Entreprise'
import {
  DocumentListingModel,
  DocumentModel
} from '@/types/documents.types.ts'

interface State {
  listing: {
    documents: DocumentListingModel[]
    lastPage: number
    total: number
  }
}

export const useDocumentsStore = defineStore('documents', {
  state: (): State => {
    return {
      listing: {
        documents: [],
        lastPage: 0,
        total: 0
      }
    }
  },

  getters: {},

  actions: {
    async getDocuments(filters: {
      currentPage: number
      perPage: number
      search: string
      sortBy: string
      sortDesc: boolean
      forme: string
      startDate: string
      endDate: string
    }) {
      const entrepriseStore = useEntrepriseStore()

      const { data } = await http.get<
        ApiPaginatedResponse<DocumentListingModel>
      >(`/api/entreprise/${entrepriseStore.entreprise?.slug}/documents/`, {
        params: {
          page: filters.currentPage,
          page_size: filters.perPage,
          search: filters.search,
          sort_by: filters.sortBy,
          sort_desc: filters.sortDesc,
          start_date: filters.startDate,
          end_date: filters.endDate,
          forme: filters.forme
        }
      })

      this.listing.documents = data.results
      this.listing.lastPage = data.count / filters.perPage
      this.listing.total = data.count
    },

    async getDocument(documentId: string | number) {
      const entrepriseStore = useEntrepriseStore()

      return await http.get<ApiResponse<DocumentModel>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/documents/${documentId}/`
      )
    }
  },

  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useDocumentsStore, import.meta.hot)
  )
}

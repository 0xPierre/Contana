import { defineStore, acceptHMRUpdate } from 'pinia'
import http from '@/helpers/http'
import type {
  EntrepriseModel,
  EntrepriseSettingsInformations,
  EntrepriseUser,
  ApplicationToken
} from '@/types/entreprise.types'
import type { ApiResponse } from '@/types/api.types'
import { PaymentsMethod } from '@/types/core.types.ts'

interface State {
  selectedEntrepriseSlug: string | null
  entreprise: EntrepriseModel | null
}

export const useEntrepriseStore = defineStore('entreprise', {
  state: (): State => {
    return {
      selectedEntrepriseSlug: null,
      entreprise: null
    }
  },

  getters: {
    usersWithoutOwner: (state) => {
      return (
        state.entreprise?.users.filter(
          (user) => user.id !== state.entreprise?.owner
        ) || []
      )
    },

    isPaymentStatusOk: (state) => {
      return state.entreprise?.stripe_payment_status === 'paid'
    }
  },

  actions: {
    async getEntrepriseData() {
      const { data } = await http.post<ApiResponse<EntrepriseModel>>(
        `/api/entreprise/${this.selectedEntrepriseSlug}/data`
      )

      this.entreprise = data.data
    },

    async updateEntrepriseInformations(
      data: EntrepriseSettingsInformations
    ) {
      return http.post<ApiResponse<EntrepriseModel>>(
        `/api/entreprise/${this.entreprise?.slug}/settings/informations`,
        data
      )
    },
    async updateEntrepriseDocumentsPersonnalization(data: {
      document_logo_size: number
      document_logo_margin_right: number
      document_logo_margin_top: number
      document_logo_margin_bottom: number
      document_logo_used: null | number
      document_default_payment_method: PaymentsMethod
      document_payment_mention: string
      document_other_mention: string
      document_notes: string
      vat_payer: boolean
    }) {
      return http.post<ApiResponse<EntrepriseModel>>(
        `/api/entreprise/${this.entreprise?.slug}/settings/informations/personnalization/documents`,
        data
      )
    },

    async getPersonnalizationDocumentPreview(data: {
      document_logo_size: number
      document_logo_margin_right: number
      document_logo_margin_top: number
      document_logo_margin_bottom: number
      document_logo_used: null | number
      document_default_payment_method: PaymentsMethod
      document_payment_mention: string
      document_other_mention: string
      document_notes: string
      vat_payer: boolean
    }) {
      return http.post<Blob>(
        `/api/entreprise/${this.entreprise?.slug}/settings/informations/personnalization/documents/preview`,
        data,
        {
          responseType: 'blob'
        }
      )
    },

    async updateEntrepriseLogos(
      logos: (File | { id: number; url: string })[]
    ) {
      const formData = new FormData()
      logos.forEach((logo) => {
        if (logo instanceof File) {
          formData.append('logos', logo)
        } else {
          formData.append('logos_id', logo.id.toString())
        }
      })

      return http.post<ApiResponse<EntrepriseModel>>(
        `/api/entreprise/${this.entreprise?.slug}/settings/logos`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )
    },

    async updateUserPermissions(user: EntrepriseUser) {
      return http.post<ApiResponse<EntrepriseModel>>(
        `/api/entreprise/${this.entreprise?.slug}/settings/user/${user.id}/permissions`,
        {
          permissions: user.permissions
        }
      )
    },

    async removeUser(user: EntrepriseUser) {
      return http.post<ApiResponse<{ users: EntrepriseUser[] }>>(
        `/api/entreprise/${this.entreprise?.slug}/settings/user/${user.id}/remove`
      )
    },

    async createInvitationLink() {
      return http.post<
        ApiResponse<{
          invitation_link: string
          invitation_token: string
        }>
      >(
        `/api/entreprise/${this.entreprise?.slug}/settings/invitations/create`
      )
    },

    async sendInvitationLinkToUserByEmail(payload: {
      email: string
      invitation_token: string
    }) {
      return http.post<ApiResponse>(
        `/api/entreprise/${this.entreprise?.slug}/settings/invitations/send-by-email`,
        payload
      )
    },

    async getInvitationInfo(
      invitation_token: string,
      entreprise_slug: string
    ) {
      return http.post<
        ApiResponse<{
          entreprise_name?: string
          is_valid: boolean
          already_in: boolean
        }>
      >(
        `/api/entreprise/${entreprise_slug}/settings/invitations/get-info`,
        {
          invitation_token
        }
      )
    },

    async joinEntreprise(
      invitation_token: string,
      entreprise_slug: string
    ) {
      return http.post<ApiResponse>(
        `/api/entreprise/${entreprise_slug}/settings/invitations/join`,
        {
          invitation_token
        }
      )
    },

    async deleteEntreprise() {
      return http.post<ApiResponse>(
        `/api/entreprise/${this.entreprise?.slug}/settings/delete`
      )
    },

    async createEntrepriseCheckoutSession(data: {
      name: string
      siren: string
      email: string
    }) {
      return http.post<ApiResponse<{ url: string }>>(
        `/api/entreprise/create-checkout-session`,
        data
      )
    },

    async createCustomerPortal() {
      return http.post<ApiResponse<{ url: string }>>(
        `/api/entreprise/${this.entreprise?.slug}/settings/customer-portal/create`
      )
    },

    async getApplicationTokens(): Promise<ApplicationToken[]> {
      const { data } = await http.get<ApplicationToken[]>(
        `/token/application/`,
        {
          params: {
            entreprise_slug: this.entreprise?.slug
          }
        }
      )
      return data
    },

    async createApplicationToken(name?: string): Promise<ApplicationToken> {
      const { data } = await http.post<ApplicationToken>(
        `/token/application/`,
        name ? { name } : {},
        {
          params: {
            entreprise_slug: this.entreprise?.slug
          }
        }
      )
      return data
    },

    async updateApplicationToken(tokenKey: string, name: string): Promise<ApplicationToken> {
      const { data } = await http.patch<ApplicationToken>(
        `/token/application/${tokenKey}/`,
        { name },
        {
          params: {
            entreprise_slug: this.entreprise?.slug
          }
        }
      )
      return data
    },

    async deleteApplicationToken(tokenKey: string) {
      return http.delete<ApiResponse>(
        `/token/application/${tokenKey}/`,
        {
          params: {
            entreprise_slug: this.entreprise?.slug
          }
        }
      )
    }
  },

  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useEntrepriseStore, import.meta.hot)
  )
}

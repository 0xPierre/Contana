import { defineStore, acceptHMRUpdate } from 'pinia'
import http from '@/helpers/http'
import type {
  UserRegistration,
  UserModel,
  UserLogin
} from '@/types/user.types'
import { useRouter } from 'vue-router'
import type { ApiResponse } from '@/types/api.types'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'

interface State {
  data: UserModel | null
  auth: {
    access: string
    refresh: string
    isLoggedIn: boolean
  }
}

export const useUserStore = defineStore('user', {
  state: (): State => {
    return {
      data: null,
      auth: {
        access: '',
        refresh: '',
        isLoggedIn: false
      }
    }
  },

  getters: {},

  actions: {
    async register(data: UserRegistration) {
      return http.post<
        ApiResponse<{
          user: UserModel
          auth: {
            access: string
            refresh: string
          }
        }>
      >('/api/user/registration', data)
    },

    async logIn(data: UserLogin) {
      return http.post<
        ApiResponse<{
          user: UserModel
          auth: {
            access: string
            refresh: string
          }
        }>
      >('/api/user/login', data)
    },

    async refreshToken() {
      const { data } = await http.post<{ access: string }>(
        '/api/user/refresh',
        {
          refresh: this.auth.refresh
        }
      )

      if (data.access) {
        this.auth.access = data.access
        return data.access
      } else {
        this.auth.access = ''
        this.auth.refresh = ''
        this.auth.isLoggedIn = false
        const router = useRouter()
        router.push({
          name: 'login'
        })

        return null
      }
    },

    async logOut() {
      http.post<ApiResponse<null>>('/api/user/logout', {
        refresh: this.auth.refresh
      })
      this.auth.access = ''
      this.auth.refresh = ''
      this.auth.isLoggedIn = false
    },

    async resetPasswordRequest(email: string) {
      return http.post<ApiResponse<null>>(
        '/api/user/password-reset-request',
        {
          email
        }
      )
    },

    async resetPassword(data: {
      token: string
      password: string
      password_confirmation: string
    }) {
      return http.post<ApiResponse<null>>('/api/user/password-reset', data)
    },

    async updateProfil(data: FormData) {
      return http.post<
        ApiResponse<{
          user: UserModel
        }>
      >('/api/user/update-profile', data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    },

    async updatePassword(data: {
      current_password: string
      new_password: string
      password_confirmation: string
    }) {
      return http.post<ApiResponse<null>>(
        '/api/user/update-password',
        data
      )
    },

    async selectEntreprise(entrepriseSlug: string) {
      const entrepriseStore = useEntrepriseStore()
      entrepriseStore.selectedEntrepriseSlug = entrepriseSlug
      return entrepriseStore.getEntrepriseData()
    },

    async getData() {
      const { data } = await http.get<
        ApiResponse<{
          user: UserModel
        }>
      >('/api/user/data')

      this.data = data.data.user

      const entrepriseStore = useEntrepriseStore()
      if (this.data.entreprises.length > 0) {
        this.selectEntreprise(this.data.entreprises[0].slug)
      } else {
        entrepriseStore.selectedEntrepriseSlug = null
        entrepriseStore.entreprise = null
      }
    }
  },

  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot))
}

import { defineStore, acceptHMRUpdate } from 'pinia'
import http from '@/helpers/http'
import type { ApiResponse } from '@/types/api.types'
import { useEntrepriseStore } from './Entreprise'
import { notify } from '@/helpers/notify.ts'

interface State {
  period:
    | 'week'
    | 'last_week'
    | 'month'
    | 'last_month'
    | 'year'
    | 'last_year'
    | 'all'
    | 'custom'
  startDate: string
  endDate: string

  cardsData: {
    isLoading: boolean
    data: {
      turnover: number
      cash_collection: number
      outstanding_quotations: number
      outstanding_client_amount: number
    }
  }

  turnoverChart: {
    isLoading: boolean
    data: {
      labels: string[]
      series: { name: ''; data: number[] }[]
    }
  }

  bestArticlesChart: {
    isLoading: boolean
    data: {
      labels: string[]
      serie: number[]
    }
  }

  bestClientsChart: {
    isLoading: boolean
    data: {
      labels: string[]
      serie: number[]
    }
  }
}

export const useDashboardStore = defineStore('dashboard', {
  state: (): State => {
    return {
      period: 'week',
      startDate: '',
      endDate: '',

      cardsData: {
        isLoading: false,
        data: {
          turnover: 0,
          cash_collection: 0,
          outstanding_quotations: 0,
          outstanding_client_amount: 0
        }
      },

      turnoverChart: {
        isLoading: false,
        data: {
          labels: [],
          series: []
        }
      },

      bestArticlesChart: {
        isLoading: false,
        data: {
          labels: [],
          serie: []
        }
      },

      bestClientsChart: {
        isLoading: false,
        data: {
          labels: [],
          serie: []
        }
      }
    }
  },

  getters: {},

  actions: {
    async getCardsData() {
      const entrepriseStore = useEntrepriseStore()
      this.cardsData.isLoading = true

      try {
        const { data } = await http.post<
          ApiResponse<{
            turnover: number
            cash_collection: number
            outstanding_quotations: number
            outstanding_client_amount: number
          }>
        >(
          `/api/entreprise/${entrepriseStore.entreprise?.slug}/dashboard/cards-data`,
          {
            period: this.period,
            start_date: this.startDate,
            end_date: this.endDate
          }
        )

        this.cardsData.data = data.data
      } catch {
        notify(
          'Une erreur est survenue lors de la récupération des données des cartes',
          'danger'
        )
      }
      this.cardsData.isLoading = false
    },
    async getTurnover() {
      const entrepriseStore = useEntrepriseStore()

      this.turnoverChart.isLoading = true

      try {
        const { data } = await http.post<
          ApiResponse<{
            labels: string[]
            series: { name: ''; data: number[] }[]
          }>
        >(
          `/api/entreprise/${entrepriseStore.entreprise?.slug}/dashboard/turnover-chart`,
          {
            period: this.period,
            start_date: this.startDate,
            end_date: this.endDate
          }
        )

        this.turnoverChart.data = data.data
      } catch {
        notify(
          "Une erreur est survenue lors de la récupération des données du graphique de chiffre d'affaires",
          'danger'
        )
      }

      this.turnoverChart.isLoading = false
    },

    async getBestArticles() {
      const entrepriseStore = useEntrepriseStore()

      this.bestArticlesChart.isLoading = true

      try {
        const { data } = await http.post<
          ApiResponse<{
            labels: string[]
            serie: number[]
          }>
        >(
          `/api/entreprise/${entrepriseStore.entreprise?.slug}/dashboard/best-articles-chart`,
          {
            period: this.period,
            start_date: this.startDate,
            end_date: this.endDate
          }
        )

        this.bestArticlesChart.data = data.data
      } catch {
        notify(
          'Une erreur est survenue lors de la récupération des données du graphique des meilleurs articles',
          'danger'
        )
      }

      this.bestArticlesChart.isLoading = false
    },

    async getBestClients() {
      const entrepriseStore = useEntrepriseStore()

      this.bestClientsChart.isLoading = true

      try {
        const { data } = await http.post<
          ApiResponse<{
            labels: string[]
            serie: number[]
          }>
        >(
          `/api/entreprise/${entrepriseStore.entreprise?.slug}/dashboard/best-clients-chart`,
          {
            period: this.period,
            start_date: this.startDate,
            end_date: this.endDate
          }
        )

        this.bestClientsChart.data = data.data
      } catch {
        notify(
          'Une erreur est survenue lors de la récupération des données du graphique des meilleurs clients',
          'danger'
        )
      }

      this.bestClientsChart.isLoading = false
    }
  },
  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useDashboardStore, import.meta.hot)
  )
}

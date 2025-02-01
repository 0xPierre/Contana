import { defineStore, acceptHMRUpdate } from 'pinia'
import http from '@/helpers/http'
import type { ApiResponse } from '@/types/api.types'
import { useEntrepriseStore } from './Entreprise'
import { notify } from '@/helpers/notify.ts'

interface PieChart {
  isLoading: boolean
  data: {
    labels: string[]
    serie: number[]
  }
}

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
      signed_quotes: number
      turnover: number
      cash_collection: number
      outstanding_client_amount: number
      discovery_calls: number
      follow_up_calls: number
      new_professional_clients: number
      new_private_customers: number
      clients_to_follow_up: number
      total_outstanding_quotations: string
    }
  }

  turnoverChart: {
    isLoading: boolean
    data: {
      labels: string[]
      series: { name: ''; data: number[] }[]
    }
  }

  bestClientsByQuote: PieChart
  bestUsersByQuote: PieChart
  outstandingQuoteByCommercial: PieChart
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
          signed_quotes: 0,
          turnover: 0,
          cash_collection: 0,
          outstanding_client_amount: 0,
          discovery_calls: 0,
          follow_up_calls: 0,
          new_professional_clients: 0,
          new_private_customers: 0,
          clients_to_follow_up: 0,
          total_outstanding_quotations: ''
        }
      },

      turnoverChart: {
        isLoading: false,
        data: {
          labels: [],
          series: []
        }
      },

      bestClientsByQuote: {
        isLoading: false,
        data: {
          labels: [],
          serie: []
        }
      },

      bestUsersByQuote: {
        isLoading: false,
        data: {
          labels: [],
          serie: []
        }
      },

      outstandingQuoteByCommercial: {
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
          ApiResponse<State['cardsData']['data']>
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

    async getBestClientsBySignedQuote() {
      const entrepriseStore = useEntrepriseStore()

      this.bestClientsByQuote.isLoading = true

      try {
        const { data } = await http.post<
          ApiResponse<{
            labels: string[]
            serie: number[]
          }>
        >(
          `/api/entreprise/${entrepriseStore.entreprise?.slug}/dashboard/best-clients-by-signed-quotes`,
          {
            period: this.period,
            start_date: this.startDate,
            end_date: this.endDate
          }
        )

        this.bestClientsByQuote.data = data.data
      } catch {
        notify(
          'Une erreur est survenue lors de la récupération des données du graphique des meilleurs clients par devis signé',
          'danger'
        )
      }

      this.bestClientsByQuote.isLoading = false
    },
    async getBestUserBySignedQuotes() {
      const entrepriseStore = useEntrepriseStore()

      this.bestUsersByQuote.isLoading = true

      try {
        const { data } = await http.post<
          ApiResponse<{
            labels: string[]
            serie: number[]
          }>
        >(
          `/api/entreprise/${entrepriseStore.entreprise?.slug}/dashboard/best-user-by-signed-quotes`,
          {
            period: this.period,
            start_date: this.startDate,
            end_date: this.endDate
          }
        )

        this.bestUsersByQuote.data = data.data
      } catch {
        notify(
          'Une erreur est survenue lors de la récupération des données du graphique du classement des commerciaux par devis signé',
          'danger'
        )
      }

      this.bestUsersByQuote.isLoading = false
    },
    async getOutstandingQuoteByCommercial() {
      const entrepriseStore = useEntrepriseStore()

      this.outstandingQuoteByCommercial.isLoading = true

      try {
        const { data } = await http.post<
          ApiResponse<{
            labels: string[]
            serie: number[]
          }>
        >(
          `/api/entreprise/${entrepriseStore.entreprise?.slug}/dashboard/outstanding-quote-by-commercial`
        )

        this.outstandingQuoteByCommercial.data = data.data
      } catch (e) {
        notify(
          'Une erreur est survenue lors de la récupération des données du graphique des devis en cours par commercial',
          'danger'
        )
      }

      this.outstandingQuoteByCommercial.isLoading = false
    }
  },
  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useDashboardStore, import.meta.hot)
  )
}

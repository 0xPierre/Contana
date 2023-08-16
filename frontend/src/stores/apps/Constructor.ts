import { defineStore, acceptHMRUpdate } from 'pinia'
import http from '@/helpers/http'
import type { ClientModel } from '@/types/clients.types'
import { DocumentsType, PaymentsMethod } from '@/types/core.types'
import type { ApiPaginatedResponse, ApiResponse } from '@/types/api.types'
import { useEntrepriseStore } from './Entreprise'

interface State {
  client: ClientModel | null
  subject: string
  forme: DocumentsType
  paymentMethod: PaymentsMethod
  validityDate: Date
  paymentMention: string
  notes: string
  vatPayer: boolean
  otherMention: string
}

export const useConstructorStore = defineStore('constructor', {
  state: (): State => {
    return {
      client: null,
      subject: '',
      forme: DocumentsType.Facture,
      paymentMethod: PaymentsMethod.BankTransfer,
      validityDate: new Date(
        new Date().setDate(new Date().getDate() + 90)
      ),
      paymentMention: 'À réception de la facture',
      notes: '',
      vatPayer: false,
      otherMention: ''
    }
  },

  getters: {
    formeSentence: (state) => {
      return {
        first:
          state.forme === DocumentsType.Facture
            ? 'la facture'
            : state.forme === DocumentsType.Devis
            ? 'le devis'
            : "l'acompte",
        second:
          state.forme === DocumentsType.Facture
            ? 'de la facture'
            : state.forme === DocumentsType.Devis
            ? 'du devis'
            : "de l'acompte"
      }
    }
  },

  actions: {},

  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useConstructorStore, import.meta.hot)
  )
}

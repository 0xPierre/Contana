import {
  DocumentsType
  // PaymentsMethod
} from '@/types/core.types.ts'

export enum DocumentsState {
  Draft = 'draft',
  Produced = 'produced',
  DevisAccepted = 'devis_accepted',
  DevisRefused = 'devis_refused',
  DevisExpired = 'devis_expired',
  DevisInvoiced = 'devis_invoiced',
  Paid = 'paid'
}

export interface DocumentListingModel {
  id: number
  document_number: string
  forme: DocumentsType
  client: {
    id: number
    client_number: string
    socialreasonorname: string
  }
  created_at: string
  total_ht: number
  is_draft: boolean
  state: DocumentsState
}

export interface DocumentModel extends DocumentListingModel {
  // subject: string
  // validity_date: Date
  // payment_method: PaymentsMethod
  // payment_mention: string
  // other_mention: string
  // notes: string
  // vat_payer: boolean
  // total_ttc: number
  // total_vat: number
}

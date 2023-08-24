import {
  DocumentsType
  // PaymentsMethod
} from '@/types/core.types.ts'
export interface DocumentListingModel {
  id: number
  document_number: string
  forme: DocumentsType
  client: {
    id: number
    client_number: string
    socialreasonorname: string
  }
  created_at: Date
  total_ht: number
  is_draft: boolean
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

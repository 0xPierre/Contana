import type { Permissions } from './core.types'
import { PaymentsMethod } from './core.types'

export interface EntrepriseListingItem {
  id: number
  name: string
  slug: string
  stripe_payment_status: 'paid' | 'failed' | 'cancelled'
}

export interface EntrepriseSettingsInformations {
  name: string
  email: string
  phone: string

  country: string
  city: string
  zip_code: string
  address: string

  num_rcs: string
  vat_number: string
  iban: string
  bic: string
  bank: string
  ape: string
  forme: string
  siren: string
  capital: string
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
  first_facture_number: number
  first_devis_number: number
  first_acompte_number: number
  first_avoir_number: number
  first_client_number: number
  stripe_payment_status: 'paid' | 'failed' | 'cancelled'
}

export interface EntrepriseUser {
  id: number
  full_name: string
  email: string
  avatar: string
  permissions: Permissions
}

export interface ApplicationToken {
  key: string
  name: string
  created: string
}

export interface EntrepriseModel extends EntrepriseSettingsInformations {
  id: number
  created_at: string
  slug: string
  owner: number
  is_owner: boolean
  users: EntrepriseUser[]
  user_permissions: Permissions
  logos: {
    id: number
    url: string
    name: string
  }[]
}

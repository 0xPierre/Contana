import type { Permissions } from './core.types'

export interface EntrepriseListingItem {
  id: number
  name: string
  slug: string
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
  siret: string
  capital: string
}

export interface EntrepriseUser {
  id: number
  full_name: string
  email: string
  avatar: string
  permissions: Permissions
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
  }[]
}

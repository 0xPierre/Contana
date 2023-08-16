import type { EntrepriseListingItem } from './entreprise.types'

export interface UserRegistration {
  first_name: string
  last_name: string
  email: string
  password: string
  status: boolean
}

export interface UserLogin {
  email: string
  password: string
}

export interface UserModel {
  id: number
  first_name: string
  last_name: string
  email: string
  full_name: string
  avatar: string
  entreprises: EntrepriseListingItem[]
}

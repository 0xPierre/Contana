export type ClientType = 'particulier' | 'professionnel'

export interface ClientCreationForm {
  socialreasonorname: string
  email: string
  phone: string
  country: string
  city: string
  zip_code: string
  address: string
  vat_number: string
  siren: string
  note: string
  type: ClientType
  website: string
}

export interface ClientModel extends ClientCreationForm {
  id: number
  created_at: string
  updated_at: string
  client_number: string
  archived: boolean
  document_count: number
  files: {
    id: number
    url: string
  }[]
}

export interface ClientConstructor {
  id: number
  socialreasonorname: string
  address: string
  city: string
  zip_code: string
  country: string
  client_number: string
}

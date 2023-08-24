export interface Permissions {
  administrate: boolean
  access_documents: boolean
  update_documents: boolean
  access_clients: boolean
  update_clients: boolean
  access_constructor: boolean
}

export enum DocumentsType {
  Facture = 'facture',
  Devis = 'devis',
  Avoir = 'avoir',
  Acompte = 'acompte'
}
export enum PaymentsMethod {
  BankTransfer = 'bank_transfer',
  Check = 'check',
  Cash = 'cash',
  CreditCard = 'credit_card',
  DirectDebit = 'direct_debit',
  Other = 'other'
}

import { DocumentsState } from '@/types/documents.types.ts'

export const DocumentStateBadgeInfo = {
  [DocumentsState.Draft]: {
    color: 'light-secondary',
    textColor: 'text-secondary',
    text: 'Brouillon'
  },
  [DocumentsState.Produced]: {
    color: 'light-primary',
    textColor: 'text-primary',
    text: 'Produit'
  },
  [DocumentsState.DevisAccepted]: {
    color: 'light-success',
    textColor: 'text-success',
    text: 'Devis accepté'
  },
  [DocumentsState.DevisRefused]: {
    color: 'light-danger',
    textColor: 'text-danger',
    text: 'Devis refusé'
  },
  [DocumentsState.DevisExpired]: {
    color: 'light-warning',
    textColor: 'text-warning',
    text: 'Devis expiré'
  },
  [DocumentsState.DevisInvoiced]: {
    color: 'light-info',
    textColor: 'text-info',
    text: 'Devis facturé'
  },
  [DocumentsState.Paid]: {
    color: 'light-dark',
    textColor: 'text-dark',
    text: 'Payé'
  }
}

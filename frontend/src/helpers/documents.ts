import { DocumentsState } from '@/types/documents.types.ts'
import { DocumentsType } from '@/types/core.types.ts'

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

export const DocumentStateText = {
  [DocumentsState.Draft]: 'Brouillon',
  [DocumentsState.Produced]: 'Produit',
  [DocumentsState.DevisAccepted]: 'Devis accepté',
  [DocumentsState.DevisRefused]: 'Devis refusé',
  [DocumentsState.DevisExpired]: 'Devis expiré',
  [DocumentsState.DevisInvoiced]: 'Devis facturé',
  [DocumentsState.Paid]: 'Payé'
}

export const DocumentTypeText = {
  [DocumentsType.Facture]: 'Facture',
  [DocumentsType.Devis]: 'Devis',
  [DocumentsType.Avoir]: 'Avoir',
  [DocumentsType.Acompte]: 'Acompte'
}

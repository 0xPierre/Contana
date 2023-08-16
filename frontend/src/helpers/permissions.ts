import { useEntrepriseStore } from '@/stores/apps/Entreprise'
import type { EntrepriseModel } from '@/types/entreprise.types'

const can = (
  permission: string,
  entreprise: EntrepriseModel | null = null
): boolean => {
  if (!entreprise) entreprise = useEntrepriseStore().entreprise

  if (!entreprise) return false

  if (entreprise.user_permissions) {
    return (entreprise.user_permissions as any)[permission]
  }

  return false
}

export { can }

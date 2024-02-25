<script setup lang="ts">
import { useUserStore } from '@/stores/apps/User.ts'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()

const billingToBeRegularized = computed(() => {
  return userStore.data?.entreprises.filter(
    (entreprise) => entreprise.stripe_payment_status != 'paid'
  )
})

const routeToSettings = (entreprise) => {
  userStore.selectEntreprise(entreprise.slug)
  router.push({
    name: 'entreprise-settings',
    params: { entrepriseSlug: entreprise.slug }
  })
}
</script>

<template>
  <b-alert
    variant="danger"
    class="p-2"
    :show="!userStore.data?.is_billing_ok"
  >
    Un de vos abonnements est suspendu. Merci de régulariser votre
    situation en accédant à votre portail de paiement dans les paramètres
    de l'entreprise.
    <br />
    Liste des entreprises à régulariser :
    <ul>
      <li
        v-for="entreprise in billingToBeRegularized"
        :key="entreprise.id"
        @click="routeToSettings(entreprise)"
        class="cursor-pointer text-primary"
      >
        {{ entreprise.name }}
      </li>
    </ul>
  </b-alert>
</template>

<style scoped lang="scss"></style>

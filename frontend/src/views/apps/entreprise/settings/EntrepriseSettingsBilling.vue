<script setup lang="ts">
import { notify, swalAlert } from '@/helpers/notify'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'
import { useUserStore } from '@/stores/apps/User'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const isLoading = ref(false)
const entrepriseStore = useEntrepriseStore()

const createCustomerPortal = async () => {
  isLoading.value = true

  try {
    const { data } = await entrepriseStore.createCustomerPortal()
    if (data.url) {
      document.location.href = data.url
    }
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}
</script>

<template>
  <div>
    <b-overlay :show="isLoading">
      <b-row>
        <b-col md="6">
          <b-card title="Accès au portail de paiement">
            <p>
              Contana utilise Stripe pour la gestion des paiements. Vous
              pouvez accéder à votre portail pour gérer votre abonnement.
            </p>

            <b-button
              variant="primary"
              class="mt-1"
              v-ripple
              @click="createCustomerPortal"
            >
              Accéder au portail de paiement
            </b-button>
          </b-card>
        </b-col>
      </b-row>
    </b-overlay>
  </div>
</template>

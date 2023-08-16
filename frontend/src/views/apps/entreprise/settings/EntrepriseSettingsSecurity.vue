<script setup lang="ts">
import { notify, swalAlert } from '@/helpers/notify'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'
import { useUserStore } from '@/stores/apps/User'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const isLoading = ref(false)
const entrepriseStore = useEntrepriseStore()
const userStore = useUserStore()
const router = useRouter()

const deleteEntreprise = async () => {
  const { value } = await swalAlert(
    'Attention',
    'warning',
    'Êtes-vous sûr de vouloir supprimer votre entreprise ? Cette action est irréversible.',
    'Oui, supprimer mon entreprise'
  )

  if (value) {
    isLoading.value = true

    try {
      await entrepriseStore.deleteEntreprise()
      notify('Votre entreprise a bien été supprimée', 'success')
      await userStore.getData()
      router.push({ name: 'home' })
    } catch {
      notify('Une erreur est survenue', 'danger')
    }

    isLoading.value = false
  }
}
</script>

<template>
  <div>
    <b-overlay :show="isLoading">
      <b-row>
        <b-col md="6">
          <b-card title="Supprimer votre entreprise">
            <p>
              Vous pouvez supprimer votre entreprise à tout moment.
              Attention cette action est irréversible.
            </p>

            <b-button
              variant="danger"
              class="mt-1"
              v-ripple
              @click="deleteEntreprise"
            >
              Supprimer mon entreprise
            </b-button>
          </b-card>
        </b-col>
      </b-row>
    </b-overlay>
  </div>
</template>

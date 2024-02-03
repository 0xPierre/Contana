<script setup lang="ts">
import Logo from '@/assets/images/logo.png'

import { ref, onMounted } from 'vue'
import { notify, swalAlert } from '@/helpers/notify'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'
import { useUserStore } from '@/stores/apps/User'
import { useRoute, useRouter } from 'vue-router'

const entrepriseStore = useEntrepriseStore()
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()

const isInvitationValid = ref(false)
const entrepriseName = ref('')
const isLoading = ref(false)
const userAlreadyInEntreprise = ref(false)

onMounted(async () => {
  isLoading.value = true
  try {
    const { data } = await entrepriseStore.getInvitationInfo(
      route.params.invitationToken as string,
      route.params.entrepriseSlug as string
    )

    if (data.status === 'success' && data.data.is_valid) {
      isInvitationValid.value = true
      entrepriseName.value = data.data.entreprise_name
      userAlreadyInEntreprise.value = data.data.already_in
    } else {
      isInvitationValid.value = false
    }
  } catch {
    notify('Une erreur est survenue', 'danger')
  }
  isLoading.value = false
})

const joinEntreprise = async () => {
  isLoading.value = true
  try {
    const { data } = await entrepriseStore.joinEntreprise(
      route.params.invitationToken as string,
      route.params.entrepriseSlug as string
    )

    if (data.status === 'success') {
      swalAlert(
        'Bienvenue',
        'success',
        "Vous avez rejoint l'entreprise avec succès !"
      )
      router.push({ name: 'home' })
      userStore.getData()
    } else {
      notify('Une erreur est survenue', 'danger')
    }
  } catch {
    notify('Une erreur est survenue', 'danger')
  }
  isLoading.value = false
}
</script>

<template>
  <b-overlay :show="isLoading">
    <div class="auth-wrapper auth-v1 px-2">
      <div class="auth-inner py-2">
        <b-card class="mb-0">
          <b-link class="brand-logo">
            <b-img :src="Logo" alt="Contana logo" />

            <h2 class="brand-text text-primary ml-1">Contana</h2>
          </b-link>

          <div v-if="userAlreadyInEntreprise">
            <h4 class="mb-2">
              Vous êtes déjà membre de {{ entrepriseName }}
            </h4>

            <b-button
              variant="primary"
              block
              v-ripple
              :to="{ name: 'home' }"
            >
              Accéder à mon espace
            </b-button>
          </div>
          <div v-else-if="isInvitationValid">
            <h4 class="mb-2">
              Vous avez été invité à rejoindre {{ entrepriseName }}
            </h4>

            <b-button
              variant="primary"
              block
              v-ripple
              @click="joinEntreprise"
            >
              Accepter l'invitation
            </b-button>
          </div>

          <div v-else>
            <h4 class="mb-2">Invitation invalide ou expirée</h4>
          </div>
        </b-card>
      </div>
    </div>
  </b-overlay>
</template>

<style lang="scss">
@import '@/assets/scss/template/vue/pages/page-auth.scss';
</style>

<script setup lang="ts">
import { useFormValidation } from '@/composables/formValidation'
import { required, email } from '@vuelidate/validators'
import Logo from '@/assets/images/logo.png'
import { notify } from '@/helpers/notify'
import { ref } from 'vue'
import { useUserStore } from '@/stores/apps/User'

const { formState, v$ } = useFormValidation(
  {
    email: ''
  },
  {
    email: { required, email }
  }
)

const isLoading = ref(false)
const userStore = useUserStore()
const requestSent = ref(false)

const submitForm = async () => {
  const validated = await v$.value.$validate()
  if (!validated) return

  isLoading.value = true

  try {
    const { data } = await userStore.resetPasswordRequest(formState.email)
    if (data.status === 'failed') {
      notify(data.error, 'danger')
    } else {
      requestSent.value = true
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

          <div v-if="!requestSent">
            <b-card-title class="mb-1">
              Mot de passe oublié ?
            </b-card-title>
            <b-card-text class="mb-2">
              Entrez votre adresse email et nous vous enverrons un lien
              pour réinitialiser votre mot de passe.
            </b-card-text>

            <b-form
              class="auth-forgot-password-form mt-2"
              @submit.prevent="submitForm"
            >
              <b-form-group label="Adresse email">
                <b-form-input
                  v-model="formState.email"
                  placeholder="john@example.com"
                />
                <small
                  v-show="v$.email.$errors.length > 0"
                  class="text-danger"
                >
                  Adresse email invalide
                </small>
              </b-form-group>

              <b-button type="submit" variant="primary" block v-ripple>
                Envoyer le lien
              </b-button>
            </b-form>

            <b-card-text class="mt-2">
              <b-link
                :to="{ name: 'login' }"
                class="d-flex align-items-center justify-content-center"
              >
                <vue-feather type="chevron-left" /> Se connecter
              </b-link>
            </b-card-text>
          </div>
          <div v-else>
            <b-card-text class="mb-2">
              Un email contenant un lien de réinitialisation de mot de
              passe vous a été envoyé.
            </b-card-text>

            <b-card-text>
              Si vous ne recevez pas l'email dans quelques minutes,
              vérifiez votre dossier de courrier indésirable.
            </b-card-text>

            <b-card-text class="mt-2">
              <b-link
                :to="{ name: 'login' }"
                class="d-flex align-items-center justify-content-center"
              >
                <vue-feather type="chevron-left" /> Se connecter
              </b-link>
            </b-card-text>
          </div>
        </b-card>
      </div>
    </div>
  </b-overlay>
</template>

<style lang="scss">
@import '@/assets/scss/template/vue/pages/page-auth.scss';
</style>

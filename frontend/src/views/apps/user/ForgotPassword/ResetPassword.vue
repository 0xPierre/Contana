<script lang="ts" setup>
import { useFormValidation } from '@/composables/formValidation'
import { required, minLength } from '@vuelidate/validators'
import Logo from '@/assets/images/logo.png'
import { notify } from '@/helpers/notify'
import { ref } from 'vue'
import { useUserStore } from '@/stores/apps/User'
import { useRouter, useRoute } from 'vue-router'
import { usePasswordVisibility } from '@/composables/passwordVisiblity'

const { formState, v$ } = useFormValidation(
  {
    password: '',
    password_confirmation: ''
  },
  {
    password: { required, minLength: minLength(8) },
    password_confirmation: { required, minLength: minLength(8) }
  }
)

const { passwordFieldType, togglePasswordVisibility, passwordIcon } =
  usePasswordVisibility()

const {
  passwordFieldType: passwordFieldType2,
  togglePasswordVisibility: togglePasswordVisibility2,
  passwordIcon: passwordIcon2
} = usePasswordVisibility()

const isLoading = ref(false)
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const token = route.query.token as string

if (!token) {
  notify('Token invalide', 'danger')
  router.push({ name: 'login' })
}

const submitForm = async () => {
  const validated = await v$.value.$validate()
  if (!validated) return

  isLoading.value = true

  try {
    const { data } = await userStore.resetPassword({
      token,
      password: formState.password,
      password_confirmation: formState.password_confirmation
    })

    if (data.status === 'failed') {
      notify(data.error, 'danger')
    } else {
      notify(
        'Mot de passe réinitialisé',
        'success',
        'Vous pouvez maintenant vous connecter avec votre nouveau mot de passe.'
      )
      router.push({ name: 'login' })
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

          <b-card-title class="mb-1">
            Réinitialiser votre mot de passe
          </b-card-title>
          <b-card-text class="mb-2">
            Veuillez saisir votre nouveau mot de passe.
          </b-card-text>

          <b-form
            method="POST"
            class="auth-reset-password-form mt-2"
            @submit.prevent="submitForm"
          >
            <b-form-group label="Nouveau mot de passe">
              <b-input-group class="input-group-merge">
                <b-form-input
                  v-model="formState.password"
                  :type="passwordFieldType"
                  class="form-control-merge"
                  placeholder="············"
                />
                <b-input-group-append
                  is-text
                  @click="togglePasswordVisibility"
                >
                  <vue-feather
                    class="cursor-pointer"
                    :type="passwordIcon"
                  />
                </b-input-group-append>
              </b-input-group>
              <small
                v-show="v$.password.$errors.length > 0"
                class="text-danger"
              >
                Votre mot de passe doit contenir au moins 8 caractères.
              </small>
            </b-form-group>

            <b-form-group label="Confirmer le mot de passe">
              <b-input-group class="input-group-merge">
                <b-form-input
                  v-model="formState.password_confirmation"
                  :type="passwordFieldType2"
                  class="form-control-merge"
                  placeholder="············"
                />
                <b-input-group-append
                  is-text
                  @click="togglePasswordVisibility2"
                >
                  <vue-feather
                    class="cursor-pointer"
                    :type="passwordIcon2"
                  />
                </b-input-group-append>
              </b-input-group>
              <small
                v-show="v$.password_confirmation.$errors.length > 0"
                class="text-danger"
              >
                Votre mot de passe doit contenir au moins 8 caractères.
              </small>
            </b-form-group>

            <b-button block type="submit" variant="primary" v-ripple>
              Modifier mon mot de passe
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
        </b-card>
      </div>
    </div>
  </b-overlay>
</template>

<style lang="scss">
@import '@/assets/scss/template/vue/pages/page-auth.scss';
</style>

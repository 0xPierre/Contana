<script setup lang="ts">
import { ref } from 'vue'
import { useFormValidation } from '@/composables/formValidation'
import { required } from '@vuelidate/validators'

import createEntrepriseSvg from '@/assets/svg/entreprise/createEntreprise.svg'
import Logo from '@/assets/images/logo.png'
import { notify, notifyApiError } from '@/helpers/notify'
import { useRouter, useRoute } from 'vue-router'
import { useEntrepriseStore } from '@/stores/apps/Entreprise.ts'
import { useUserStore } from '@/stores/apps/User.ts'

const entrepriseStore = useEntrepriseStore()
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
const isLoading = ref(false)

const { formState, v$ } = useFormValidation<{
  name: string
  siren: string
  email: string
}>(
  {
    name: '',
    siren: '',
    email: ''
  },
  {
    name: { required },
    siren: { required },
    email: { required }
  }
)

const createEntreprise = async () => {
  const validated = await v$.value.$validate()
  if (!validated) return

  isLoading.value = true

  try {
    const { data } = await entrepriseStore.createEntreprise(formState)

    if (data.status === 'success') {
      await userStore.getData()
      notify(
        'Entreprise créée avec succès',
        'success',
        'Vous pouvez maintenant personnaliser votre entreprise'
      )
      await userStore.selectEntreprise(data.data.slug)
      await router.push({
        name: 'entreprise-settings',
        params: { entrepriseSlug: data.data.slug }
      })
    } else {
      if (data.errors) {
        notifyApiError(data.errors)
      }
    }
  } catch (error: unknown) {
    notify('Une erreur est survenue', 'danger')
  }
  isLoading.value = false
}
</script>

<template>
  <b-overlay :show="isLoading">
    <div class="auth-wrapper auth-v2">
      <b-row class="auth-inner m-0">
        <b-link :to="{ name: 'home' }" class="brand-logo">
          <b-img :src="Logo" alt="Contana logo" />

          <h2 class="brand-text text-primary ml-1">Contana</h2>
        </b-link>

        <b-col
          lg="4"
          class="d-flex align-items-center auth-bg px-2 p-lg-5"
        >
          <b-col sm="8" md="6" lg="12" class="px-xl-2 mx-auto">
            <b-card-title title-tag="h2" class="font-weight-bold mb-1">
              Créer votre entreprise
            </b-card-title>
            <b-card-text class="mb-2">
              Créer votre entreprise gratuitement, personnalisez là et
              commencez à facturer vos clients dès maintenant.
            </b-card-text>
            <div class="auth-register-form mt-2">
              <b-form @submit.prevent="createEntreprise">
                <b-form-group label="Nom de l'entreprise">
                  <b-form-input
                    v-model="formState.name"
                    placeholder="Dupond Technologies"
                  />
                  <small
                    v-show="v$.name.$errors.length > 0"
                    class="text-danger"
                  >
                    Nom requis
                  </small>
                </b-form-group>

                <b-form-group label="Siren">
                  <b-form-input
                    v-model="formState.siren"
                    placeholder="123456789"
                  />
                  <small
                    v-show="v$.siren.$errors.length > 0"
                    class="text-danger"
                  >
                    Siren requis
                  </small>
                </b-form-group>

                <b-form-group label="Adresse email de l'entreprise">
                  <b-form-input
                    v-model="formState.email"
                    placeholder="contact@dupond.com"
                  />
                  <small
                    v-show="v$.email.$errors.length > 0"
                    class="text-danger"
                  >
                    Adresse email requise
                  </small>
                </b-form-group>

                <b-button variant="primary" block type="submit" v-ripple>
                  Créer l'entreprise
                </b-button>
              </b-form>
            </div>
          </b-col>
        </b-col>
        <b-col lg="8" class="d-none d-lg-flex align-items-center">
          <div
            class="w-100 d-lg-flex align-items-center justify-content-center px-5"
          >
            <b-img fluid :src="createEntrepriseSvg" />
          </div>
        </b-col>
      </b-row>
    </div>
  </b-overlay>
</template>

<style lang="scss">
@import '@/assets/scss/template/vue/pages/page-auth.scss';
</style>

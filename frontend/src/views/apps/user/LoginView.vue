<script setup lang="ts">
import { ref } from 'vue'
import { useFormValidation } from '@/composables/formValidation'
import { required } from '@vuelidate/validators'
import { usePasswordVisibility } from '@/composables/passwordVisiblity'

import registerSvg from '@/assets/svg/register/register.svg'
import Logo from '@/assets/images/logo.png'
import { useUserStore } from '@/stores/apps/User'
import type { UserLogin } from '@/types/user.types'
import { notify } from '@/helpers/notify'
import { useRouter, useRoute } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
const isLoading = ref(false)

const { formState, v$ } = useFormValidation<UserLogin>(
  {
    email: '',
    password: ''
  },
  {
    email: { required },
    password: { required }
  }
)

const { passwordFieldType, togglePasswordVisibility, passwordIcon } =
  usePasswordVisibility()

const logIn = async () => {
  const validated = await v$.value.$validate()
  if (!validated) return

  isLoading.value = true

  try {
    const { data } = await userStore.logIn(formState)

    if (data.status === 'success') {
      userStore.$patch({
        data: data.data.user,
        auth: {
          ...data.data.auth,
          isLoggedIn: true
        }
      })

      if (route.query.redirect) router.push(route.query.redirect as string)
      else router.push({ name: 'home' })
    } else {
      if (data.error) notify(data.error, 'danger')
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
        <b-link to="/" class="brand-logo">
          <b-img :src="Logo" alt="Contana logo" />

          <h2 class="brand-text text-primary ml-1">Contana</h2>
        </b-link>

        <b-col lg="8" class="d-none d-lg-flex align-items-center p-5">
          <div
            class="w-100 d-lg-flex align-items-center justify-content-center px-5"
          >
            <b-img fluid :src="registerSvg" />
          </div>
        </b-col>

        <b-col
          lg="4"
          class="d-flex align-items-center auth-bg px-2 p-lg-5"
        >
          <b-col sm="8" md="6" lg="12" class="px-xl-2 mx-auto">
            <b-card-title title-tag="h2" class="font-weight-bold mb-1">
              Connexion à votre espace
            </b-card-title>
            <b-card-text class="mb-2">
              Connecter vous à votre espace pour accéder à Contana
            </b-card-text>

            <div class="auth-register-form mt-2">
              <b-form @submit.prevent="logIn">
                <b-form-group label="Adresse email">
                  <b-form-input
                    v-model="formState.email"
                    placeholder="john@example.com"
                  />
                  <small
                    v-show="v$.email.$errors.length > 0"
                    class="text-danger"
                  >
                    Adresse email requise
                  </small>
                </b-form-group>

                <b-form-group
                  label-for="register-password"
                  label="Mot de passe"
                >
                  <b-input-group class="input-group-merge">
                    <b-form-input
                      id="register-password"
                      v-model="formState.password"
                      class="form-control-merge"
                      :type="passwordFieldType"
                      name="register-password"
                      placeholder="············"
                    />
                    <b-input-group-append is-text>
                      <span @click="togglePasswordVisibility">
                        <vue-feather
                          :type="passwordIcon"
                          class="cursor-pointer"
                        />
                      </span>
                    </b-input-group-append>
                  </b-input-group>
                  <small
                    v-show="v$.password.$errors.length > 0"
                    class="text-danger"
                  >
                    Mot de passe requis
                  </small>
                </b-form-group>

                <b-button variant="primary" block type="submit" v-ripple>
                  Connexion
                </b-button>
              </b-form>
            </div>

            <p class="text-center mt-2 mb-50">
              <span> Vous n'avez pas de compte ? </span>
              <b-link
                :to="{
                  name: 'signup',
                  query: {
                    redirect: $route.query.redirect
                  }
                }"
              >
                <span>&nbsp;Créer un compte</span>
              </b-link>
            </p>
            <p class="text-center">
              <b-link :to="{ name: 'forgot-password' }">
                <span> Mot de passe oublié ? </span>
              </b-link>
            </p>
          </b-col>
        </b-col>
      </b-row>
    </div>
  </b-overlay>
</template>

<style lang="scss">
@import '@/assets/scss/template/vue/pages/page-auth.scss';
</style>

<script setup lang="ts">
import { ref } from 'vue'
import { useFormValidation } from '@/composables/formValidation'
import { required, email, minLength } from '@vuelidate/validators'
import { usePasswordVisibility } from '@/composables/passwordVisiblity'
import { notifyApiError } from '@/helpers/notify'

import registerSvg from '@/assets/svg/register/register-2.svg'
import Logo from '@/assets/images/logo.png'
import { useUserStore } from '@/stores/apps/User'
import type { UserRegistration } from '@/types/user.types'
import { notify } from '@/helpers/notify'
import { useRouter, useRoute } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
const isLoading = ref(false)

const { formState, v$ } = useFormValidation<UserRegistration>(
  {
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    status: false
  },
  {
    first_name: { required },
    last_name: { required },
    email: { required, email },
    password: { required, minLength: minLength(8) },
    status: { mustBeTrue: (value: boolean) => value === true }
  }
)

const { passwordFieldType, togglePasswordVisibility, passwordIcon } =
  usePasswordVisibility()

const createAccount = async () => {
  const validated = await v$.value.$validate()
  if (!validated) return

  isLoading.value = true

  try {
    const { data } = await userStore.register(formState)

    if (data.status === 'success') {
      notify(
        'Compte créé avec succès !',
        'success',
        'Bienvenue sur Contana !'
      )

      userStore.$patch({
        data: data.data.user,
        auth: {
          ...data.data.auth,
          isLoggedIn: true
        }
      })
      await userStore.getData()

      if (route.query.redirect) {
        await router.push(route.query.redirect as string)
      } else {
        await router.push({ name: 'home' })
      }
    } else {
      notifyApiError(data.errors)
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
              La gestion de votre entreprise commence ici
            </b-card-title>
            <b-card-text class="mb-2">
              Créez un compte pour commencer à gérer votre entreprise avec
              Contana.
            </b-card-text>

            <div class="auth-register-form mt-2">
              <b-form @submit.prevent="createAccount">
                <b-row>
                  <b-col xl="6">
                    <b-form-group label="Prénom">
                      <b-form-input
                        v-model="formState.first_name"
                        name="register-username"
                        placeholder="John"
                      />
                      <small
                        v-show="v$.first_name.$errors.length > 0"
                        class="text-danger"
                      >
                        Prénom requis
                      </small>
                    </b-form-group>
                  </b-col>

                  <b-col xl="6">
                    <b-form-group label="Nom">
                      <b-form-input
                        v-model="formState.last_name"
                        name="register-username"
                        placeholder="Doe"
                      />
                      <small
                        v-show="v$.last_name.$errors.length > 0"
                        class="text-danger"
                      >
                        Nom requis
                      </small>
                    </b-form-group>
                  </b-col>
                </b-row>

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
                    Votre mot de passe doit contenir minimum 8 charactères
                  </small>
                </b-form-group>

                <b-form-group>
                  <b-form-checkbox
                    id="register-privacy-policy"
                    v-model="formState.status"
                    name="checkbox-1"
                  >
                    J'accepte les
                    <b-link :to="{ name: 'cgu' }">
                      <span>termes et conditions</span>
                    </b-link>
                  </b-form-checkbox>
                  <small
                    v-show="v$.status.$errors.length > 0"
                    class="text-danger"
                  >
                    Vous devez accepter les termes et conditions
                  </small>
                </b-form-group>

                <b-button variant="primary" block type="submit" v-ripple>
                  Créer mon compte
                </b-button>
              </b-form>
            </div>

            <p class="text-center mt-2">
              <span>Vous avez déjà un compte ?</span>
              <b-link
                :to="{
                  name: 'login',
                  query: {
                    redirect: route.query.redirect
                  }
                }"
              >
                <span>&nbsp;Connectez vous</span>
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

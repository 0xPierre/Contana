<script lang="ts" setup>
import { ref } from 'vue'
import { notify, notifyApiError } from '@/helpers/notify'
import { useUserStore } from '@/stores/apps/User'
import { useFormValidation } from '@/composables/formValidation'
import { required, minLength } from '@vuelidate/validators'
import { usePasswordVisibility } from '@/composables/passwordVisiblity'

const userStore = useUserStore()
const isLoading = ref(false)

const { formState, v$, reset } = useFormValidation(
  {
    current_password: '',
    new_password: '',
    password_confirmation: ''
  },
  {
    current_password: {
      required
    },
    new_password: {
      required,
      minLength: minLength(8)
    }
  }
)

const { passwordFieldType, togglePasswordVisibility, passwordIcon } =
  usePasswordVisibility()
const {
  passwordFieldType: passwordFieldTypeNew,
  togglePasswordVisibility: togglePasswordVisibilityNew,
  passwordIcon: passwordIconNew
} = usePasswordVisibility()
const {
  passwordFieldType: passwordFieldTypeConfirm,
  togglePasswordVisibility: togglePasswordVisibilityConfirm,
  passwordIcon: passwordIconConfirm
} = usePasswordVisibility()

const updatePassword = async () => {
  const validated = await v$.value.$validate()
  if (!validated) return

  isLoading.value = true

  try {
    const { data } = await userStore.updatePassword(formState)

    if (data.status === 'success') {
      notify('Votre mot de passe a été mis à jour', 'success')
      reset()
    } else {
      notifyApiError(data.errors)
    }
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}
</script>

<template>
  <b-overlay :show="isLoading">
    <b-card>
      <b-form @submit.prevent="updatePassword">
        <b-row>
          <b-col md="6">
            <b-form-group label="Mot de passe actuel">
              <b-input-group class="input-group-merge">
                <b-form-input
                  v-model="formState.current_password"
                  :type="passwordFieldType"
                  class="form-control-merge"
                  placeholder="Votre mot de passe actuel"
                />
                <b-input-group-append
                  is-text
                  @click="togglePasswordVisibility"
                >
                  <vue-feather
                    :type="passwordIcon"
                    class="cursor-pointer"
                  />
                </b-input-group-append>
              </b-input-group>
              <small
                v-show="v$.current_password.$errors.length > 0"
                class="text-danger"
              >
                Mot de passe actuel requis
              </small>
            </b-form-group>
          </b-col>
        </b-row>

        <b-row>
          <b-col md="6">
            <b-form-group label="Nouveau mot de passe">
              <b-input-group class="input-group-merge">
                <b-form-input
                  v-model="formState.new_password"
                  :type="passwordFieldTypeNew"
                  placeholder="Nouveau mot de passe"
                />
                <b-input-group-append
                  is-text
                  @click="togglePasswordVisibilityNew"
                >
                  <vue-feather
                    :type="passwordIconNew"
                    class="cursor-pointer"
                  />
                </b-input-group-append>
              </b-input-group>
              <small
                v-show="v$.new_password.$errors.length > 0"
                class="text-danger"
              >
                Votre nouveau mot de passe doit contenir au moins 8
                caractères
              </small>
            </b-form-group>
          </b-col>

          <b-col md="6">
            <b-form-group label="Confirmez votre nouveau mot de passe">
              <b-input-group class="input-group-merge">
                <b-form-input
                  v-model="formState.password_confirmation"
                  :type="passwordFieldTypeConfirm"
                  placeholder="Confirmez votre nouveau mot de passe"
                />
                <b-input-group-append
                  is-text
                  @click="togglePasswordVisibilityConfirm"
                >
                  <vue-feather
                    :type="passwordIconConfirm"
                    class="cursor-pointer"
                  />
                </b-input-group-append>
              </b-input-group>
            </b-form-group>
          </b-col>

          <b-col cols="12">
            <b-button
              v-ripple
              variant="primary"
              class="mt-1 mr-1"
              type="submit"
            >
              Mettre à jour
            </b-button>
          </b-col>
        </b-row>
      </b-form>
    </b-card>
  </b-overlay>
</template>

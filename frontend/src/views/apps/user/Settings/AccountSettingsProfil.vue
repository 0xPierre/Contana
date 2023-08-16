<script lang="ts" setup>
import { useFormValidation } from '@/composables/formValidation'
import { required, email } from '@vuelidate/validators'
import { ref, onMounted } from 'vue'
import { notify, notifyApiError } from '@/helpers/notify'
import { useUserStore } from '@/stores/apps/User'

const profileFile = ref<null | File>(null)
const refInputEl = ref<null | File>(null)
const userStore = useUserStore()
const isLoading = ref(false)

const { formState, v$ } = useFormValidation(
  {
    avatar: '',
    first_name: '',
    last_name: '',
    email: ''
  },
  {
    first_name: {
      required
    },
    last_name: {
      required
    },
    email: {
      required,
      email
    }
  }
)

const onAvatarChange = (e: Event) => {
  const files = (<HTMLInputElement>e.target).files || []
  if (files.length === 0) return

  const file = files[0]
  if (file.size < 8000000) {
    formState.avatar = URL.createObjectURL(file)
    profileFile.value = file
  } else {
    notify(
      'Avatar trop grand',
      'warning',
      "L'avatar que vous avez choisis est trop grand !"
    )
  }
}

const chooseFile = () => {
  // @ts-ignore
  refInputEl.value?.$el.click()
}

const saveChanges = async () => {
  const validated = await v$.value.$validate()
  if (!validated) return

  isLoading.value = true

  try {
    const fd = new FormData()
    fd.append('first_name', formState.first_name)
    fd.append('last_name', formState.last_name)
    fd.append('email', formState.email)
    if (profileFile.value) {
      fd.append('avatar', profileFile.value)
    }

    const { data } = await userStore.updateProfil(fd)

    if (data.status === 'success') {
      notify('Vos informations ont été mises à jour', 'success')
      userStore.data = data.data.user
    } else {
      notifyApiError(data.errors)
    }
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}

onMounted(() => {
  formState.avatar = userStore.data?.avatar || ''
  formState.first_name = userStore.data?.first_name || ''
  formState.last_name = userStore.data?.last_name || ''
  formState.email = userStore.data?.email || ''
})
</script>

<template>
  <b-overlay :show="isLoading">
    <b-card>
      <b-media no-body>
        <b-media-aside>
          <b-link>
            <b-img rounded :src="formState.avatar" height="80" />
          </b-link>
        </b-media-aside>

        <b-media-body class="mt-75 ml-75">
          <b-button
            v-ripple
            variant="primary"
            size="sm"
            class="mb-75 mr-75"
            @click="chooseFile"
          >
            {{
              formState.avatar
                ? 'Changer de photo de profil'
                : 'Mettre en ligne'
            }}
          </b-button>
          <b-form-file
            ref="refInputEl"
            v-model="profileFile"
            accept=".jpg, .png, .gif"
            :hidden="true"
            plain
            @change="onAvatarChange"
          />
          <b-card-text
            >Seulement les images JPG, GIF ou PNG sont autorisé, et de
            moins de 800kB</b-card-text
          >
        </b-media-body>
      </b-media>

      <b-form class="mt-2" @submit.prevent="saveChanges">
        <b-row>
          <b-col sm="6">
            <b-form-group label="Adresse email">
              <b-form-input
                v-model="formState.email"
                placeholder="Adresse email"
              />
              <small
                v-show="v$.email.$errors.length > 0"
                class="text-danger"
              >
                Adresse email invalide
              </small>
            </b-form-group>
          </b-col>
          <b-col sm="6">
            <b-form-group label="Prénom">
              <b-form-input
                v-model="formState.first_name"
                placeholder="Prénom"
              />
              <small
                v-show="v$.first_name.$errors.length > 0"
                class="text-danger"
              >
                Prénom requis
              </small>
            </b-form-group>
          </b-col>
          <b-col sm="6">
            <b-form-group label="Nom">
              <b-form-input
                v-model="formState.last_name"
                placeholder="Nom"
              />
              <small
                v-show="v$.last_name.$errors.length > 0"
                class="text-danger"
              >
                Prénom requis
              </small>
            </b-form-group>
          </b-col>

          <b-col cols="12">
            <b-button
              type="submit"
              v-ripple
              variant="primary"
              class="mt-2 mr-1"
            >
              Enregistrer
            </b-button>
          </b-col>
        </b-row>
      </b-form>
    </b-card>
  </b-overlay>
</template>

<script lang="ts" setup>
import { notify } from '@/helpers/notify'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'

import { ref } from 'vue'

const entrepriseStore = useEntrepriseStore()

const isLoading = ref(false)
const modalInviteUser = ref<any>(null)
const inviteUserMail = ref('')
const invitation_link = ref('')
const inviation_token = ref('')

const openInviteUserModal = async () => {
  modalInviteUser.value?.show()
  inviteUserMail.value = ''
  isLoading.value = true

  try {
    const { data } = await entrepriseStore.createInvitationLink()
    invitation_link.value = data.data.invitation_link
    inviation_token.value = data.data.invitation_token
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}

const sendInvitationLinkToUserByEmail = async () => {
  isLoading.value = true

  try {
    const { data } = await entrepriseStore.sendInvitationLinkToUserByEmail(
      {
        email: inviteUserMail.value,
        invitation_token: inviation_token.value
      }
    )

    if (data.status === 'success') {
      notify("L'invitation a bien été envoyée", 'success')
      modalInviteUser.value?.hide()
    } else notify(data.error, 'danger')
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}

const copyInvitationToClipBoard = () => {
  navigator.clipboard.writeText(invitation_link.value)
  notify('Lien copié dans le presse-papier', 'success')
}
</script>

<template>
  <b-modal ref="modalInviteUser" title="Inviter un utilisateur" size="lg">
    <b-overlay :show="isLoading">
      <p>
        Le lien d'invitation est
        <span class="font-weight-bolder">unique</span> et sera utilisable
        24h. Après ce délai, aucun utilisateur ne pourra rejoindre votre
        entreprise avec ce lien.
      </p>
      <h4 class="mt-2">Lien d'invitation</h4>
      <div
        class="text-primary mt-50 cursor-pointer d-flex"
        @click="copyInvitationToClipBoard"
      >
        <span class="mr-50">
          {{ invitation_link }}
        </span>
        <vue-feather type="copy" />
      </div>

      <h4 class="mt-2">Envoyer le lien d'invitation par e-mail</h4>
      <b-form @submit.prevent="sendInvitationLinkToUserByEmail">
        <b-form-group label="Adresse e-mail">
          <b-input-group>
            <b-form-input
              v-model="inviteUserMail"
              placeholder="Adresse e-mail"
            />
            <b-input-group-append>
              <b-button type="submit" variant="outline-primary" v-ripple>
                Envoyer
              </b-button>
            </b-input-group-append>
          </b-input-group>
        </b-form-group>
      </b-form>
    </b-overlay>
    <template #modal-footer="{ cancel }">
      <b-button variant="outline-secondary" v-ripple @click="cancel">
        Fermer
      </b-button>
    </template>
  </b-modal>

  <b-button variant="primary" v-ripple @click="openInviteUserModal">
    Invitez un utilisateur
  </b-button>
</template>

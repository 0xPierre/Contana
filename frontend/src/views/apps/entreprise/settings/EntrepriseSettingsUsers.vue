<script lang="ts" setup>
import { notify, notifyApiError, swalAlert } from '@/helpers/notify'
import type { EntrepriseUser } from '@/types/entreprise.types'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'

import { ref } from 'vue'
import { fullNameToText } from '@/helpers/utils'
import EntrepriseSettingsUserInvite from './EntrepriseSettingsUserInvite.vue'

const isLoading = ref(false)
const entrepriseStore = useEntrepriseStore()

const tableFields = ref([
  {
    key: 'avatar',
    sortable: false,
    label: 'Avatar'
  },
  {
    key: 'full_name',
    sortable: true,
    label: 'Prénom et nom'
  },
  {
    key: 'email',
    sortable: true,
    label: 'Email'
  },
  {
    key: 'actions',
    sortable: false,
    label: 'Actions'
  }
])

const modalEditUserPermissions = ref<any>(null)
const selectedUser = ref<EntrepriseUser | null>(null)

const openUserPermissionModal = (user: EntrepriseUser) => {
  // administrators cannot edit other administrator permissions
  if (
    (user.permissions.administrate &&
      !entrepriseStore.entreprise?.is_owner) ||
    user.id == entrepriseStore.entreprise?.owner
  )
    return
  selectedUser.value = user
  modalEditUserPermissions.value?.show()
}

const updateUserPermissions = async () => {
  if (!selectedUser.value) return

  isLoading.value = true

  try {
    const { data } = await entrepriseStore.updateUserPermissions(
      selectedUser.value
    )

    if (data.status === 'success') {
      notify('Permissions mises à jour avec succès', 'success')

      modalEditUserPermissions.value?.hide()
    } else {
      notifyApiError(data.errors)
    }
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}

const removeUser = async (user: EntrepriseUser) => {
  const { value } = await swalAlert(
    'Attention',
    'warning',
    `Êtes vous sûr de vouloir éjecter ${user.full_name} de ${entrepriseStore.entreprise?.name} ?`
  )

  if (value && entrepriseStore.entreprise) {
    isLoading.value = true
    try {
      const { data } = await entrepriseStore.removeUser(user)
      if (data.status === 'success') {
        notify('Utilisateur éjecté avec succès', 'success')
        entrepriseStore.entreprise.users = data.data.users
      }
    } catch {
      notify('Une erreur est survenue', 'danger')
    }
    isLoading.value = false
  }
}
</script>

<template>
  <b-overlay :show="isLoading">
    <b-card>
      <template #header>
        <h4 class="mb-0">Utilisateurs</h4>
        <EntrepriseSettingsUserInvite />
      </template>

      <b-table
        :fields="tableFields"
        :items="entrepriseStore.entreprise?.users"
        hover
        @row-clicked="openUserPermissionModal"
      >
        <template #cell(avatar)="data">
          <b-avatar
            size="40"
            variant="light-primary"
            :src="data.value"
            :text="fullNameToText(data.item.full_name || '')"
          />
        </template>

        <template #cell(actions)="data">
          <b-button
            v-if="
              data.item.id !== entrepriseStore.entreprise?.owner &&
              ((data.item.permissions.administrate &&
                entrepriseStore.entreprise?.is_owner) ||
                entrepriseStore.entreprise?.is_owner)
            "
            variant="flat-danger"
            @click="removeUser(data.item)"
          >
            <vue-feather type="trash" size="18" />
          </b-button>
        </template>
      </b-table>
    </b-card>
  </b-overlay>

  <b-modal
    ref="modalEditUserPermissions"
    :title="`Permission de ${selectedUser?.full_name}`"
    size="lg"
  >
    <b-overlay :show="isLoading" v-if="selectedUser">
      <h5>Administrateur</h5>
      <b-form-group>
        <b-form-checkbox
          v-model="selectedUser.permissions.administrate"
          class="m-0"
        >
          Administrateur
        </b-form-checkbox>
      </b-form-group>
      <b-row v-show="!selectedUser.permissions.administrate">
        <b-col md="6">
          <h5>Documents</h5>
          <b-form-group>
            <b-form-checkbox
              v-model="selectedUser.permissions.access_documents"
              class="m-0"
            >
              Accès aux documents
            </b-form-checkbox>
          </b-form-group>
          <b-form-group>
            <b-form-checkbox
              v-model="selectedUser.permissions.update_documents"
              class="m-0"
            >
              Modification des documents
            </b-form-checkbox>
          </b-form-group>
          <h5>Constructeur</h5>
          <b-form-group>
            <b-form-checkbox
              v-model="selectedUser.permissions.access_constructor"
              class="m-0"
            >
              Accès au constructeur
            </b-form-checkbox>
          </b-form-group>
          <h5>Constructeur</h5>
          <b-form-group>
            <b-form-checkbox
              v-model="selectedUser.permissions.access_crm"
              class="m-0"
            >
              Accès aux fonctionnalitées CRM
            </b-form-checkbox>
          </b-form-group>
        </b-col>
        <b-col md="6">
          <h5>Clients</h5>
          <b-form-group>
            <b-form-checkbox
              v-model="selectedUser.permissions.access_clients"
              class="m-0"
            >
              Accès aux clients
            </b-form-checkbox>
          </b-form-group>
          <b-form-group>
            <b-form-checkbox
              v-model="selectedUser.permissions.update_clients"
              class="m-0"
            >
              Modification des clients
            </b-form-checkbox>
          </b-form-group>
          <h5>Tableau de bord</h5>
          <b-form-group>
            <b-form-checkbox
              v-model="selectedUser.permissions.access_dashboard"
              class="m-0"
            >
              Accès aux tableau de bord
            </b-form-checkbox>
          </b-form-group>
        </b-col>
      </b-row>
    </b-overlay>
    <template #modal-footer="{ cancel }">
      <b-button variant="flat-danger" v-ripple @click="cancel">
        Annuler
      </b-button>
      <b-button variant="primary" v-ripple @click="updateUserPermissions">
        Enregistrer
      </b-button>
    </template>
  </b-modal>
</template>

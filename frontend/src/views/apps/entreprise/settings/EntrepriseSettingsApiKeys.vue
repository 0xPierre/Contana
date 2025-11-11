<script lang="ts" setup>
import { notify, notifyApiError, swalAlert } from '@/helpers/notify'
import type { ApplicationToken } from '@/types/entreprise.types'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'
import { ref, onMounted } from 'vue'

const isLoading = ref(false)
const entrepriseStore = useEntrepriseStore()
const tokens = ref<ApplicationToken[]>([])

const modalCreateToken = ref<any>(null)
const modalShowToken = ref<any>(null)
const tokenName = ref('')
const selectedUserId = ref<number | null>(null)
const createdToken = ref<string | null>(null)

const tableFields = ref([
  {
    key: 'name',
    sortable: true,
    label: 'Nom'
  },
  {
    key: 'key',
    sortable: true,
    label: 'Clé'
  },
  {
    key: 'user',
    sortable: true,
    label: 'Utilisateur'
  },
  {
    key: 'created',
    sortable: true,
    label: 'Créé le'
  },
  {
    key: 'actions',
    sortable: false,
    label: 'Actions'
  }
])

const loadTokens = async () => {
  isLoading.value = true
  try {
    const result = await entrepriseStore.getApplicationTokens()
    tokens.value = Array.isArray(result)
      ? result
      : (result as any).results || []
  } catch (error: any) {
    notify(
      'Une erreur est survenue lors du chargement des clés API',
      'danger'
    )
    tokens.value = []
  }
  isLoading.value = false
}

const openCreateTokenModal = () => {
  tokenName.value = ''
  selectedUserId.value = null
  modalCreateToken.value?.show()
}

const createToken = async () => {
  if (!selectedUserId.value) {
    notify('Veuillez sélectionner un utilisateur', 'warning')
    return
  }

  isLoading.value = true
  try {
    const newToken = await entrepriseStore.createApplicationToken(
      tokenName.value ? tokenName.value : undefined,
      selectedUserId.value
    )
    loadTokens()
    createdToken.value = newToken.key
    modalCreateToken.value?.hide()
    modalShowToken.value?.show()
  } catch (error: any) {
    if (error.response?.data?.errors) {
      notifyApiError(error.response.data.errors)
    } else {
      notify(
        'Une erreur est survenue lors de la création de la clé API',
        'danger'
      )
    }
  }
  isLoading.value = false
}

const copyTokenAndClose = async () => {
  if (createdToken.value) {
    await copyToClipboard(createdToken.value)
  }
  modalShowToken.value?.hide()
  createdToken.value = null
}

const deleteToken = async (token: ApplicationToken) => {
  const { value } = await swalAlert(
    'Attention',
    'warning',
    `Êtes-vous sûr de vouloir supprimer cette clé API ? Cette action est irréversible.`
  )

  if (value) {
    isLoading.value = true
    try {
      await entrepriseStore.deleteApplicationToken(token.key)
      loadTokens()
      notify('Clé API supprimée avec succès', 'success')
    } catch {
      notify(
        'Une erreur est survenue lors de la suppression de la clé API',
        'danger'
      )
    }
    isLoading.value = false
  }
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const copyToClipboard = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text)
    notify('Clé API copiée dans le presse-papier', 'success')
  } catch {
    notify('Impossible de copier la clé API', 'danger')
  }
}

onMounted(() => {
  loadTokens()
})
</script>

<template>
  <b-overlay :show="isLoading">
    <b-card>
      <template #header>
        <div
          class="d-flex w-100 justify-content-between align-items-center"
        >
          <h4 class="mb-0">Clés API</h4>
          <b-button
            variant="primary"
            v-ripple
            @click="openCreateTokenModal"
            class="btn-with-icon"
          >
            <vue-feather type="plus" size="18" class="mr-50" />
            Créer une clé API
          </b-button>
        </div>
      </template>

      <b-table
        :fields="tableFields"
        :items="tokens"
        hover
        show-empty
        empty-text="Aucune clé API créée"
      >
        <template #cell(name)="data">
          <span v-if="data.value">{{ data.value }}</span>
          <span v-else class="text-muted">Sans nom</span>
        </template>

        <template #cell(user)="data">
          <span v-if="data.value?.full_name">{{ data.value.full_name }}</span>
          <span v-else class="text-muted">-</span>
        </template>

        <template #cell(created)="data">
          {{ formatDate(data.value) }}
        </template>

        <template #cell(actions)="data">
          <b-button
            variant="flat-danger"
            @click="deleteToken(data.item)"
            title="Supprimer la clé API"
          >
            <vue-feather type="trash" size="18" />
          </b-button>
        </template>
      </b-table>
    </b-card>
  </b-overlay>

  <b-modal
    ref="modalCreateToken"
    title="Créer une clé API"
    @hidden="tokenName = ''; selectedUserId = null"
  >
    <b-form-group label="Nom de la clé API (optionnel)">
      <b-form-input
        v-model="tokenName"
        placeholder="Ex: Production API, Test API..."
        :disabled="isLoading"
      />
    </b-form-group>
    <b-form-group label="Clé liée à" required>
      <v-select
        v-model="selectedUserId"
        :options="entrepriseStore.entreprise?.users"
        :reduce="(a: any) => a.id"
        label="full_name"
        :disabled="isLoading"
        :clearable="false"
        placeholder="Sélectionner un utilisateur..."
      />
    </b-form-group>
    <template #modal-footer="{ cancel }">
      <b-button
        variant="flat-danger"
        v-ripple
        @click="cancel"
        :disabled="isLoading"
      >
        Annuler
      </b-button>
      <b-button
        variant="primary"
        v-ripple
        @click="createToken"
        :disabled="isLoading"
      >
        Créer
      </b-button>
    </template>
  </b-modal>

  <b-modal
    ref="modalShowToken"
    title="Clé API créée"
    @hidden="createdToken = null"
  >
    <b-form-group>
      <b-form-input
        :value="createdToken || ''"
        readonly
        class="font-monospace"
      />
    </b-form-group>
    <template #modal-footer="{ cancel }">
      <b-button variant="flat-secondary" v-ripple @click="cancel">
        Fermer
      </b-button>
      <b-button variant="primary" v-ripple @click="copyTokenAndClose">
        Copier la clé
      </b-button>
    </template>
  </b-modal>
</template>

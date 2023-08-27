<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { DocumentModel } from '@/types/documents.types.ts'

const { document } = defineProps<{
  document: DocumentModel
}>()

const modal = ref<HTMLElement | null>(null)
const isLoading = ref(false)

const acompte = reactive({
  type: 'pourcentage',
  value: 30
})

const openModal = () => {
  modal.value?.show()
}
</script>

<template>
  <b-button
    variant="outline-success"
    block
    v-ripple
    class="btn-with-icon justify-content-center"
    @click="openModal"
  >
    <vue-feather type="file-plus" size="18" class="mr-50" />
    Produire un acompte
  </b-button>

  <b-modal
    ref="modal"
    :title="`Nouvel acompte sur devis ${document.document_number}`"
    size="md"
  >
    <template #modal-footer="{ cancel }">
      <b-button
        variant="outline-secondary"
        v-ripple
        @click="cancel"
        :disabled="isLoading"
      >
        Annuler
      </b-button>
      <b-button variant="primary" v-ripple :disabled="isLoading">
        Produire l'acompte
      </b-button>
    </template>
  </b-modal>
</template>

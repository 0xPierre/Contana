<script lang="ts" setup>
import { ref } from 'vue'
import { notify } from '@/helpers/notify.ts'
import { useConstructorStore } from '@/stores/apps/Constructor.ts'

const pdfOverview = ref<HTMLElement | null>(null)
const isLoading = ref(false)
const constructorStore = useConstructorStore()
const blobUrl = ref<string | null>(null)

const generatePreview = async () => {
  blobUrl.value = null
  pdfOverview.value?.show()
  isLoading.value = true
  try {
    const { data } = await constructorStore.generatePreview()
    console.log(data)

    blobUrl.value = URL.createObjectURL(
      new Blob([data], { type: 'application/pdf' })
    )
  } catch (e) {
    notify(
      "Une erreur est survenue lors de la génération de l'aperçu",
      'danger'
    )
    pdfOverview.value?.hide()
  }
  isLoading.value = false
}
</script>

<template>
  <div>
    <b-modal title="Aperçu du document" ref="pdfOverview" size="lg">
      <b-overlay :show="isLoading">
        <div class="mt-2" style="min-height: 600px">
          <iframe
            v-if="blobUrl"
            :src="`${blobUrl}#toolbar=0&navpanes=0&scrollbar=1`"
            type="application/pdf"
            width="100%"
            height="600px"
          />
        </div>
      </b-overlay>
      <template #modal-footer="{ cancel }">
        <b-button
          variant="outline-secondary"
          v-ripple
          @click="cancel"
          :disabled="isLoading"
        >
          Fermer
        </b-button>
        <b-button
          variant="outline-primary"
          v-ripple
          @click="cancel"
          :disabled="isLoading"
          :href="blobUrl"
          target="_blank"
        >
          Ouvrir dans un nouvel onglet
        </b-button>
      </template>
    </b-modal>
    <b-button
      v-ripple
      variant="outline-primary"
      block
      class="btn-with-icon"
      @click="generatePreview"
    >
      <vue-feather type="eye" class="mr-50" size="16" />
      Aperçu {{ constructorStore.formeSentence.second }}
    </b-button>
  </div>
</template>

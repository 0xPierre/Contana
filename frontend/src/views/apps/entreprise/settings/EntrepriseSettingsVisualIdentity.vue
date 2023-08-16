<script lang="ts" setup>
import FileUploadManager from '@/components/file-upload-manager/FileUploadManager.vue'
import { notify } from '@/helpers/notify'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'
import { ref } from 'vue'

const entrepriseStore = useEntrepriseStore()

const files = ref<any>(entrepriseStore.entreprise?.logos)
const isLoading = ref(false)

const filesUpdates = (newFiles: File[]) => {
  files.value = newFiles
}

const updateLogos = async () => {
  isLoading.value = true

  try {
    const { data } = await entrepriseStore.updateEntrepriseLogos(
      files.value
    )
    notify('Logos mis à jour avec succès', 'success')
    entrepriseStore.entreprise = data.data
    files.value = entrepriseStore.entreprise?.logos
  } catch {
    notify('Une erreur est survenue', 'danger')
  }

  isLoading.value = false
}
</script>

<template>
  <div>
    <b-overlay :show="isLoading">
      <b-card title="Logos">
        <FileUploadManager
          :files="files"
          :multiple="true"
          accept="image/*"
          :preview="true"
          @update-files="filesUpdates"
        />
        <b-button
          v-ripple
          variant="primary"
          class="mt-1"
          @click="updateLogos"
        >
          Enregistrer
        </b-button>
      </b-card>
    </b-overlay>
  </div>
</template>

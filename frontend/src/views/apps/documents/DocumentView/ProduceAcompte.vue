<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { DocumentModel } from '@/types/documents.types.ts'
import { useNumberInputHandler } from '@/composables/numberInputHandler.ts'
import { notify } from '@/helpers/notify.ts'
import { useDocumentsStore } from '@/stores/apps/Documents.ts'
import { useRouter } from 'vue-router'

const { document } = defineProps<{
  document: DocumentModel
}>()

const modal = ref<HTMLElement | null>(null)
const documentStore = useDocumentsStore()
const isLoading = ref(false)
const router = useRouter()

const acompte = reactive({
  type: 'percentage',
  value: 30,
  vat_rate: 20
})

const openModal = () => {
  modal.value?.show()
  acompte.type = 'percentage'
  acompte.value = 30
  acompte.vat_rate = 20
}

const produceAcompte = async () => {
  isLoading.value = true

  try {
    const { data } = await documentStore.produceAcompteFromDevis(
      document.id,
      acompte
    )
    if (data.status === 'failed') {
      notify(data.error, 'danger')
    } else {
      router.push({
        name: 'entreprise-document-view',
        params: {
          documentId: data.data.document_id,
          documentNumber: data.data.document_number
        }
      })
    }
  } catch (e) {
    console.log(e)
    notify(
      "Une erreur est survenue lors de la production de l'acompte",
      'danger'
    )
  }

  isLoading.value = false
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
    <b-row>
      <b-col md="6">
        <b-form-group label="Type d'acompte">
          <v-select
            :options="[
              {
                label: '% du total TTC',
                value: 'percentage'
              },
              {
                label: 'Montant TTC',
                value: 'amount'
              }
            ]"
            v-model="acompte.type"
            :reduce="(option) => option.value"
            :clearable="false"
          />
        </b-form-group>
      </b-col>
      <b-col md="6">
        <b-form-group label="Taux de TVA">
          <v-select
            :options="[
              {
                label: '20%',
                value: 20
              },
              {
                label: '10%',
                value: 10
              },
              {
                label: '5.5%',
                value: 5.5
              },
              {
                label: '2.1%',
                value: 2.1
              },
              {
                label: '0%',
                value: 0
              }
            ]"
            v-model="acompte.vat_rate"
            :reduce="(option) => option.value"
            :clearable="false"
          />
        </b-form-group>
      </b-col>
    </b-row>

    <b-form-group v-if="acompte.type === 'amount'" label="Montant TTC">
      <b-input-group append="€">
        <b-form-input v-model="acompte.value" type="number" />
      </b-input-group>
    </b-form-group>

    <b-form-group v-else label="Montant de l'acompte">
      <b-input-group append="%">
        <b-form-input v-model="acompte.value" type="number" />
      </b-input-group>
    </b-form-group>

    <template #modal-footer="{ cancel }">
      <b-button
        variant="outline-secondary"
        v-ripple
        @click="cancel"
        :disabled="isLoading"
      >
        Annuler
      </b-button>
      <b-button
        variant="primary"
        v-ripple
        :disabled="isLoading"
        @click="produceAcompte"
      >
        Produire l'acompte
      </b-button>
    </template>
  </b-modal>
</template>

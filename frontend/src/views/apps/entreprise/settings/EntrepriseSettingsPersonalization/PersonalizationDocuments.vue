<script lang="ts" setup>
import { PaymentsMethod } from '@/types/core.types.ts'
import { computed, onBeforeMount, reactive, ref } from 'vue'
import { useEntrepriseStore } from '@/stores/apps/Entreprise.ts'
import { notify } from '@/helpers/notify.ts'

const isLoading = ref(false)
const entrepriseStore = useEntrepriseStore()

const localData = reactive({
  document_logo_size: 0,
  document_logo_margin_right: 0,
  document_logo_margin_top: 0,
  document_logo_margin_bottom: 0,
  document_logo_used: null as null | number,
  document_default_payment_method: PaymentsMethod.BankTransfer,
  document_payment_mention: '',
  document_other_mention: '',
  vat_payer: true,
  document_notes: '',
  first_facture_number: 1,
  first_devis_number: 1,
  first_acompte_number: 1,
  first_avoir_number: 1,
  first_client_number: 1
})

onBeforeMount(() => {
  localData.document_logo_size =
    entrepriseStore.entreprise?.document_logo_size || 0
  localData.document_logo_margin_right =
    entrepriseStore.entreprise?.document_logo_margin_right || 0
  localData.document_logo_margin_top =
    entrepriseStore.entreprise?.document_logo_margin_top || 0
  localData.document_logo_margin_bottom =
    entrepriseStore.entreprise?.document_logo_margin_bottom || 0
  localData.document_logo_used =
    entrepriseStore.entreprise?.document_logo_used || null
  localData.document_default_payment_method =
    entrepriseStore.entreprise?.document_default_payment_method ||
    PaymentsMethod.BankTransfer
  localData.document_payment_mention =
    entrepriseStore.entreprise?.document_payment_mention || ''
  localData.document_other_mention =
    entrepriseStore.entreprise?.document_other_mention || ''
  localData.vat_payer = entrepriseStore.entreprise?.vat_payer || true
  localData.document_notes =
    entrepriseStore.entreprise?.document_notes || ''
  localData.first_facture_number =
    entrepriseStore.entreprise?.first_facture_number || 1
  localData.first_devis_number =
    entrepriseStore.entreprise?.first_devis_number || 1
  localData.first_acompte_number =
    entrepriseStore.entreprise?.first_acompte_number || 1
  localData.first_avoir_number =
    entrepriseStore.entreprise?.first_avoir_number || 1
  localData.first_client_number =
    entrepriseStore.entreprise?.first_client_number || 1
})

const savePersonnalization = async () => {
  isLoading.value = true
  try {
    const { data } =
      await entrepriseStore.updateEntrepriseDocumentsPersonnalization(
        localData
      )
    if (data.status === 'success') {
      entrepriseStore.entreprise = data.data
      notify('Informations mises à jour avec succès', 'success')
    } else {
      notify(data.error, 'danger')
    }
  } catch (e) {
    notify("Une erreur est survenue lors de l'enregistrement", 'danger')
  }
  isLoading.value = false
}

const documentPreview = async () => {
  isLoading.value = true
  try {
    const { data } =
      await entrepriseStore.getPersonnalizationDocumentPreview(localData)

    const blobUrl = URL.createObjectURL(
      new Blob([data], { type: 'application/pdf' })
    )
    window.open(blobUrl, '_blank')
  } catch (e) {
    notify(
      "Une erreur est survenue lors de la génération de l'aperçu",
      'danger'
    )
  }
  isLoading.value = false
}

const logoUsedUrl = computed(() => {
  const logo = entrepriseStore.entreprise?.logos.find(
    (logo) => logo.id === localData.document_logo_used
  )

  return logo ? logo.url : ''
})
</script>

<template>
  <b-overlay :show="isLoading">
    <vue-perfect-scrollbar tagname="div" class="scroll-container">
      <b-card>
        <h4>Logo</h4>
        <b-row>
          <b-col md="8">
            <b-row>
              <b-col md="6">
                <b-form-group
                  :label="`Taille du logo : ${localData.document_logo_size}px`"
                >
                  <b-form-input
                    min="0"
                    max="500"
                    type="range"
                    v-model="localData.document_logo_size"
                  />
                </b-form-group>
              </b-col>
              <b-col md="6">
                <b-form-group
                  :label="`Marge droite du logo : ${localData.document_logo_margin_right}px`"
                >
                  <b-form-input
                    min="-100"
                    max="250"
                    type="range"
                    v-model="localData.document_logo_margin_right"
                  />
                </b-form-group>
              </b-col>
              <b-col md="6">
                <b-form-group
                  :label="`Marge haute du logo : ${localData.document_logo_margin_top}px`"
                >
                  <b-form-input
                    min="-250"
                    max="250"
                    type="range"
                    v-model="localData.document_logo_margin_top"
                  />
                </b-form-group>
              </b-col>
              <b-col md="6">
                <b-form-group
                  :label="`Marge basse du logo : ${localData.document_logo_margin_bottom}px`"
                >
                  <b-form-input
                    min="0"
                    max="150"
                    type="range"
                    v-model="localData.document_logo_margin_bottom"
                  />
                </b-form-group>
              </b-col>
            </b-row>
          </b-col>
          <b-col md="4">
            <b-form-group label="Logo utilisé sur les documents">
              <v-select
                :options="[
                  {
                    id: null,
                    name: 'Aucun',
                    url: ''
                  },
                  ...entrepriseStore.entreprise?.logos
                ]"
                :reduce="(a) => a.id"
                label="name"
                v-model="localData.document_logo_used"
                :clearable="false"
              />
              <img
                v-if="logoUsedUrl"
                class="mt-1"
                :src="logoUsedUrl"
                style="max-width: 200px; max-height: 75px"
              />
            </b-form-group>
          </b-col>
        </b-row>
        <hr />
        <h4>Informations complémentaires</h4>
        <b-row>
          <b-col md="6">
            <b-form-group
              label="Moyen de paiement"
              description="Moyen de paiement par défaut pour les factures."
            >
              <v-select
                :options="[
                  {
                    label: 'Virement',
                    value: PaymentsMethod.BankTransfer
                  },
                  {
                    label: 'Chèque',
                    value: PaymentsMethod.Check
                  },
                  {
                    label: 'Espèces',
                    value: PaymentsMethod.Cash
                  },
                  {
                    label: 'Carte bancaire',
                    value: PaymentsMethod.CreditCard
                  },
                  {
                    label: 'Prélèvement',
                    value: PaymentsMethod.DirectDebit
                  },
                  {
                    label: 'Autre',
                    value: PaymentsMethod.Other
                  }
                ]"
                v-model="localData.document_default_payment_method"
                :reduce="(option) => option.value"
                label="label"
                :clearable="false"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Mention de paiement">
              <b-form-input
                placeholder="À réception de la facture"
                v-model="localData.document_payment_mention"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Mention autre">
              <b-form-input
                placeholder="TVA non applicable, article 293 B du CGI"
                v-model="localData.document_other_mention"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Redevable de la TVA">
              <v-select
                :options="[
                  {
                    label: 'Oui',
                    value: true
                  },
                  {
                    label: 'Non',
                    value: false
                  }
                ]"
                :reduce="(option) => option.value"
                label="label"
                :clearable="false"
                v-model="localData.vat_payer"
              />
            </b-form-group>
          </b-col>
          <b-col md="12">
            <b-form-group label="Note du document">
              <b-form-textarea
                rows="5"
                max-rows="10"
                placeholder="En cas de retard de paiement, il sera appliqué des pénalités et intérêts de retard suivant le taux minimum légal en vigueur, par mois de retard. En outre, une indemnité forfaitaire pour frais de recouvrement de 40€ sera due."
                v-model="localData.document_notes"
              />
            </b-form-group>
          </b-col>
        </b-row>

        <hr />
        <h4>Numéro de document</h4>
        <p>
          Vous pouvez modifier le premier numéro d'une série de document
          seulement si aucun document de celle-ci n'a été créé.
        </p>
        <b-row>
          <b-col md="6">
            <b-form-group label="Premier numéro de facture">
              <b-form-input
                placeholder="1"
                type="number"
                min="0"
                v-model="localData.first_facture_number"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Premier numéro de devis">
              <b-form-input
                placeholder="1"
                type="number"
                min="0"
                v-model="localData.first_devis_number"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Premier numéro d'acompte">
              <b-form-input
                placeholder="1"
                type="number"
                min="0"
                v-model="localData.first_acompte_number"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Premier numéro d'avoir">
              <b-form-input
                placeholder="1"
                type="number"
                min="0"
                v-model="localData.first_avoir_number"
              />
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Premier numéro client">
              <b-form-input
                placeholder="1"
                type="number"
                min="0"
                v-model="localData.first_client_number"
              />
            </b-form-group>
          </b-col>
        </b-row>

        <div class="d-flex">
          <b-button
            variant="primary"
            v-ripple
            @click="savePersonnalization"
          >
            Enregistrer
          </b-button>
          <b-button
            variant="outline-primary"
            v-ripple
            class="btn-with-icon ml-1"
            @click="documentPreview"
          >
            <vue-feather type="eye" size="16" class="mr-50" />
            <span> Aperçu d'un document </span>
          </b-button>
        </div>
      </b-card>
    </vue-perfect-scrollbar>
  </b-overlay>
</template>

<style scoped>
.scroll-container {
  max-height: calc(100vh - 102px - 1rem - 41px - 1rem);
}
</style>

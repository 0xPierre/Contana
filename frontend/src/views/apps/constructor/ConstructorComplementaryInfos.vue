<script lang="ts" setup>
import { ref } from 'vue'
import { useConstructorStore } from '@/stores/apps/Constructor'
import { PaymentsMethod, DocumentsType } from '@/types/core.types'

const constructorStore = useConstructorStore()
const modalInfos = ref<HTMLElement | null>(null)
</script>
<template>
  <div>
    <b-button
      variant="flat-success"
      v-ripple
      block
      @click="modalInfos.show()"
    >
      Informations complémentaires
    </b-button>

    <b-modal
      ref="modalInfos"
      title="Informations complémentaires"
      size="lg"
    >
      <b-row>
        <b-col md="6">
          <b-form-group label="Redevable de la TVA">
            <v-select
              v-model="constructorStore.vatPayer"
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
            />
          </b-form-group>
          <b-form-group
            :label="`Moyen de paiement ${constructorStore.formeSentence.second}`"
          >
            <v-select
              v-model="constructorStore.paymentMethod"
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
              :reduce="(option) => option.value"
              label="label"
              :clearable="false"
            />
          </b-form-group>
        </b-col>
        <b-col md="6">
          <b-form-group
            v-show="constructorStore.forme === DocumentsType.Devis"
            :label="`Date de fin de validité ${constructorStore.formeSentence.second}`"
          >
            <flat-pickr
              v-model="constructorStore.validityDate"
              class="form-control"
            />
          </b-form-group>
          <b-form-group label="Mention de paiement">
            <b-form-input
              v-model="constructorStore.paymentMention"
              placeholder="A réception de la facture"
            />
          </b-form-group>

          <b-form-group label="Mention autre">
            <b-form-input
              v-model="constructorStore.otherMention"
              placeholder=""
            />
          </b-form-group>
        </b-col>
      </b-row>
      <b-form-group
        :label="`Notes sur ${constructorStore.formeSentence.first}`"
      >
        <b-form-textarea
          v-model="constructorStore.notes"
          placeholder="Notes"
          rows="5"
          max-rows="10"
        />
      </b-form-group>
      <template #modal-footer="{ ok }">
        <b-button variant="outline-secondary" v-ripple @click="ok">
          Fermer
        </b-button>
      </template>
    </b-modal>
  </div>
</template>

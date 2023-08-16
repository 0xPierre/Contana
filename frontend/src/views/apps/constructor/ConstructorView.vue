<script lang="ts" setup>
import { onBeforeMount } from 'vue'
import ConstructorClient from './ConstructorClient.vue'
import ConstructorComplementaryInfos from './ConstructorComplementaryInfos.vue'
import ConstructorCatalogue from './Catalogue/ConstructorCatalogue.vue'
import { useConstructorStore } from '@/stores/apps/Constructor'
import { PaymentsMethod, DocumentsType } from '@/types/core.types'

const constructorStore = useConstructorStore()

onBeforeMount(() => {
  constructorStore.client = null
  constructorStore.paymentMethod = PaymentsMethod.BankTransfer
  constructorStore.forme = DocumentsType.Devis
  constructorStore.validityDate = new Date(
    new Date().setDate(new Date().getDate() + 90)
  )
  constructorStore.paymentMention = 'À réception de la facture'
  constructorStore.vatPayer = true
  constructorStore.notes =
    'En cas de retard de paiement, il sera appliqué des pénalités et intérêts de retard suivant le taux minimum légal en vigueur, par mois de retard. En outre, une indemnité forfaitaire pour frais de recouvrement de 40€ sera due.'
  constructorStore.otherMention = ''
})
</script>

<template>
  <div>
    <b-row>
      <b-col md="9" class="pr-md-50">
        <b-card class="mb-1 p-1" no-body>
          <b-row>
            <b-col cols="4">
              <v-select
                :options="[
                  {
                    label: 'Devis',
                    value: DocumentsType.Devis
                  },
                  {
                    label: 'Facture',
                    value: DocumentsType.Facture
                  },
                  {
                    label: 'Avoir',
                    value: DocumentsType.Avoir
                  }
                ]"
                :clearable="false"
                v-model="constructorStore.forme"
                :reduce="(option) => option.value"
                label="label"
                block
              />
            </b-col>
            <b-col cols="4">
              <b-form-input
                :placeholder="`Objet ${constructorStore.formeSentence.second}`"
                type="text"
              />
            </b-col>
            <b-col cols="4">
              <ConstructorComplementaryInfos />
            </b-col>
          </b-row>
        </b-card>

        <b-card no-body>
          <vue-perfect-scrollbar
            :settings="{
              wheelPropagation: true
            }"
            class="area"
          >
            <!-- <div
              class="empty-area d-flex justify-content-center align-items-center cursor-pointer"
            >
              <vue-feather type="plus-circle" size="28" />
              <span class="ml-1 font-medium-1">Ajouter une section</span>
            </div> -->
            <div class="sections">
              <div class="section section-title">
                <b-row>
                  <b-col cols="5">
                    <h5 class="mb-0 font-small-5">Titre de section</h5>
                    <div class="d-flex mt-1" style="gap: 1.2rem">
                      <vue-feather
                        type="copy"
                        size="22"
                        class="cursor-pointer"
                      />
                      <vue-feather
                        type="trash-2"
                        size="22"
                        class="cursor-pointer"
                      />
                    </div>
                  </b-col>
                  <b-col cols="7">
                    <b-form-input
                      placeholder="Titre de la section"
                      type="text"
                    />
                  </b-col>
                </b-row>
              </div>
              <div class="section section-subtotal">
                <b-row>
                  <b-col cols="5">
                    <h5 class="mb-0 font-small-5">Sous total</h5>
                    <div class="d-flex mt-1" style="gap: 1.2rem">
                      <vue-feather
                        type="copy"
                        size="22"
                        class="cursor-pointer"
                      />
                      <vue-feather
                        type="trash-2"
                        size="22"
                        class="cursor-pointer"
                      />
                    </div>
                  </b-col>
                  <b-col cols="4">
                    <b-form-input
                      placeholder="Titre du sous total"
                      type="text"
                    />
                  </b-col>
                  <b-col cols="3">
                    <b-input-group append="€">
                      <b-form-input
                        placeholder="Prix du sous total"
                        type="number"
                        :value="18"
                        :disabled="true"
                      />
                    </b-input-group>
                  </b-col>
                </b-row>
              </div>
              <div class="section section-title-with-price">
                <div class="d-flex justify-content-between">
                  <h5 class="mb-0 font-small-5">Titre avec prix</h5>
                  <div>
                    <vue-feather
                      type="settings"
                      size="22"
                      class="cursor-pointer"
                    />
                  </div>
                </div>

                <b-row class="mt-50">
                  <b-col md="4">
                    <b-form-group label="Titre">
                      <b-form-input
                        type="text"
                        placeholder="Titre de la section"
                      />
                    </b-form-group>
                  </b-col>
                  <b-col md="3">
                    <b-form-group label="Prix">
                      <b-input-group append="€">
                        <b-form-input
                          type="number"
                          placeholder="Prix de la section"
                          min="0"
                          step="0.01"
                        />
                      </b-input-group>
                    </b-form-group>
                  </b-col>
                  <b-col md="3">
                    <b-form-group label="TVA">
                      <v-select
                        :options="[
                          {
                            label: '20 %',
                            value: 20
                          },
                          {
                            label: '10 %',
                            value: 10
                          },
                          {
                            label: '5.5 %',
                            value: 5.5
                          },
                          {
                            label: '2.1 %',
                            value: 2.1
                          },
                          {
                            label: '0 %',
                            value: 0
                          }
                        ]"
                        :clearable="false"
                        style="width: 100%"
                      />
                    </b-form-group>
                  </b-col>
                  <b-col md="2">
                    <b-form-group label="Qté">
                      <b-form-input
                        type="number"
                        placeholder="Quantité"
                        min="0"
                      />
                    </b-form-group>
                  </b-col>
                </b-row>

                <b-form-textarea
                  placeholder="Description de la section"
                  rows="3"
                  class="mb-1"
                  max-rows="10"
                />
                <div class="d-flex justify-content-between mt-25">
                  <div class="d-flex" style="gap: 1.2rem">
                    <vue-feather
                      type="copy"
                      size="22"
                      class="cursor-pointer"
                    />
                    <vue-feather
                      type="trash-2"
                      size="22"
                      class="cursor-pointer"
                    />
                  </div>
                  <div class="font-medium-1">
                    Total HT :
                    <span class="font-weight-bolder text-primary"
                      >&nbsp;0 €</span
                    >
                  </div>
                </div>
              </div>
            </div>
          </vue-perfect-scrollbar>
        </b-card>
      </b-col>
      <b-col md="3" class="pl-md-50">
        <vue-perfect-scrollbar class="actions-col" tagname="div">
          <ConstructorClient />
          <b-card class="mb-1 user-select-none p-1" no-body>
            <div class="draggable article mx-75">
              <vue-feather type="move" size="16" class="cursor-pointer" />
              <span>Article</span>
            </div>
            <div class="draggable article mx-75">
              <vue-feather type="move" size="16" class="cursor-pointer" />
              <span>Titre</span>
            </div>
            <div class="draggable article mx-75">
              <vue-feather type="move" size="16" class="cursor-pointer" />
              <span>Sous-total</span>
            </div>
            <hr class="px-2" />
            <ConstructorCatalogue />
          </b-card>

          <b-card class="p-1" no-body>
            <div>
              <div
                class="d-flex justify-content-between font-weight-bolder"
              >
                <span>Total HT</span>
                <span>0,00 €</span>
              </div>
              <div class="d-flex justify-content-between">
                <span>TVA</span>
                <span>0,00 €</span>
              </div>
              <div class="d-flex justify-content-between">
                <span>Total TTC</span>
                <span>0,00 €</span>
              </div>
            </div>

            <hr />
            <b-button
              v-ripple
              variant="success"
              block
              class="btn-with-icon"
            >
              <vue-feather type="file-plus" class="mr-50" size="16" />
              Produire {{ constructorStore.formeSentence.first }}
            </b-button>
            <b-button
              v-ripple
              variant="outline-primary"
              block
              class="btn-with-icon"
            >
              <vue-feather type="eye" class="mr-50" size="16" />
              Aperçu {{ constructorStore.formeSentence.second }}
            </b-button>
            <b-button
              v-ripple
              variant="outline-secondary"
              block
              class="btn-with-icon"
            >
              <vue-feather type="save" class="mr-50" size="16" />
              Enregistrer en brouillon
            </b-button>
          </b-card>
        </vue-perfect-scrollbar>
      </b-col>
    </b-row>
  </div>
</template>

<style lang="scss">
.actions-col {
  max-height: calc(100vh - 102px - 1rem);
  // overflow-y: auto;
}

.articles-list {
  margin-top: 1rem;
  max-height: 200px;
}
.article {
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: var(--white);
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 10px;
  padding: 13px 15px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);

  span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 80%;
  }
}

.dark-layout {
  .area {
    border-color: #d0d2d6;
  }
  .draggable.article {
    background-color: #161d31;
  }

  .draggable.article:hover {
    background-color: #1f2a48;
  }
}

.area {
  min-height: 350px;
  max-height: calc(100vh - 102px - 1rem - 100px - 1rem);

  .empty-area {
    border: 2px dashed rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    min-height: 350px;
    margin: 1.5rem;
  }
}

.sections {
  .section {
    margin: 1rem 1.5rem;
    user-select: none;
    cursor: move;
    padding: 1.2rem;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 5px;
    margin-bottom: 1rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  }
}
</style>

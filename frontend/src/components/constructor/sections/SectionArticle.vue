<script lang="ts" setup>
import { useConstructorStore } from '@/stores/apps/Constructor.ts'
import {
  CatalogTemplate,
  Section,
  SectionsType
} from '@/types/constructor.types.ts'
import { computed, ref, watch } from 'vue'
import { useNumberInputHandler } from '@/composables/numberInputHandler.ts'
import { euro, getSectionArticleTotalHT } from '@/helpers/utils.ts'

const props = defineProps<{
  section: Section<SectionsType.Article> | CatalogTemplate
  isTemplate?: boolean
}>()

const totalHT = computed(() => {
  return getSectionArticleTotalHT(
    props.section as Section<SectionsType.Article>
  ).format()
})
const { inputHandler, formattedValue } = useNumberInputHandler(
  props.section.values.unitPriceHT,
  (value: number) => {
    props.section.values.unitPriceHT = value
  }
)
const constructorStore = useConstructorStore()
const modal = ref<HTMLElement | null>(null)
</script>

<template>
  <div class="section section-article">
    <div class="d-flex justify-content-between">
      <h5 class="mb-0 font-small-5">Article</h5>
      <div @click="modal.show()">
        <vue-feather type="settings" size="22" class="cursor-pointer" />
      </div>
    </div>

    <b-row class="mt-50">
      <b-col :md="constructorStore.vatPayer ? 4 : 7">
        <b-form-group label="Titre">
          <b-form-input
            type="text"
            placeholder="Titre de la section"
            v-model="props.section.values.title"
            class="nodrag"
          />
        </b-form-group>
      </b-col>
      <b-col md="3">
        <b-form-group label="Prix">
          <b-input-group append="€">
            <input
              class="form-control nodrag"
              :value="formattedValue"
              type="number"
              step="0.01"
              min="0"
              placeholder="Prix"
              @input="inputHandler"
            />
          </b-input-group>
        </b-form-group>
      </b-col>
      <b-col v-if="constructorStore.vatPayer" md="3">
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
            :reduce="(option: any) => option.value"
            style="width: 100%"
            v-model="props.section.values.vatRate"
            class="nodrag"
          />
        </b-form-group>
      </b-col>
      <b-col md="2">
        <b-form-group label="Qté">
          <b-form-input
            type="number"
            placeholder="Quantité"
            min="0"
            v-model="props.section.values.quantity"
            class="nodrag"
          />
        </b-form-group>
      </b-col>
    </b-row>

    <b-form-textarea
      placeholder="Description de la section"
      rows="3"
      class="mb-1 nodrag"
      max-rows="10"
      v-model="props.section.values.description"
    />
    <div class="d-flex justify-content-between mt-25">
      <div v-if="!isTemplate" class="d-flex" style="gap: 1.2rem">
        <span
          @click="
            constructorStore.removeSection(props.section.id as string)
          "
        >
          <vue-feather type="trash-2" size="22" class="cursor-pointer" />
        </span>
        <b-nav-item-dropdown class="duplicate-dropdown">
          <template #button-content>
            <span>
              <vue-feather type="copy" size="22" class="cursor-pointer" />
            </span>
          </template>
          <b-dropdown-item
            link-class="d-flex align-items-center"
            @click="
              constructorStore.duplicateSection(props.section.id as string)
            "
          >
            <vue-feather size="16" type="chevron-down" class="mr-50" />
            <span>En dessous</span>
          </b-dropdown-item>
          <b-dropdown-item
            link-class="d-flex align-items-center"
            @click="
              constructorStore.dupplicateAtTheEnd(
                props.section.id as string
              )
            "
          >
            <vue-feather size="16" type="arrow-down" class="mr-50" />
            <span>Tout en bas</span>
          </b-dropdown-item>
        </b-nav-item-dropdown>
      </div>
      <div v-else />
      <div class="font-medium-1">
        <template v-if="props.section.values.discountType !== null">
          Remise de :
          <span class="font-weight-bolder text-warning mr-4">
            {{ props.section.values.discount }}
            {{
              props.section.values.discountType === 'percentage'
                ? '%'
                : '€'
            }}
          </span>
        </template>
        Total HT :
        <span class="font-weight-bolder text-primary"
          >&nbsp;{{ constructorStore.isAvoir ? '-' : '' }}{{ totalHT }} €
        </span>
      </div>
    </div>
  </div>

  <b-modal title="Paramètres de l'article" ref="modal" size="lg">
    <b-row>
      <b-col md="6">
        <b-form-group label="Type de l'article">
          <v-select
            v-model="props.section.values.articleType"
            :options="[
              {
                label: 'Service',
                value: 'service'
              },
              {
                label: 'Produit',
                value: 'product'
              }
            ]"
            :reduce="(option) => option.value"
            :clearable="false"
          />
        </b-form-group>
      </b-col>
      <b-col md="6">
        <b-form-group label="Unité">
          <v-select
            :options="[
              {
                label: 'Aucune',
                value: ''
              },
              {
                label: 'mm',
                value: 'mm'
              },
              {
                label: 'cm',
                value: 'cm'
              },
              {
                label: 'm',
                value: 'm'
              },
              {
                label: 'km',
                value: 'km'
              },
              {
                label: 'm²',
                value: 'm²'
              },
              {
                label: 'm³',
                value: 'm³'
              },
              {
                label: 'kg',
                value: 'kg'
              },
              {
                label: 'heure(s)',
                value: 'hour'
              },
              {
                label: 'jour(s)',
                value: 'day'
              },
              {
                label: 'mois',
                value: 'month'
              },
              {
                label: 'année(s)',
                value: 'year'
              },
              {
                label: 'ml',
                value: 'ml'
              },
              {
                label: 'Litre(s)',
                value: 'l'
              }
            ]"
            :clearable="false"
            :reduce="(option) => option.value"
            v-model="props.section.values.unit"
          />
        </b-form-group>
      </b-col>
      <b-col md="6">
        <b-form-group label="Type de remise">
          <v-select
            :clearable="false"
            :options="[
              {
                label: 'Aucune',
                value: null
              },
              {
                label: 'Montant HT',
                value: 'amount'
              },
              {
                label: 'Pourcentage HT',
                value: 'percentage'
              }
            ]"
            :reduce="(option) => option.value"
            v-model="props.section.values.discountType"
          />
        </b-form-group>
      </b-col>
      <b-col
        v-if="props.section.values.discountType === 'percentage'"
        md="6"
      >
        <b-form-group label="Pourcentage de remise HT">
          <b-input-group append="%">
            <input
              class="form-control"
              type="number"
              step="0.01"
              min="0"
              placeholder="Pourcentage de remise"
              v-model="props.section.values.discount"
            />
          </b-input-group>
        </b-form-group>
      </b-col>
      <b-col v-if="props.section.values.discountType === 'amount'" md="6">
        <b-form-group label="Montant de remise HT">
          <b-input-group append="€">
            <input
              class="form-control"
              type="number"
              step="0.01"
              min="0"
              :max="
                props.section.values.unitPriceHT *
                props.section.values.quantity
              "
              placeholder="Montant de remise"
              v-model="props.section.values.discount"
            />
          </b-input-group>
        </b-form-group>
      </b-col>
      <b-col v-if="props.section.values.discountType !== null" md="6">
        <b-form-group label="Description de la remise">
          <b-form-input
            type="text"
            placeholder="Description de la remise"
            v-model="props.section.values.discountDescription"
          />
        </b-form-group>
      </b-col>
      <b-col md="6">
        <b-form-group
          class="mt-1"
          description="Affiche ou cache le prix unitaire, la remise, l'unité, la quantité et la TVA de l'article"
        >
          <b-form-checkbox
            v-model="props.section.values.displayPriceInfos"
          >
            Afficher les informations de l'article</b-form-checkbox
          >
        </b-form-group>
      </b-col>
    </b-row>
    <template #modal-footer="{ ok }">
      <b-button variant="outline-secondary" v-ripple @click="ok">
        Fermer
      </b-button>
    </template>
  </b-modal>
</template>

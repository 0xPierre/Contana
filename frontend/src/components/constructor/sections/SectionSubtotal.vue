<script lang="ts" setup>
import { Section, SectionsType } from '@/types/constructor.types.ts'
import { useConstructorStore } from '@/stores/apps/Constructor.ts'

const props = defineProps<{
  section: Section<SectionsType.Subtotal>
}>()

const constructorStore = useConstructorStore()
</script>

<template>
  <div class="section section-subtotal">
    <b-row>
      <b-col cols="5">
        <h5 class="mb-0 font-small-5">Sous total</h5>
        <div class="d-flex mt-1" style="gap: 1.2rem">
          <span @click="constructorStore.removeSection(section.id)">
            <vue-feather type="trash-2" size="22" class="cursor-pointer" />
          </span>
          <b-nav-item-dropdown class="duplicate-dropdown">
            <template #button-content>
              <span>
                <vue-feather
                  type="copy"
                  size="22"
                  class="cursor-pointer"
                />
              </span>
            </template>
            <b-dropdown-item
              link-class="d-flex align-items-center"
              @click="
                constructorStore.duplicateSection(
                  props.section.id as string
                )
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
      </b-col>
      <b-col cols="4">
        <b-form-input
          placeholder="Titre du sous total"
          type="text"
          class="no-drag"
          v-model="section.values.title"
        />
      </b-col>
      <b-col cols="3">
        <b-input-group append="€">
          <b-form-input
            placeholder="Prix du sous total"
            class="no-drag"
            :value="`${
              constructorStore.isAvoir ? '-' : ''
            }${constructorStore.subtotals[section.id].format()}`"
            :disabled="true"
          />
        </b-input-group>
      </b-col>
    </b-row>
  </div>
</template>

<script lang="ts" setup>
import { Section, SectionsType } from '@/types/constructor.types.ts'
import { useConstructorStore } from '@/stores/apps/Constructor.ts'

const props = defineProps<{
  section: Section<SectionsType.Subtotal>
}>()

const constructoreStore = useConstructorStore()
</script>

<template>
  <div class="section section-subtotal">
    <b-row>
      <b-col cols="5">
        <h5 class="mb-0 font-small-5">Sous total</h5>
        <div class="d-flex mt-1" style="gap: 1.2rem">
          <span @click="constructoreStore.removeSection(section.id)">
            <vue-feather type="trash-2" size="22" class="cursor-pointer" />
          </span>
          <span @click="constructoreStore.duplicateSection(section.id)">
            <vue-feather type="copy" size="22" class="cursor-pointer" />
          </span>
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
            :value="constructoreStore.subtotals[section.id].format()"
            :disabled="true"
          />
        </b-input-group>
      </b-col>
    </b-row>
  </div>
</template>

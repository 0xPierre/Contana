<script lang="ts" setup>
import { Section, SectionsType } from '@/types/constructor.types.ts'
import { useConstructorStore } from '@/stores/apps/Constructor.ts'

const props = defineProps<{
  section: Section<SectionsType.Title>
}>()

const constructoreStore = useConstructorStore()
</script>

<template>
  <div class="section section-title">
    <b-row>
      <b-col cols="5">
        <h5 class="mb-0 font-small-5">Titre de section</h5>
        <div class="d-flex mt-1" style="gap: 1.2rem">
          <span @click="constructoreStore.removeSection(section.id)">
            <vue-feather type="trash-2" size="22" class="cursor-pointer" />
          </span>
          <span @click="constructoreStore.duplicateSection(section.id)">
            <vue-feather type="copy" size="22" class="cursor-pointer" />
          </span>
        </div>
      </b-col>
      <b-col cols="7">
        <b-form-input
          placeholder="Titre de la section"
          type="text"
          v-model="section.values.title"
        />
      </b-col>
    </b-row>
  </div>
</template>

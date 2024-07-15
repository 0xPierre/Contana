<script lang="ts" setup>
import SectionArticle from '@/components/constructor/sections/SectionArticle.vue'

SectionArticle
import { Section, SectionsType } from '@/types/constructor.types.ts'
import { useConstructorStore } from '@/stores/apps/Constructor.ts'

const props = defineProps<{
  section: Section<SectionsType.Title>
}>()

const constructorStore = useConstructorStore()
</script>

<template>
  <div class="section section-title">
    <b-row>
      <b-col cols="5">
        <h5 class="mb-0 font-small-5">Titre de section</h5>
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

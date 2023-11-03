<script setup lang="ts">
import { useEntrepriseStore } from '@/stores/apps/Entreprise.ts'
import { useUserStore } from '@/stores/apps/User.ts'
import { fullNameToText } from '@/helpers/utils.ts'
import { ref } from 'vue'

const entrepriseStore = useEntrepriseStore()
const userStore = useUserStore()

const isOpen = ref(false)
</script>

<template>
  <div>
    <div v-if="userStore.data?.entreprises.length === 0">
      <b-button
        variant="flat-primary"
        class="btn-with-icon"
        size="sm"
        v-ripple
      >
        <vue-feather type="plus-square" :size="20" />
        <span class="ml-50"> Créer une entreprise </span>
      </b-button>
    </div>
    <div v-else>
      <b-nav-item-dropdown
        style="list-style: none"
        toggle-class="p-0"
        menu-class="mt-50"
        @show="isOpen = true"
        @hide="isOpen = false"
      >
        <template #button-content>
          <b-button
            variant="flat-secondary"
            class="btn-with-icon"
            size="sm"
            v-ripple
          >
            <vue-feather
              :type="isOpen ? 'chevron-down' : 'chevron-right'"
              :size="20"
            />
            <span class="ml-25">
              {{ entrepriseStore.entreprise?.name }}</span
            >
          </b-button>
        </template>

        <b-dropdown-item link-class="d-flex align-items-center">
          <vue-feather type="plus-square" :size="20" />
          <span class="ml-50"> Créer une entreprise </span>
        </b-dropdown-item>

        <b-dropdown-divider />

        <b-dropdown-item
          v-for="entreprise in userStore.data?.entreprises"
          :key="entreprise.id"
          link-class="d-flex align-items-center"
          :active="entreprise.id === entrepriseStore.entreprise?.id"
          @click="userStore.selectEntreprise(entreprise.slug)"
        >
          {{ entreprise.name }}
        </b-dropdown-item>
      </b-nav-item-dropdown>
    </div>
  </div>
</template>

<style scoped lang="scss"></style>

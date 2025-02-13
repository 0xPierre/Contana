<script setup lang="ts">
import { useEntrepriseStore } from '@/stores/apps/Entreprise.ts'
import { useUserStore } from '@/stores/apps/User.ts'
import { fullNameToText } from '@/helpers/utils.ts'
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()
const entrepriseStore = useEntrepriseStore()
const userStore = useUserStore()

const isOpen = ref(false)

const selectEntreprise = async (slug: string) => {
  await userStore.selectEntreprise(slug)
  if (
    entrepriseStore?.entreprise?.user_permissions.access_dashboard &&
    route.name === 'entreprise-dashboard'
  ) {
    router.push({
      name: 'entreprise-dashboard',
      params: { entrepriseSlug: slug }
    })
  } else if (
    entrepriseStore?.entreprise?.user_permissions.access_documents &&
    route.name === 'entreprise-documents'
  ) {
    router.push({
      name: 'entreprise-documents',
      params: { entrepriseSlug: slug }
    })
  } else if (
    entrepriseStore?.entreprise?.user_permissions.access_clients &&
    route.name === 'entreprise-clients'
  ) {
    router.push({
      name: 'entreprise-clients',
      params: { entrepriseSlug: slug }
    })
  } else if (
    entrepriseStore?.entreprise?.user_permissions.access_constructor &&
    route.name === 'entreprise-constructor'
  ) {
    router.push({
      name: 'entreprise-constructor',
      params: { entrepriseSlug: slug }
    })
  } else if (
    entrepriseStore?.entreprise?.user_permissions.access_crm &&
    route.name === 'entreprise-tasks'
  ) {
    router.push({
      name: 'entreprise-tasks',
      params: { entrepriseSlug: slug }
    })
  } else if (
    entrepriseStore?.entreprise?.user_permissions.administrate &&
    route.name === 'entreprise-settings'
  ) {
    router.push({
      name: 'entreprise-settings',
      params: { entrepriseSlug: slug }
    })
  } else {
    router.push({ name: 'home' })
  }
}
</script>

<template>
  <div>
    <div v-if="userStore.data?.entreprises.length === 0">
      <b-button
        variant="flat-primary"
        class="btn-with-icon"
        size="sm"
        v-ripple
        :to="{ name: 'entreprise-create' }"
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

        <b-dropdown-item
          link-class="d-flex align-items-center"
          :to="{ name: 'entreprise-create' }"
        >
          <vue-feather type="plus-square" :size="20" />
          <span class="ml-50"> Créer une entreprise </span>
        </b-dropdown-item>

        <b-dropdown-divider />

        <b-dropdown-item
          v-for="entreprise in userStore.data?.entreprises"
          :key="entreprise.id"
          :link-class="`d-flex align-items-center ${
            entreprise.stripe_payment_status != 'paid'
              ? 'text-danger font-weight-bolder'
              : ''
          }`"
          :active="entreprise.id === entrepriseStore.entreprise?.id"
          @click="selectEntreprise(entreprise.slug)"
        >
          {{ entreprise.name }}
        </b-dropdown-item>
      </b-nav-item-dropdown>
    </div>
  </div>
</template>

<style scoped lang="scss"></style>

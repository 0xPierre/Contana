<script lang="ts" setup>
import DarkToggler from './components/DarkToggler.vue'
import UserDropdown from './components/UserDropdown.vue'
import EntrepriseSelector from '@/layouts/components/app-navbar/components/EntrepriseSelector.vue'

defineProps<{
  toggleVerticalMenuActive: () => void
}>()
</script>

<template>
  <div class="navbar-container d-flex content align-items-center">
    <ul class="nav navbar-nav d-xl-none">
      <li class="nav-item">
        <b-link class="nav-link" @click="toggleVerticalMenuActive">
          <vue-feather type="menu" size="21" />
        </b-link>
      </li>
    </ul>

    <EntrepriseSelector />

    <b-navbar-nav class="nav align-items-center ml-auto">
      <DarkToggler class="d-block" />
      <UserDropdown />
    </b-navbar-nav>
  </div>
</template>

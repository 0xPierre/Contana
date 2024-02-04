<script lang="ts" setup>
import { useAppConfigStore } from '@/stores/AppConfig'
import { computed } from 'vue'

const appConfigStore = useAppConfigStore()

const isDark = computed(() => appConfigStore.theme === 'dark')
</script>

<template>
  <b-nav-item @click="appConfigStore.toggleTheme" class="mt-50">
    <vue-feather size="21" :type="`${isDark ? 'sun' : 'moon'}`" />
  </b-nav-item>
</template>

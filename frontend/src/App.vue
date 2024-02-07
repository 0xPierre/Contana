<script setup lang="ts">
import { computed, onBeforeMount, ref, watch } from 'vue'
import { RouterView } from 'vue-router'
import { useRoute } from 'vue-router'
import { useAppConfigStore } from '@/stores/AppConfig'
import { useUserStore } from '@/stores/apps/User'

const appConfigStore = useAppConfigStore()
const userStore = useUserStore()

const route = useRoute()

const LayoutFull = () => import('@/layouts/layout-full/LayoutFull.vue')
const LayoutVertical = () =>
  import('@/layouts/layout-vertical/LayoutVertical.vue')

const layout = computed(() => {
  if (!route.meta.layout || route.meta.layout === 'layout-full')
    return LayoutFull

  return LayoutVertical
})

if (appConfigStore.theme === 'dark') {
  document.body.classList.add('dark-layout')
}

onBeforeMount(() => {
  document.documentElement.setAttribute('dir', 'ltr')
})

const dataHasBeeGetted = ref(false)
watch(
  () => route.params.entrepriseSlug,
  () => {
    if (userStore.auth.isLoggedIn && !dataHasBeeGetted.value) {
      userStore.getData(route.params.entrepriseSlug as string)
      dataHasBeeGetted.value = true
    }
  }
)
</script>

<template>
  <div id="app" class="h-100">
    <component :is="layout">
      <RouterView />
    </component>
  </div>
</template>

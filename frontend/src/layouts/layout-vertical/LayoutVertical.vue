<script lang="ts" setup>
import { useAppConfigStore } from '@/stores/AppConfig'
import useVerticalLayout from './useVerticalLayout'
import AppNavbarVerticalLayout from '../components/app-navbar/AppNavbarVerticalLayout.vue'
import VerticalNavMenu from './vertical-nav-menu/VerticalNavMenu.vue'
import { onUnmounted } from 'vue'

const appConfigStore = useAppConfigStore()

const {
  isVerticalMenuActive,
  toggleVerticalMenuActive,
  isVerticalMenuCollapsed,
  layoutClasses,
  overlayClasses,
  resizeHandler,
  navbarTypeClass,
  footerTypeClass
} = useVerticalLayout(
  appConfigStore.navbar.type,
  appConfigStore.footer.type
)

resizeHandler()
window.addEventListener('resize', resizeHandler)
onUnmounted(() => {
  window.removeEventListener('resize', resizeHandler)
})
</script>

<template>
  <div class="vertical-layout h-100" :class="[layoutClasses]">
    <b-navbar
      :toggleable="false"
      :variant="appConfigStore.navbar.backgroundColor"
      class="header-navbar navbar navbar-shadow align-items-center"
      :class="navbarTypeClass"
    >
      <slot
        name="navbar"
        :toggleVerticalMenuActive="toggleVerticalMenuActive"
        :navbarBackgroundColor="appConfigStore.navbar.backgroundColor"
        :navbarTypeClass="[
          ...navbarTypeClass,
          'header-navbar navbar navbar-shadow align-items-center'
        ]"
      >
        <AppNavbarVerticalLayout
          :toggle-vertical-menu-active="toggleVerticalMenuActive"
        />
      </slot>
    </b-navbar>

    <VerticalNavMenu
      :is-vertical-menu-active="isVerticalMenuActive"
      :toggle-vertical-menu-active="toggleVerticalMenuActive"
    >
      <template #header="slotProps">
        <slot name="vertical-menu-header" v-bind="slotProps" />
      </template>
    </VerticalNavMenu>

    <div
      class="sidenav-overlay"
      :class="overlayClasses"
      @click="isVerticalMenuActive = false"
    />

    <RouterView v-slot="{ Component }">
      <Transition name="zoom-fade" mode="out-in">
        <div
          class="app-content content"
          :class="[$route.meta.contentClass]"
        >
          <div class="content-overlay" />
          <div class="header-navbar-shadow" />
          <div class="content-wrapper">
            <div class="content-body">
              <Transition name="zoom-fade" mode="out-in">
                <component :is="Component" />
              </Transition>
            </div>
          </div>
        </div>
      </Transition>
    </RouterView>
  </div>
</template>

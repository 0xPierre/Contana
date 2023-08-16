<script lang="ts" setup>
// import navMenuItems from '@/navigation/vertical'
// @ts-ignore
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
import { provide, computed, ref } from 'vue'
// import useAppConfig from '@core/app-config/useAppConfig'
// import { $themeConfig } from '@themeConfig'
import VerticalNavMenuItems from './components/vertical-nav-menu-items/VerticalNavMenuItems.vue'
// import useVerticalNavMenu from './useVerticalNavMenu'
import { useAppConfigStore } from '@/stores/AppConfig'

const appConfigStore = useAppConfigStore()

defineProps<{
  isVerticalMenuActive: boolean
  toggleVerticalMenuActive: () => void
}>()

const shallShadowBottom = ref(false)

const isMouseHovered = ref(false)
provide('isMouseHovered', isMouseHovered)

const perfectScrollbarSettings = {
  maxScrollbarLength: 60,
  wheelPropagation: false
}

const collapseTogglerIconFeather = computed(() =>
  collapseTogglerIcon.value === 'unpinned' ? 'circle' : 'disc'
)

const collapseTogglerIcon = computed(() => {
  if (appConfigStore.isVerticalMenuCollapsed) {
    return appConfigStore.isVerticalMenuCollapsed ? 'unpinned' : 'pinned'
  }
  return 'close'
})
</script>

<template>
  <div
    class="main-menu menu-fixed menu-accordion menu-shadow"
    :class="[
      {
        expanded:
          !appConfigStore.isVerticalMenuCollapsed ||
          (appConfigStore.isVerticalMenuCollapsed && isMouseHovered)
      },
      'menu-light'
    ]"
    @mouseenter="isMouseHovered = true"
    @mouseleave="isMouseHovered = false"
  >
    <div class="navbar-header expanded">
      <slot
        name="header"
        :toggleVerticalMenuActive="toggleVerticalMenuActive"
        :toggleCollapsed="appConfigStore.toggleVerticalMenuCollapsed"
        :collapseTogglerIcon="collapseTogglerIcon"
      >
        <ul class="nav navbar-nav flex-row">
          <!-- Logo & Text -->
          <li class="nav-item mr-auto">
            <b-link class="navbar-brand" to="/">
              <span class="brand-logo">
                <!-- <b-img :src="appLogoImage" alt="logo" /> -->
              </span>
              <h2 class="brand-text">Contana</h2>
            </b-link>
          </li>
          <!-- Toggler Button -->
          <li class="nav-item nav-toggle">
            <b-link class="nav-link modern-nav-toggle">
              <div @click="toggleVerticalMenuActive">
                <vue-feather
                  type="x"
                  size="20"
                  class="d-block d-xl-none"
                />
              </div>
              <div @click="appConfigStore.toggleVerticalMenuCollapsed()">
                <vue-feather
                  :type="collapseTogglerIconFeather"
                  size="20"
                  class="d-none d-xl-block collapse-toggle-icon"
                />
              </div>
            </b-link>
          </li>
        </ul>
      </slot>
    </div>
    <!-- / main menu header-->

    <!-- Shadow -->
    <div :class="{ 'd-block': shallShadowBottom }" class="shadow-bottom" />

    <!-- main menu content-->
    <vue-perfect-scrollbar
      :settings="perfectScrollbarSettings"
      class="main-menu-content scroll-area"
      tagname="ul"
      @ps-scroll-y="
        (evt: any) => {
          shallShadowBottom = evt.srcElement.scrollTop > 0
        }
      "
    >
      <VerticalNavMenuItems class="navigation navigation-main" />
    </vue-perfect-scrollbar>
    <!-- /main menu content-->
  </div>
</template>

<style lang="scss">
// @import "~@core/scss/base/core/menu/menu-types/vertical-menu.scss";
@import '@/assets/scss/template/base/core/menu/menu-types/vertical-menu.scss';
</style>

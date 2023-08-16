<script lang="ts" setup>
import { resolveVerticalNavMenuItemComponent as resolveNavItemComponent } from '@/layouts/utils'
import VerticalNavMenuHeader from '../vertical-nav-menu-header/VerticalNavMenuHeader.vue'
import VerticalNavMenuLink from '../vertical-nav-menu-link/VerticalNavMenuLink.vue'
import type { MenuLink } from '@/layouts/menu.type'
import { onMounted, ref } from 'vue'

// import useVerticalNavMenuGroup from './useVerticalNavMenuGroup'

defineProps<{
  item: MenuLink
}>()
// const { isOpen, isActive, updateGroupOpen, updateIsActive } =
//   useVerticalNavMenuGroup(props.item)
// onMounted(() => {
//   updateIsActive()
// })

const isOpen = ref(false)
const isActive = ref(false)

const updateGroupOpen = (value: boolean) => {
  isOpen.value = value
}
</script>

<template>
  <li
    class="nav-item has-sub"
    :class="{
      open: isOpen,
      disabled: item.disabled,
      'sidebar-group-active': isActive
    }"
  >
    <b-link
      class="d-flex align-items-center"
      @click="() => updateGroupOpen(!isOpen)"
    >
      <vue-feather :type="item.icon || 'circle'" />
      <span class="menu-title text-truncate">{{ item.title }}</span>
      <b-badge
        v-if="item.tag"
        pill
        :variant="item.tagVariant || 'primary'"
        class="mr-1 ml-auto"
      >
        {{ item.tag }}
      </b-badge>
    </b-link>
    <b-collapse v-model="isOpen" class="menu-content" tag="ul">
      <component
        :is="resolveNavItemComponent(child)"
        v-for="child in item.children"
        :key="child.header || child.title"
        ref="groupChild"
        :item="child"
      />
    </b-collapse>
  </li>
</template>

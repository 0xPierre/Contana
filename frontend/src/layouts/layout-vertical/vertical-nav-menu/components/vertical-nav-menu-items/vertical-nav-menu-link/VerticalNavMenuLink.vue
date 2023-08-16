<script lang="ts" setup>
import useVerticalNavMenuLink from './useVerticalNavMenuLink'
import { watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { MenuLink } from '@/layouts/menu.type'

const route = useRoute()

const props = defineProps<{
  item: MenuLink
}>()

const { isActive, linkProps, updateIsActive } = useVerticalNavMenuLink(
  props.item
)

onMounted(() => {
  updateIsActive()
})

watch(
  () => route.path,
  () => {
    updateIsActive()
  }
)
</script>

<template>
  <li
    class="nav-item"
    :class="{
      active: isActive,
      disabled: item.disabled
    }"
  >
    <b-link v-bind="linkProps" class="d-flex align-items-center">
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
  </li>
</template>

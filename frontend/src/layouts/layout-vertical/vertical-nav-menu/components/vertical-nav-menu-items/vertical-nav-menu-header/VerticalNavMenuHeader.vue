<script setup lang="ts">
import type { MenuLink } from '@/layouts/menu.type'

defineProps<{
  item: MenuLink
}>()
</script>

<template>
  <li class="navigation-header text-truncate">
    <span>
      {{ item.header }}
    </span>
    <vue-feather type="more-horizontal" szie="18" />
  </li>
</template>

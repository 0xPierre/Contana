<template>
  <ul v-bind="$attrs" class="app-timeline">
    <slot />
  </ul>
</template>

<script>
export default {}
</script>
<style lang="scss" scoped>
.app-timeline {
  list-style: none;
  padding: 0;
  position: relative;
  margin: 0 0 0 1rem;
}
</style>

<script setup lang="ts">
interface Props {
  title: string
  value: string
  icon: string
  variant: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'light-info',
  icon: 'check-circle'
})
</script>

<template>
  <b-card no-body class="mb-1">
    <div class="d-flex p-1 align-items-center">
      <b-avatar :variant="variant" size="lg">
        <vue-feather :type="icon" size="21" />
      </b-avatar>
      <div class="ml-1">
        <div>{{ title }}</div>
        <div class="font-weight-bolder font-medium-3">
          {{ value }}
        </div>
      </div>
    </div>
  </b-card>
</template>

<script setup lang="ts">
import { ClientStatusEnum } from '@/types/clients.types.ts'

interface Props {
  status: ClientStatusEnum
}
const { status } = defineProps<Props>()
</script>

<template>
  <div>
    <b-badge
      v-if="status === ClientStatusEnum.ARCHIVED"
      variant="light-secondary"
    >
      Archivé
    </b-badge>
    <b-badge
      v-else-if="status === ClientStatusEnum.SUSPECT"
      variant="light-warning"
    >
      Suspect
    </b-badge>
    <b-badge
      v-else-if="status === ClientStatusEnum.PROSPECT"
      variant="light-primary"
    >
      Prospect
    </b-badge>
    <b-badge
      v-else-if="status === ClientStatusEnum.CLIENT"
      variant="light-success"
    >
      Client
    </b-badge>
  </div>
</template>

<style scoped lang="scss"></style>

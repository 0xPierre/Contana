<script lang="ts" setup>
import { DocumentsState } from '@/types/documents.types.ts'
import { DocumentStateBadgeInfo } from '@/helpers/documents.ts'

const props = defineProps<{
  state: DocumentsState
}>()
</script>

<template>
  <div class="document-state-badge">
    <b-badge
      :variant="DocumentStateBadgeInfo[state].color"
      class="text-capitalize"
    >
      {{ DocumentStateBadgeInfo[state].text }}
    </b-badge>
  </div>
</template>

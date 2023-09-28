<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  useRouter,
  type HistoryState,
  type LocationQuery
} from 'vue-router'

const props = defineProps<{
  text: string
  to: LocationQuery | HistoryState
}>()

const router = useRouter()
const backRoute = ref<HistoryState | string>('')

onMounted(() => {
  // backRoute.value = router.options.history.state.back as HistoryState
})
</script>

<template>
  <RouterLink :to="backRoute ? backRoute : to" class="back-button">
    <vue-feather type="arrow-left" size="18" />
    <span>
      {{ text }}
    </span>
  </RouterLink>
</template>

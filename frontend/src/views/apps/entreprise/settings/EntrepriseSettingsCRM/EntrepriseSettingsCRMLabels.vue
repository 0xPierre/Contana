<script lang="ts" setup>
import { useTasksStore } from '@/stores/apps/Tasks'
import type { Label } from '@/types/tasks.types'
import { onMounted, reactive, ref } from 'vue'

const tasksStore = useTasksStore()
const localLabels = ref<Omit<Label, 'id'>[]>([])
const isLoading = ref(false)

onMounted(async () => {
  isLoading.value = true
  await tasksStore.getLabels()
  localLabels.value = tasksStore.labels

  isLoading.value = false
})

const addLabel = () => {
  localLabels.value.push({ label: '', color: '#ff0000' })
}
</script>

<template>
  <b-overlay :show="isLoading">
    {{ tasksStore.labels }}
    <b-card title="Labels">
      <div v-for="(label, i) in localLabels" :key="i" class="d-flex gap-2">
        <div class="d-flex mb-50">
          <b-input class="w-100" v-model="label.label" blc />
          <b-input type="color" class="w-20" v-model="label.color" blc />
        </div>
      </div>
      <b-button
        variant="outline-primary"
        size="sm"
        class="btn-with-icon"
        @click="addLabel"
      >
        <vue-feather type="plus" size="18" class="mr-50" />
        Nouveau label
      </b-button>
    </b-card>
  </b-overlay>
</template>

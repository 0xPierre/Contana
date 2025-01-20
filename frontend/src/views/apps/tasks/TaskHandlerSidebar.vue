<script lang="ts" setup>
import { ref, Ref, watch } from 'vue'
import { Task } from '@/types/tasks.types'

interface Props {
  isTaskHandlerSidebarActive: boolean
  task: Task
}

const props = defineProps<Props>()
const emits = defineEmits([
  'update:is-task-handler-sidebar-active',
  'delete-task',
  'create-task',
  'update-task'
])

const createOrUpdateTask = () => {
  if (props.task.id) {
    emits('update-task', props.task)
  } else {
    emits('create-task', props.task)
  }
}
</script>

<template>
  <div>
    <b-sidebar
      id="sidebar-task-handler"
      sidebar-class="sidebar-lg"
      :visible="isTaskHandlerSidebarActive"
      bg-variant="white"
      shadow
      backdrop
      no-header
      right
      @change="
        (val: boolean) =>
          emits('update:is-task-handler-sidebar-active', val)
      "
    >
      <template #default="{ hide }">
        <div
          class="d-flex justify-content-between align-items-center content-sidebar-header px-2 py-1"
        >
          <b-button
            v-if="task.id"
            size="sm"
            :variant="
              task.checked ? 'outline-success' : 'outline-secondary'
            "
            @click="task.checked = !task.checked"
          >
            {{ task.checked ? 'Complété' : 'Marquer comme terminé' }}
          </b-button>
          <h5 v-else class="mb-0">Ajouter une tâche</h5>
          <div class="d-flex align-items-center">
            <div
              @click="
                () => {
                  $emit('delete-task')
                  hide()
                }
              "
            >
              <vue-feather
                v-show="task.id"
                type="trash"
                class="cursor-pointer"
                size="22"
              />
            </div>
            <div @click="hide">
              <vue-feather
                class="ml-1 cursor-pointer"
                type="x"
                size="22"
              />
            </div>
          </div>
        </div>

        <b-form @submit.prevent="createOrUpdateTask" class="p-2">
          <b-form-group label="Titre" label-for="task-title">
            <b-form-input
              id="task-title"
              ref="task-title"
              v-model="task.title"
              autofocus
              trim
              placeholder="Titre de la tâche"
            />
          </b-form-group>
          <b-form-group label="Date d'échéance" label-for="due-date">
            <flat-pickr
              v-model="task.due_date"
              class="form-control"
              :config="{
                locale: 'fr',
                dateFormat: 'Y-m-d',
                altInput: true,
                altFormat: 'Y-m-d'
              }"
            />
          </b-form-group>
          <b-form-group label="Description" label-for="task-description">
            <b-form-textarea
              v-model="task.description"
              placeholder="Écrivez la description de la tâche ici..."
              rows="4"
            />
          </b-form-group>

          <b-button
            v-ripple.400="'rgba(255, 255, 255, 0.15)'"
            variant="primary"
            class="mr-2"
            type="submit"
          >
            {{ task.id ? 'Enregistrer' : 'Ajouter ' }}
          </b-button>
        </b-form>
      </template>
    </b-sidebar>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, watch } from 'vue'
import TasksSidebar from './TasksSidebar.vue'
import TaskHandlerSidebar from './TaskHandlerSidebar.vue'
import { useTasksStore } from '@/stores/apps/Tasks'
import notifcationSound from '@/assets/sounds/notification1.wav'
import { Task } from '@/types/tasks.types'
import strftime from 'strftime'
import { notify } from '@/helpers/notify'

const onCheck = async (task: Task) => {
  if (!task.checked) {
    // new Audio(notifcationSound).play()
  }
  task.checked = !task.checked
  await updateTask(task)
}

const getHumanDate = (date: string) => {
  const today = new Date()
  const taskDate = new Date(date)

  if (today.toDateString() === taskDate.toDateString()) {
    return "Aujourd'hui"
  }

  today.setDate(today.getDate() - 1)
  if (today.toDateString() === taskDate.toDateString()) {
    return 'Hier'
  }

  today.setDate(today.getDate() + 2)
  if (today.toDateString() === taskDate.toDateString()) {
    return 'Demain'
  }

  return strftime('%d/%m/%Y', taskDate)
}

const isTaskHandlerSidebarActive = ref(false)
const localTask = ref<Partial<Task>>({
  id: null,
  title: '',
  description: '',
  due_date: new Date().toISOString(),
  checked: false
})

const createTaskHandlerSidebar = () => {
  isTaskHandlerSidebarActive.value = true
  localTask.value = {
    id: null,
    title: '',
    description: '',
    due_date: new Date().toISOString(),
    checked: false
  }
}

const updateTaskHandlerSidebar = (task: Task) => {
  isTaskHandlerSidebarActive.value = true
  localTask.value = { ...task }
}

const createTask = async () => {
  try {
    await taskStore.createTask(localTask.value as Task)
  } catch {
    notify("Erreur lors de la création d'une tâche.", 'danger')
  }
  isTaskHandlerSidebarActive.value = false
  await taskStore.getTasks()
}

const deleteTask = async () => {
  console.log('delete task')
  try {
    await taskStore.deleteTask(localTask.value as Task)
    await taskStore.getTasks()
  } catch {
    notify("Erreur lors de la suppression d'une tâche.", 'danger')
  }
}

const updateTask = async (task: Task | null) => {
  task = task ?? (localTask.value as Task)

  try {
    await taskStore.updateTask(task)
  } catch {
    notify("Erreur lors de la modification d'une tâche.", 'danger')
  }
  isTaskHandlerSidebarActive.value = false
  await taskStore.getTasks()
}

const taskStore = useTasksStore()

onMounted(() => {
  taskStore.getTasks()
})

watch(
  () => taskStore.filters,
  () => {
    taskStore.getTasks()
  },
  { deep: true }
)
</script>

<template>
  <div class="todo-application">
    <div class="content-area-wrapper h-100">
      <TasksSidebar @add-task="createTaskHandlerSidebar" />
      <div class="content-right">
        <div class="content-wrapper">
          <div class="content-body">
            <div class="todo-app-list">
              <div
                class="app-fixed-search d-flex align-items-center p-75 p-md-0"
              >
                <div
                  class="align-content-center justify-content-between w-100 d-none d-md-flex"
                >
                  <b-input-group class="input-group-merge">
                    <b-input-group-prepend is-text>
                      <vue-feather type="search" class="text-muted" />
                    </b-input-group-prepend>
                    <b-form-input
                      placeholder="Rechercher des tâches"
                      v-model="taskStore.filters.search"
                      debounce="300"
                    />
                  </b-input-group>
                </div>
                <div>
                  <v-select
                    v-model="taskStore.filters.completed"
                    class="completed"
                    :options="[
                      { label: 'Complété Jamais', value: 'never' },
                      { label: 'Complété Aujourd\'hui', value: 'today' },
                      { label: 'Complété Toujours', value: 'always' }
                    ]"
                    style="min-width: 300px"
                    :reduce="(option: any) => option.value"
                    :clearable="false"
                  />
                </div>
              </div>
              <vue-perfect-scrollbar
                :settings="{
                  maxScrollbarLength: 150
                }"
                class="todo-task-list-wrapper list-group scroll-area h-100"
              >
                <ul
                  handle=".draggable-task-handle"
                  tag="ul"
                  class="todo-task-list media-list"
                >
                  <li
                    v-for="task in taskStore.tasks"
                    :key="task.id as number"
                    class="todo-item"
                    :class="{
                      completed: task.checked
                    }"
                    @click.self="updateTaskHandlerSidebar(task)"
                  >
                    <!-- <vue-feather
                      type="more-vertical"
                      class="draggable-task-handle d-inline"
                    /> -->
                    <div
                      class="todo-title-wrapper"
                      @click.self="updateTaskHandlerSidebar(task)"
                    >
                      <div class="todo-title-area">
                        <div class="title-wrapper">
                          <!-- @click.stop.prevent doesn't work -->
                          <b-form-checkbox
                            :checked="task.checked"
                            @change="onCheck(task)"
                          />
                          <div
                            class="ml-50 text-body"
                            @click="updateTaskHandlerSidebar(task)"
                          >
                            {{ task.title }}
                          </div>
                        </div>
                      </div>
                      <div
                        class="d-flex"
                        @click="updateTaskHandlerSidebar(task)"
                      >
                        <div class="d-none">
                          <div class="badge-wrapper mr-1">
                            <b-badge
                              pill
                              :variant="`light-dark`"
                              class="text-capitalize"
                            >
                              Label 1
                            </b-badge>
                            <b-badge
                              pill
                              :variant="`light-danger`"
                              class="text-capitalize"
                            >
                              Label 2
                            </b-badge>
                          </div>
                        </div>
                        <div
                          class="badge-wrapper mr-1 d-flex justify-content-end"
                          style="min-width: 100px"
                        >
                          <b-badge
                            pill
                            :variant="`light-dark`"
                            class="text-capitalize"
                          >
                            {{ getHumanDate(task.due_date) }}
                          </b-badge>
                        </div>
                      </div>
                    </div>
                  </li>
                </ul>
                <div
                  class="no-results"
                  :class="{ show: !taskStore.tasks.length }"
                >
                  <h5>Vous n'avez aucune tâche pour le moment</h5>
                </div>
              </vue-perfect-scrollbar>
            </div>
          </div>
        </div>
      </div>
    </div>
    <TaskHandlerSidebar
      :is-task-handler-sidebar-active="isTaskHandlerSidebarActive"
      @update:is-task-handler-sidebar-active="
        isTaskHandlerSidebarActive = $event
      "
      @create-task="createTask"
      @delete-task="deleteTask"
      @update-task="updateTask"
      :task="localTask as Task"
    />
  </div>
</template>

<style lang="scss" scoped>
.todo-application {
  height: calc(100vh - 102px - 1rem - 1rem);
}
</style>

<style lang="scss">
@import '@/assets/scss/template/base/pages/app-todo.scss';

.completed {
  .vs__dropdown-toggle {
    border: none;
  }
}

.todo-app-menu {
  .list-group-item {
    &.active {
      border-color: #3c68ca !important;
    }
  }
}

.icon-sidebar {
  svg {
    display: inline;
  }
}
</style>

<style lang="scss" scoped>
.draggable-task-handle {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  visibility: hidden;
  cursor: move;

  .todo-task-list .todo-item:hover & {
    visibility: visible;
  }
}
</style>

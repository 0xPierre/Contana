<script lang="ts" setup>
import { useEntrepriseStore } from '@/stores/apps/Entreprise'
import { fullNameToText } from '@/helpers/utils'
import { useUserStore } from '@/stores/apps/User'
import { useTasksStore } from '@/stores/apps/Tasks'
import { can } from '@/helpers/permissions.ts'

const taskStore = useTasksStore()

const entrepriseStore = useEntrepriseStore()
const userStore = useUserStore()

const users = (entrepriseStore.entreprise?.users || []).filter(
  (user) => user.id !== userStore.data?.id
)
</script>

<template>
  <div class="sidebar-left">
    <div class="sidebar">
      <div class="sidebar-content todo-sidebar">
        <div class="todo-app-menu">
          <div class="add-task">
            <b-button
              variant="primary"
              block
              v-ripple
              @click="$emit('add-task')"
            >
              <span class="align-middle"> Ajouter une tâche </span>
            </b-button>
          </div>
          <vue-perfect-scrollbar
            :settings="{
              maxScrollbarLength: 60
            }"
            class="sidebar-menu-list scroll-area"
          >
            <b-list-group class="list-group-filters">
              <b-list-group-item
                class="list-group-item-action cursor-pointer"
                :class="{ active: taskStore.filters.user === null }"
                @click="taskStore.filters.user = null"
              >
                <vue-feather
                  type="mail"
                  size="18"
                  class="mr-75 d-inline icon-sidebar"
                />
                <span class="align-text-bottom line-height-1">
                  Mes tâches
                </span>
              </b-list-group-item>
            </b-list-group>

            <template v-if="can('administrate')">
              <div class="mt-1 px-2 d-flex justify-content-between">
                <h6 class="section-label mb-1">Utilisateurs</h6>
              </div>

              <b-list-group class="list-group-labels">
                <b-list-group-item
                  v-for="(user, i) in users"
                  class="cursor-pointer"
                  :key="i"
                  :class="{ active: taskStore.filters.user === user.id }"
                  @click="taskStore.filters.user = user.id"
                >
                  <b-avatar
                    size="32"
                    variant="light-warning"
                    :src="user.avatar"
                    :text="fullNameToText(user.full_name || '')"
                  />
                  <span class="ml-1 d-inline-bloc²k align-middle">
                    {{ user.full_name }}
                  </span>
                </b-list-group-item>
              </b-list-group>
            </template>
          </vue-perfect-scrollbar>
        </div>
      </div>
    </div>
  </div>
</template>

import { defineStore, acceptHMRUpdate } from 'pinia'
import http from '@/helpers/http'
import type {
  Label,
  Task,
} from '@/types/tasks.types'
import { TaskCompleted } from '@/types/tasks.types'
import type { ApiPaginatedResponse, ApiResponse } from '@/types/api.types'
import { useEntrepriseStore } from './Entreprise'

interface State {
  labels: Label[],
  filters: {
    user: number | null,
    search: '',
    completed: TaskCompleted
  },
  tasks: Task[]
}

export const useTasksStore = defineStore('tasks', {
  state: (): State => {
    return {
      labels: [],
      filters: {
        user: null,
        search: '',
        completed: TaskCompleted.today,
      },
      tasks: []
    }
  },

  getters: {},

  actions: {
    /**
     * 
     * Labels functions
     * 
     */
    async createLabel(data: Omit<Label, 'id'>) {
      const entrepriseStore = useEntrepriseStore()

      return http.post<ApiResponse<Label>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/tasks/labels/`,
        data
      )
    },
    async getLabels() {
      const entrepriseStore = useEntrepriseStore()

      const { data } = await http.get<ApiPaginatedResponse<Label>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/tasks/labels/`
      )

      this.labels = data.results
    },
    async updateLabel(data: Label) {
        const entrepriseStore = useEntrepriseStore()
    
        return http.put<ApiResponse<Label>>(
            `/api/entreprise/${entrepriseStore.entreprise?.slug}/tasks/labels/${data.id}/`,
            data
        )
    },
    async deleteLabel(data: Label) {
        const entrepriseStore = useEntrepriseStore()
    
        return http.delete<ApiResponse<Label>>(
            `/api/entreprise/${entrepriseStore.entreprise?.slug}/tasks/labels/${data.id}/`
        )
    },

    /**
     * 
     * Tasks functions
     * 
     */
    async createTask(data: Omit<Task, 'id'>) {
      const entrepriseStore = useEntrepriseStore()

      return http.post<ApiResponse<Task>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/tasks/`,
        data
      )
    },
    async getTasks() {
      const entrepriseStore = useEntrepriseStore()

      const { data } = await http.get<ApiPaginatedResponse<Task>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/tasks/`,
        {
          params: {
            search: this.filters.search,
            completed: this.filters.completed,
            user: this.filters.user
          }
        }
      )

      this.tasks = data.results
    },
    async updateTask(data: Task) {
      const entrepriseStore = useEntrepriseStore()

      return http.put<ApiResponse<Task>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/tasks/${data.id}/`,
        data
      )
    },
    async deleteTask(data: Task) {
      const entrepriseStore = useEntrepriseStore()

      return http.delete<ApiResponse<Task>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/tasks/${data.id}/`
      )
    }
  },

  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useTasksStore, import.meta.hot))
}

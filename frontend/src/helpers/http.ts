import { useUserStore } from '@/stores/apps/User'
import axios, { AxiosError } from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_HOST_API,
  headers: {
    'Content-type': 'application/json'
  }
})

http.interceptors.request.use((config) => {
  const userStore = useUserStore()
  if (config && config.headers && userStore.auth.access) {
    config.headers['Authorization'] = `Bearer ${userStore.auth.access}`
  }

  return config
})

http.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    if (error instanceof AxiosError) {
      const originalRequest = error.config

      if (
        error.response?.status === 401 &&
        // @ts-ignore
        !originalRequest._retry &&
        originalRequest.url !== '/api/user/refresh'
      ) {
        const token = await useUserStore().refreshToken()

        if (token) {
          // @ts-ignore
          originalRequest._retry = true

          return http(originalRequest)
        } else {
          if (document.location.pathname !== '/connexion?disconnected') {
            await useUserStore().logOut()
            document.location.href = '/connexion?disconnected'
          }
        }
        // @ts-ignore
      } else if (originalRequest.url === '/api/user/refresh') {
        if (document.location.pathname !== '/connexion?disconnected') {
          await useUserStore().logOut()
          document.location.href = '/connexion?disconnected'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default http

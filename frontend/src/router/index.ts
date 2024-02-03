import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

import userRoutes from './routes/user'
import legalRoutes from './routes/legals'
import entrepriseRoutes from './routes/entreprise'
import clientsRoutes from './routes/clients'
import constructorRoutes from './routes/constructor'
import documentsRoutes from './routes/documents'
import dashboardRoutes from './routes/dashboard'

import { useUserStore } from '@/stores/apps/User'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/accueil',
      name: 'home',
      component: HomeView,
      meta: {
        title: 'Accueil',
        layout: 'layout-vertical',
        requireAuth: true
      }
    },
    ...legalRoutes,
    ...userRoutes,
    ...entrepriseRoutes,
    ...clientsRoutes,
    ...constructorRoutes,
    ...documentsRoutes,
    ...dashboardRoutes,
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/errors/404.vue'),
      meta: {
        title: 'Page non trouvée',
        layout: 'layout-full'
      }
    }
  ]
})

router.beforeEach((to) => {
  const userStore = useUserStore()
  const entrepriseStore = useEntrepriseStore()

  if (to.meta.requireAuth && !userStore.auth.isLoggedIn) {
    return {
      name: 'login',
      query: { redirect: to.fullPath }
    }
  }

  if (to.meta.permissions) {
    if (Object.keys(to.meta.permissions).length > 0) {
      const permissions = to.meta.permissions

      if (!entrepriseStore.entreprise) {
        return {
          name: 'home'
        }
      }

      if (entrepriseStore.entreprise.user_permissions) {
        let isAllowed = true
        Object.entries(permissions).forEach(
          ([key, value]: [key: string, value: boolean]) => {
            if (
              (entrepriseStore.entreprise?.user_permissions as any)[
                key
              ] !== value
            ) {
              isAllowed = false
            }
          }
        )

        if (!isAllowed) {
          return {
            name: 'home'
          }
        }
      }
    }
  }

  if (typeof to.meta.title === 'string') {
    document.title = to.meta.title + ' - Contana'
  } else document.title = 'Contana - Solution de facturation'
})

export default router

export default [
  {
    path: '/:entrepriseSlug/tableau-de-bord',
    name: 'entreprise-dashboard',
    component: () => import('@/views/apps/dashboard/Dashboard.vue'),
    meta: {
      title: 'Tableau de bord',
      layout: 'layout-vertical',
      requireAuth: true,
      requireStripe: true,
      permissions: {
        access_dashboard: true
      }
    }
  }
]

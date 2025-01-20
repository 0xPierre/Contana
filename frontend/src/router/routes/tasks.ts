export default [
  {
    path: '/:entrepriseSlug/tasks',
    name: 'entreprise-tasks',
    component: () => import('@/views/apps/tasks/Tasks.vue'),
    meta: {
      title: 'Tâches',
      layout: 'layout-vertical',
      requireAuth: true,
      requireStripe: true,
      permissions: {
        access_crm: true
      }
    }
  },
]

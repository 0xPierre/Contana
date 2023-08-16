export default [
  {
    path: '/:entrepriseSlug/constructeur',
    name: 'entreprise-constructor',
    component: () =>
      import('@/views/apps/constructor/ConstructorView.vue'),
    meta: {
      title: 'Constructeur',
      layout: 'layout-vertical',
      requireAuth: true,
      permissions: {
        access_clients: true
      }
    }
  }
]

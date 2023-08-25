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
        access_constructor: true
      }
    }
  },
  {
    path: '/:entrepriseSlug/constructeur/brouillon/:documentId/:documentNumber',
    name: 'entreprise-constructor-draft',
    component: () =>
      import('@/views/apps/constructor/ConstructorView.vue'),
    meta: {
      title: 'Modification du brouillon',
      layout: 'layout-vertical',
      requireAuth: true,
      forceComponentReload: true,
      permissions: {
        access_constructor: true
      }
    }
  }
]

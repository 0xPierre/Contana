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
      requireStripe: true,
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
      requireStripe: true,
      forceComponentReload: true,
      permissions: {
        access_constructor: true
      }
    }
  },
  {
    path: '/:entrepriseSlug/constructeur/avoir/:documentNumber',
    name: 'entreprise-constructor-avoir',
    component: () =>
      import('@/views/apps/constructor/ConstructorView.vue'),
    meta: {
      title: 'Créer un avoir - Constructeur',
      layout: 'layout-vertical',
      requireAuth: true,
      requireStripe: true,
      forceComponentReload: true,
      permissions: {
        access_constructor: true
      }
    }
  }
]

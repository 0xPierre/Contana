export default [
  {
    path: '/:entrepriseSlug/parametres',
    name: 'entreprise-settings',
    component: () =>
      import('@/views/apps/entreprise/settings/EntrepriseSettings.vue'),
    meta: {
      title: 'Paramètres',
      layout: 'layout-vertical',
      requireAuth: true,
      permissions: {
        administrate: true
      }
    }
  },
  {
    path: '/:entrepriseSlug/rejoindre/:invitationToken',
    name: 'entreprise-join',
    component: () =>
      import('@/views/apps/entreprise/join/EntrepriseJoin.vue'),
    meta: {
      title: "Rejoindre l'entreprise",
      layout: 'layout-full',
      requireAuth: true
    }
  }
]

export default [
  {
    path: '/:entrepriseSlug/clients',
    name: 'entreprise-clients',
    component: () => import('@/views/apps/clients/ClientsListing.vue'),
    meta: {
      title: 'Clients',
      layout: 'layout-vertical',
      requireAuth: true,
      permissions: {
        access_clients: true
      }
    }
  },
  {
    path: '/:entrepriseSlug/clients/:clientId/:clientNumber',
    name: 'entreprise-client-view',
    component: () =>
      import('@/views/apps/clients/ClientView/ClientView.vue'),
    meta: {
      title: 'Client',
      layout: 'layout-vertical',
      requireAuth: true,
      permissions: {
        access_clients: true,
        update_clients: true
      }
    }
  }
]

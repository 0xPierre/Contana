export default [
  {
    path: '/:entrepriseSlug/documents',
    name: 'entreprise-documents',
    component: () => import('@/views/apps/documents/DocumentsListing.vue'),
    meta: {
      title: 'Documents',
      layout: 'layout-vertical',
      requireAuth: true,
      permissions: {
        access_documents: true
      }
    }
  }
]

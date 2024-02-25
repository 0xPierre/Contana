export default [
  {
    path: '/:entrepriseSlug/documents',
    name: 'entreprise-documents',
    component: () => import('@/views/apps/documents/DocumentsListing.vue'),
    meta: {
      title: 'Documents',
      layout: 'layout-vertical',
      requireAuth: true,
      requireStripe: true,
      permissions: {
        access_documents: true
      }
    }
  },
  {
    path: '/:entrepriseSlug/documents/:documentId/:documentNumber',
    name: 'entreprise-document-view',
    component: () =>
      import('@/views/apps/documents/DocumentView/DocumentView.vue'),
    meta: {
      title: 'Document',
      layout: 'layout-vertical',
      requireAuth: true,
      requireStripe: true,
      forceComponentReload: true,
      permissions: {
        access_documents: true
      }
    }
  }
]

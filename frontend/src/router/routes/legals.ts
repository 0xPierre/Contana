export default [
  {
    path: '/conditions-generales-utilisation',
    name: 'cgu',
    component: () => import('@/views/apps/legals/TermsAndConditions.vue'),
    meta: {
      title: "Condition générales d'utilisation",
      layout: 'layout-full'
    }
  }
]

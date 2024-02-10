export default [
  {
    path: '/commencer',
    name: 'signup',
    component: () => import('@/views/apps/user/RegisterView.vue'),
    meta: {
      title: 'Créer un compte',
      layout: 'layout-full'
    }
  },
  {
    path: '/',
    name: 'login',
    component: () => import('@/views/apps/user/LoginView.vue'),
    meta: {
      title: 'Connexion',
      layout: 'layout-full'
    }
  },
  {
    path: '/mot-de-passe-oublie',
    name: 'forgot-password',
    component: () =>
      import('@/views/apps/user/ForgotPassword/ForgotPassword.vue'),
    meta: {
      title: 'Mot de passe oublié',
      layout: 'layout-full'
    }
  },
  {
    path: '/reinitialisation-du-mot-de-passe',
    name: 'reset-password',
    component: () =>
      import('@/views/apps/user/ForgotPassword/ResetPassword.vue'),
    meta: {
      title: 'Réinitialiser votre mot de passe',
      layout: 'layout-full'
    }
  },
  {
    path: '/parametres',
    name: 'settings',
    component: () =>
      import('@/views/apps/user/Settings/AccountSettings.vue'),
    meta: {
      title: 'Paramètres',
      layout: 'layout-vertical',
      requireAuth: true
    }
  }
]

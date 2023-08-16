<script setup lang="ts">
// import useJwt from '@/auth/jwt/useJwt'
import { fullNameToText } from '@/helpers/utils'
import { useUserStore } from '@/stores/apps/User'
import { useRouter } from 'vue-router'
import { notify } from '@/helpers/notify'

const userStore = useUserStore()
const router = useRouter()

const logOut = () => {
  userStore.logOut()
  router.push({
    name: 'login'
  })
  notify('Vous êtes déconnecté', 'success')
}
</script>

<template>
  <b-nav-item-dropdown
    right
    toggle-class="d-flex align-items-center dropdown-user-link"
    class="dropdown-user"
  >
    <template #button-content>
      <div class="d-sm-flex d-none user-nav">
        <p class="user-name font-weight-bolder mb-0">
          {{ userStore.data?.full_name }}
        </p>
      </div>
      <b-avatar
        size="40"
        variant="light-primary"
        :src="userStore.data?.avatar"
        :text="fullNameToText(userStore.data?.full_name || '')"
      />
    </template>

    <b-dropdown-item
      link-class="d-flex align-items-center"
      :to="{ name: 'settings' }"
    >
      <vue-feather size="16" type="settings" class="mr-50" />
      <span>Paramètres</span>
    </b-dropdown-item>

    <b-dropdown-divider />

    <b-dropdown-item
      link-class="d-flex align-items-center"
      @click="logOut"
    >
      <vue-feather size="16" type="log-out" class="mr-50" />
      <span>Déconnexion</span>
    </b-dropdown-item>
  </b-nav-item-dropdown>
</template>

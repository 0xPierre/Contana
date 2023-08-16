<script setup lang="ts">
import AccountSettingPassword from './AccountSettingPassword.vue'
import AccountSettingsProfil from './AccountSettingsProfil.vue'
</script>

<template>
  <b-tabs
    content-class="col-12 col-md-9 mt-1 mt-md-0"
    pills
    nav-wrapper-class="col-md-3 col-12"
    nav-class="nav-left"
  >
    <b-tab active>
      <template #title>
        <vue-feather type="user" size="18" class="mr-50" />
        <span class="font-weight-bold">Profil</span>
      </template>

      <AccountSettingsProfil />
    </b-tab>

    <b-tab>
      <template #title>
        <vue-feather type="lock" size="18" class="mr-50" />
        <span class="font-weight-bold">Sécurité</span>
      </template>

      <AccountSettingPassword />
    </b-tab>
  </b-tabs>
</template>

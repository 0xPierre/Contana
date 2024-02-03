<script setup lang="ts">
import NotFound from '@/assets/svg/errors/notfound.svg'
import Logo from '@/assets/images/logo.png'
</script>

<template>
  <div class="auth-wrapper auth-v2">
    <b-link to="/" class="brand-logo">
      <b-img :src="Logo" alt="Contana logo" />

      <h2 class="brand-text text-primary ml-1">Contana</h2>
    </b-link>

    <div class="w-100 text-center mt-5">
      <b-img style="height: 200px" :src="NotFound" />
      <h2 class="mb-1 mt-3">Page non trouvée</h2>
      <p class="mb-2">
        Oups ! La page que vous cherchez n'existe pas ou n'existe plus.
      </p>

      <b-button
        variant="primary"
        class="btn-sm-block"
        :to="{ name: 'home' }"
      >
        Retourner à l'accueil
      </b-button>
    </div>
  </div>
</template>

<style lang="scss">
@import '@/assets/scss/template/vue/pages/page-auth.scss';
</style>

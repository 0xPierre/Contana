<script setup lang="ts">
import NotFound from '@/assets/svg/errors/notfound.svg'
</script>

<template>
  <div class="mt-2">
    <b-link to="/">
      <h2 class="text-primary ml-1">Contana</h2>
    </b-link>

    <div class="w-100 text-center">
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

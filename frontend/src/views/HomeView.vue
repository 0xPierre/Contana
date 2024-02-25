<script setup lang="ts">
import banner from '@/assets/images/banner.png'
import NewEntreprise from '@/components/home/NewEntreprise.vue'
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/apps/User.ts'

onMounted(() => {
  useUserStore().getData()
})
</script>

<template>
  <div>
    <section id="knowledge-base-search">
      <b-card
        no-body
        class="knowledge-base-bg text-center"
        :style="{
          backgroundImage: `url(${banner})`
        }"
      >
        <b-card-body class="card-body">
          <h2 class="text-primary">
            Solution de facturation, comptabilité et pilotage de votre
            entreprise.
          </h2>

          <b-row>
            <b-col md="4" class="offset-md-4">
              <b-button
                v-ripple
                variant="primary"
                block
                :to="{ name: 'entreprise-create' }"
              >
                Créer une entreprise
              </b-button>
            </b-col>
          </b-row>
        </b-card-body>
      </b-card>
    </section>
    <NewEntreprise />
  </div>
</template>

<style lang="scss">
@import '@/assets/scss/template/vue/pages/page-knowledge-base.scss';
</style>

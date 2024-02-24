<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { swalAlert } from '@/helpers/notify.ts'
import { useUserStore } from '@/stores/apps/User.ts'

const route = useRoute()
const userStore = useUserStore()

onMounted(async () => {
  if (route.query.type === 'entreprise-new-success') {
    await swalAlert(
      'Entreprise créée !',
      'success',
      'Vous pouvez dès à présent commencer à utiliser votre entreprise. Si vous ne pouvez pas la voir, veuillez rafraîchir la page.'
    )
    await userStore.getData()
  }
})
</script>

<template></template>

<style scoped lang="scss"></style>

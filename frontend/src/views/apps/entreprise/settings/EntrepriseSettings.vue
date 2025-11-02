<script setup lang="ts">
import { onMounted, ref } from 'vue'
import EntrepriseSettingsInformations from './EntrepriseSettingsInformations.vue'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'
import EntrepriseSettingsUsers from './EntrepriseSettingsUsers.vue'
import EntrepriseSettingsVisualIdentity from './EntrepriseSettingsVisualIdentity.vue'
import EntrepriseSettingsSecurity from './EntrepriseSettingsSecurity.vue'
import EntrepriseSettingsPersonalization from '@/views/apps/entreprise/settings/EntrepriseSettingsPersonalization/EntrepriseSettingsPersonalization.vue'
import EntrepriseSettingsBilling from '@/views/apps/entreprise/settings/EntrepriseSettingsBilling.vue'
import EntrepriseSettingsApiKeys from './EntrepriseSettingsApiKeys.vue'

const isLoading = ref(false)
const entrepriseStore = useEntrepriseStore()

onMounted(async () => {
  isLoading.value = true

  await entrepriseStore.getEntrepriseData()

  isLoading.value = false
})
</script>

<template>
  <b-overlay :show="isLoading">
    <b-tabs
      content-class="col-12 col-md-9 mt-1 mt-md-0"
      pills
      vertical
      nav-wrapper-class="col-md-3 col-12"
      nav-class="nav-left"
    >
      <b-tab active v-if="entrepriseStore.isPaymentStatusOk">
        <template #title>
          <vue-feather type="user" size="18" class="mr-50" />
          <span class="font-weight-bold">Informations</span>
        </template>

        <EntrepriseSettingsInformations />
      </b-tab>

      <b-tab v-if="entrepriseStore.isPaymentStatusOk">
        <template #title>
          <vue-feather type="layout" size="18" class="mr-50" />
          <span class="font-weight-bold">Personnalisation</span>
        </template>

        <EntrepriseSettingsPersonalization />
      </b-tab>

      <b-tab v-if="entrepriseStore.isPaymentStatusOk">
        <template #title>
          <vue-feather type="lock" size="18" class="mr-50" />
          <span class="font-weight-bold">Utilisateurs</span>
        </template>

        <EntrepriseSettingsUsers />
      </b-tab>

      <b-tab v-if="entrepriseStore.isPaymentStatusOk">
        <template #title>
          <vue-feather type="eye" size="18" class="mr-50" />
          <span class="font-weight-bold">Identité visuelle</span>
        </template>

        <EntrepriseSettingsVisualIdentity />
      </b-tab>

      <!-- <b-tab v-if="entrepriseStore.isPaymentStatusOk">
        <template #title>
          <vue-feather type="check-square" size="18" class="mr-50" />
          <span class="font-weight-bold">CRM</span>
        </template>

        <EntrepriseSettingsCRM />
      </b-tab> -->

      <b-tab>
        <template #title>
          <vue-feather type="dollar-sign" size="18" class="mr-50" />
          <span class="font-weight-bold">Facturation</span>
        </template>

        <EntrepriseSettingsBilling />
      </b-tab>

      <b-tab v-if="entrepriseStore.entreprise?.is_owner">
        <template #title>
          <vue-feather type="lock" size="18" class="mr-50" />
          <span class="font-weight-bold">Sécurité</span>
        </template>

        <EntrepriseSettingsSecurity />
      </b-tab>

      <b-tab v-if="entrepriseStore.entreprise?.is_owner || entrepriseStore.entreprise?.user_permissions?.administrate">
        <template #title>
          <vue-feather type="key" size="18" class="mr-50" />
          <span class="font-weight-bold">Clé API</span>
        </template>

        <EntrepriseSettingsApiKeys />
      </b-tab>
    </b-tabs>
  </b-overlay>
</template>

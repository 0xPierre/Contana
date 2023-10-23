<script setup lang="ts">
import PersonalizationDocuments from '@/views/apps/entreprise/settings/EntrepriseSettingsPersonalization/PersonalizationDocuments.vue'
</script>

<template>
  <b-tabs pills>
    <b-tab active>
      <template #title>
        <vue-feather type="file-text" size="18" class="mr-50" />
        <span class="font-weight-bold">Documents</span>
      </template>
      <PersonalizationDocuments />
    </b-tab>
  </b-tabs>
</template>

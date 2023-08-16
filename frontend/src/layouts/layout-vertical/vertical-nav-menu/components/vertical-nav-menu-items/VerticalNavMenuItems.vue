<script lang="ts" setup>
import VerticalNavMenuHeader from './vertical-nav-menu-header/VerticalNavMenuHeader.vue'
import VerticalNavMenuLink from './vertical-nav-menu-link/VerticalNavMenuLink.vue'
import VerticalNavMenuGroup from './vertical-nav-menu-group/VerticalNavMenuGroup.vue'
import { useEntrepriseStore } from '@/stores/apps/Entreprise'

import { can } from '@/helpers/permissions'

const entrepriseStore = useEntrepriseStore()
</script>

<template>
  <ul>
    <VerticalNavMenuLink
      :item="{ title: 'Accueil', route: { name: 'home' }, icon: 'home' }"
    />
    <template v-if="entrepriseStore.entreprise">
      <VerticalNavMenuHeader :item="{ header: 'Entreprise' }" />
      <VerticalNavMenuLink
        v-if="can('access_constructor')"
        :item="{
          title: 'Constructeur',
          route: {
            name: 'entreprise-constructor',
            params: { entrepriseSlug: entrepriseStore.entreprise?.slug }
          },
          icon: 'package'
        }"
      />
      <VerticalNavMenuLink
        v-if="can('access_documents')"
        :item="{
          title: 'Documents',
          route: { name: 'home' },
          icon: 'file-text'
        }"
      />
      <VerticalNavMenuLink
        v-if="can('access_clients')"
        :item="{
          title: 'Clients',
          route: {
            name: 'entreprise-clients',
            params: { entrepriseSlug: entrepriseStore.entreprise?.slug }
          },
          icon: 'users'
        }"
      />
      <VerticalNavMenuLink
        v-if="can('administrate')"
        :item="{
          title: 'Paramètres',
          route: {
            name: 'entreprise-settings',
            params: { entrepriseSlug: entrepriseStore.entreprise?.slug }
          },
          icon: 'settings'
        }"
      />
    </template>
    <!-- <VerticalNavMenuGroup
      :item="{
        title: 'Grouped',
        icon: 'activity',
        children: [
          {
            title: '1',
            route: {
              name: 'home'
            },
            icon: 'home'
          },
          {
            title: '2',
            route: {
              name: 'about'
            },
            icon: 'users'
          }
        ]
      }"
    />
    <VerticalNavMenuLink
      :item="{
        title: 'Second page',
        route: { name: 'about' },
        icon: 'users'
      }"
    /> -->
  </ul>
</template>

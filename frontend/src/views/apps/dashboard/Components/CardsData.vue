<script setup lang="ts">
import { ref, watch } from 'vue'
import { useDashboardStore } from '@/stores/apps/Dashboard.ts'
import { euro } from '@/helpers/utils.ts'

const dashboardStore = useDashboardStore()
</script>

<template>
  <b-overlay :show="dashboardStore.cardsData.isLoading">
    <b-card no-body class="mb-1">
      <div class="d-flex p-1 align-items-center">
        <b-avatar variant="light-info" size="lg">
          <vue-feather type="check-circle" size="21" />
        </b-avatar>
        <div class="ml-1">
          <div>Chiffre d'affaires</div>
          <div class="font-weight-bolder font-medium-3">
            {{ euro(dashboardStore.cardsData.data.turnover).format() }} €
          </div>
        </div>
      </div>
    </b-card>

    <b-card no-body class="mb-1">
      <div class="d-flex p-1 align-items-center">
        <b-avatar variant="light-success" size="lg">
          <vue-feather type="dollar-sign" size="21" />
        </b-avatar>
        <div class="ml-1">
          <div>Encaissements</div>
          <div class="font-weight-bolder font-medium-3">
            {{
              euro(dashboardStore.cardsData.data.cash_collection).format()
            }}
            €
          </div>
        </div>
      </div>
    </b-card>

    <b-card no-body class="mb-1">
      <div class="d-flex p-1 align-items-center">
        <b-avatar variant="light-danger" size="lg">
          <vue-feather type="file-text" size="21" />
        </b-avatar>
        <div class="ml-1">
          <div>Devis en attente</div>
          <div class="font-weight-bolder font-medium-3">
            {{
              euro(
                dashboardStore.cardsData.data.outstanding_quotations
              ).format()
            }}
            €
          </div>
        </div>
      </div>
    </b-card>

    <b-card no-body class="mb-1">
      <div class="d-flex p-1 align-items-center">
        <b-avatar variant="light-warning" size="lg">
          <vue-feather type="users" size="21" />
        </b-avatar>
        <div class="ml-1">
          <div>Encours clients</div>
          <div class="font-weight-bolder font-medium-3">
            {{
              euro(
                dashboardStore.cardsData.data.outstanding_client_amount
              ).format()
            }}
            €
          </div>
        </div>
      </div>
    </b-card>
  </b-overlay>
</template>

<style scoped lang="scss"></style>

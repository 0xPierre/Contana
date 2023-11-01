<script setup lang="ts">
import { computed, ref } from 'vue'
import { useDashboardStore } from '@/stores/apps/Dashboard.ts'

const dashboardStore = useDashboardStore()

const chartOptions = computed(() => ({
  chart: {
    toolbar: {
      show: false,
      fontFamily: 'Montserrat, Helvetica, Arial, serif'
    }
  },
  labels: dashboardStore.bestClientsChart.data.labels,
  dataLabels: {
    enabled: true,
    style: {
      fontFamily: 'Montserrat, Helvetica, Arial, serif'
    }
  },
  legend: { show: false },
  comparedResult: [2, -3, 8],
  stroke: { width: 0 },
  tooltip: {
    y: {
      formatter(val) {
        return `${new Intl.NumberFormat('fr-FR').format(val)} €`
      },
      style: {
        fontFamily: 'Montserrat, Helvetica, Arial, serif'
      }
    },
    x: {
      style: {
        fontFamily: 'Montserrat, Helvetica, Arial, serif'
      }
    }
  }
}))
</script>

<template>
  <b-overlay :show="dashboardStore.bestClientsChart.isLoading">
    <b-card no-body>
      <b-card-header>
        <b-card-title>10 Meilleurs clients</b-card-title>
      </b-card-header>

      <b-card-body class="pb-0">
        <apexchart
          v-show="dashboardStore.bestClientsChart.data.serie.length > 0"
          ref="chart"
          type="pie"
          height="350"
          :options="chartOptions"
          :series="dashboardStore.bestClientsChart.data.serie"
        />
        <div
          v-show="dashboardStore.bestClientsChart.data.serie.length === 0"
          class="text-center"
          style="height: 330px"
        >
          Aucune donnée disponible
        </div>
      </b-card-body>
    </b-card>
  </b-overlay>
</template>

<style scoped lang="scss"></style>

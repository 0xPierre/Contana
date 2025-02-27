<script setup lang="ts">
import { computed } from 'vue'
import { useDashboardStore } from '@/stores/apps/Dashboard.ts'

interface Props {
  title: string
  labels: string[]
  series: number[][] | number[]
  isLoading: boolean
}
const props = withDefaults(defineProps<Props>(), {
  isLoading: false
})

const dashboardStore = useDashboardStore()

const chartOptions = computed(() => ({
  chart: {
    toolbar: {
      show: false,
      fontFamily: 'Montserrat, Helvetica, Arial, serif'
    }
  },
  labels: props.labels,
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
  <b-overlay :show="isLoading">
    <b-card no-body>
      <b-card-header>
        <b-card-title>{{ title }}</b-card-title>
      </b-card-header>

      <b-card-body class="pb-0">
        <apexchart
          v-show="series.length > 0"
          ref="chart"
          type="pie"
          height="280"
          :options="chartOptions"
          :series="series"
        />
        <div
          v-show="series.length === 0"
          class="text-center"
          style="height: 265px"
        >
          Aucune donnée disponible
        </div>
      </b-card-body>
    </b-card>
  </b-overlay>
</template>

<style scoped lang="scss"></style>

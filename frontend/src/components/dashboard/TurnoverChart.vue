<script setup lang="ts">
import { computed, ref } from 'vue'
import { useDashboardStore } from '@/stores/apps/Dashboard.ts'

const dashboardStore = useDashboardStore()

const chartOptions = computed(() => ({
  labels: dashboardStore.turnoverChart.data.labels,
  chart: {
    toolbar: { show: false },
    zoom: { enabled: false },
    type: 'area',
    offsetX: -10
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth',
    dashArray: [0, 12],
    width: [4, 3]
  },
  legend: {
    show: false
  },
  colors: ['#3c68ca', '#28c76f'],
  markers: {
    size: 0,
    hover: {
      size: 5
    }
  },
  xaxis: {
    labels: {
      style: {
        colors: '#b9b9c3',
        fontSize: '1rem',
        fontFamily: 'Montserrat, Helvetica, Arial, serif'
      }
    },
    axisTicks: {
      show: false
    },
    categories: [],
    axisBorder: {
      show: false
    },
    tickPlacement: 'on'
  },
  yaxis: {
    tickAmount: 5,
    labels: {
      style: {
        colors: '#b9b9c3',
        fontSize: '1rem',
        fontFamily: 'Montserrat, Helvetica, Arial, serif'
      },
      formatter(val) {
        return `${new Intl.NumberFormat('fr-FR').format(val)} €`
      }
    }
  },
  grid: {
    borderColor: '#e7eef7',
    padding: {
      top: -20,
      bottom: -10,
      left: 20
    }
  },
  tooltip: {
    x: { show: false }
  }
}))

// const series = {
//   series: [
//     {
//       name: "Chiffre d'affaires",
//       data: [
//         0, 1, 2, 4, 5, 7, 10, 15, 14, 12, 12, 12, 13, 9, 8, 5, 3, 3, 3, 1,
//         0, 0, 0, 0, 0, 0, 0, 0, 0, 0
//       ]
//     }
//     // {
//     //   name: 'Bénéfices',
//     //   data: [
//     //     0, 0, 1, 3, 4, 5, 8, 13, 15, 16, 14, 10, 11, 7, 6, 3, 1, 1, 1, 0,
//     //     0, 0, 0, 0, 0, 0, 0, 0, 0, 0
//     //   ]
//     // }
//   ]
// }
const series = {
  series: [{ name: "Chiffre d'affaires", data: [0, 0, 5, 0, 0, 0, 0] }]
}
</script>

<template>
  <b-overlay :show="dashboardStore.turnoverChart.isLoading">
    <b-card no-body class="mb-1">
      <b-card-header>
        <b-card-title>Chiffre d'affaires</b-card-title>
      </b-card-header>

      <b-card-body class="pb-0">
        <apexchart
          ref="chart"
          type="area"
          height="350"
          :options="chartOptions"
          :series="dashboardStore.turnoverChart.data.series"
        />
      </b-card-body>
    </b-card>
  </b-overlay>
</template>

<style scoped lang="scss"></style>

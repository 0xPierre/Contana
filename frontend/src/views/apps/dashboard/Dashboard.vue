<script setup lang="ts">
import { onBeforeMount, onMounted, ref, watch } from 'vue'
import CardsData from '@/views/apps/dashboard/Components/CardsData.vue'
import TurnoverChart from '@/views/apps/dashboard/Components/TurnoverChart.vue'
import BestClients from '@/views/apps/dashboard/Components/BestClients.vue'
import BestArticles from '@/views/apps/dashboard/Components/BestArticles.vue'
import { useDashboardStore } from '@/stores/apps/Dashboard.ts'
import strftime from 'strftime'

const dashboardStore = useDashboardStore()

const fetchDatas = async () => {
  dashboardStore.getCardsData()
  dashboardStore.getTurnover()
  dashboardStore.getBestArticles()
  dashboardStore.getBestClients()
}

onMounted(() => {
  dashboardStore.period = 'week'
  dashboardStore.startDate = ''
  dashboardStore.endDate = ''
  fetchDatas()
})

watch(
  [
    () => dashboardStore.period,
    () => dashboardStore.startDate,
    () => dashboardStore.endDate
  ],
  async () => {
    if (
      dashboardStore.period === 'custom' &&
      (!dashboardStore.startDate || !dashboardStore.endDate)
    )
      return
    fetchDatas()
  }
)
</script>

<template>
  <div>
    <b-row>
      <b-col md="9">
        <vue-perfect-scrollbar
          tagname="div"
          style="max-height: calc(100vh - 102px - 1rem)"
          :settings="{ suppressScrollX: true }"
        >
          <TurnoverChart />

          <b-row>
            <b-col md="6">
              <BestClients />
            </b-col>
            <b-col md="6">
              <BestArticles />
            </b-col>
          </b-row>
        </vue-perfect-scrollbar>
      </b-col>
      <b-col md="3">
        <b-card class="mb-1">
          <v-select
            :options="[
              {
                label: 'Cette semaine',
                value: 'week'
              },
              {
                label: 'La semaine dernière',
                value: 'last_week'
              },
              {
                label: 'Ce mois',
                value: 'month'
              },
              {
                label: 'Le mois dernier',
                value: 'last_month'
              },
              {
                label: 'Cette année',
                value: 'year'
              },
              {
                label: 'L\'année dernière',
                value: 'last_year'
              },
              {
                label: 'Personnalisé',
                value: 'custom'
              },
              {
                label: 'Tout',
                value: 'all'
              }
            ]"
            :reduce="(o) => o.value"
            label="label"
            :clearable="false"
            v-model="dashboardStore.period"
          />
          <div v-if="dashboardStore.period === 'custom'">
            <b-form-group class="mt-1">
              <flat-pickr
                :config="{
                  mode: 'range',
                  locale: 'fr',
                  dateFormat: 'd/m/Y',
                  altInput: true,
                  altFormat: 'd/m/Y',
                  allowInput: true,
                  onChange: function (selectedDates) {
                    if (selectedDates[0]) {
                      dashboardStore.startDate = strftime(
                        '%d/%m/%Y',
                        selectedDates[0]
                      )
                    } else {
                      dashboardStore.startDate = ''
                    }

                    if (selectedDates[1]) {
                      dashboardStore.endDate = strftime(
                        '%d/%m/%Y',
                        selectedDates[1]
                      )
                    } else {
                      dashboardStore.endDate = ''
                    }
                  }
                }"
                placeholder="Sélectionner une plage de dates"
              />
            </b-form-group>
          </div>
        </b-card>

        <CardsData />
      </b-col>
    </b-row>
  </div>
</template>

<style scoped lang="scss"></style>

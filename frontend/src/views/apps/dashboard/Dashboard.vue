<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useDashboardStore } from '@/stores/apps/Dashboard.ts'
import strftime from 'strftime'
import PieChart from '@/components/dashboard/PieChart.vue'
import CardData from '@/components/dashboard/CardData.vue'
import TurnoverChart from '@/components/dashboard/TurnoverChart.vue'
import { euro } from '@/helpers/utils.ts'

const dashboardStore = useDashboardStore()

const fetchDatas = async (watched: boolean = false) => {
  dashboardStore.getCardsData()
  dashboardStore.getTurnover()
  dashboardStore.getBestClientsBySignedQuote()
  dashboardStore.getBestUserBySignedQuotes()

  if (!watched) {
    dashboardStore.getOutstandingQuoteByCommercial()
  }
}

onMounted(() => {
  dashboardStore.period = 'month'
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
    fetchDatas(true)
  }
)
</script>

<template>
  <div>
    <b-row>
      <b-col lg="9">
        <TurnoverChart />
      </b-col>
      <b-col lg="3">
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
            :reduce="(o: any) => o.value"
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
                  onChange: function (selectedDates: Date[]) {
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

        <b-overlay :show="dashboardStore.cardsData.isLoading">
          <b-row>
            <b-col lg="12" md="6" sm="12">
              <CardData
                title="Volume d'affaires"
                icon="file-text"
                variant="light-danger"
                :value="`${euro(
                  dashboardStore.cardsData.data.signed_quotes
                ).format()} €`"
              />
            </b-col>
            <b-col lg="12" md="6" sm="12">
              <CardData
                title="Chiffre d'affaires"
                icon="check-circle"
                variant="light-info"
                :value="`${euro(
                  dashboardStore.cardsData.data.turnover
                ).format()} €`"
              />
            </b-col>
            <b-col lg="12" md="6" sm="12">
              <CardData
                title="Encaissements"
                icon="dollar-sign"
                variant="light-success"
                :value="`${euro(
                  dashboardStore.cardsData.data.turnover
                ).format()} €`"
              />
            </b-col>
            <b-col lg="12" md="6" sm="12">
              <CardData
                title="Encours clients"
                icon="users"
                variant="light-warning"
                :value="`${euro(
                  dashboardStore.cardsData.data.outstanding_client_amount
                ).format()} €`"
              />
            </b-col>
          </b-row>
        </b-overlay>
      </b-col>
    </b-row>
    <b-row>
      <b-col xl="4" lg="6">
        <PieChart
          title="10 meilleurs clients par devis signé"
          :labels="dashboardStore.bestClientsByQuote.data.labels"
          :series="dashboardStore.bestClientsByQuote.data.serie"
          :is-loading="dashboardStore.bestClientsByQuote.isLoading"
        />
      </b-col>
      <b-col xl="4" lg="6">
        <PieChart
          title="Classements commerciaux par devis signé"
          :labels="dashboardStore.bestUsersByQuote.data.labels"
          :series="dashboardStore.bestUsersByQuote.data.serie"
          :is-loading="dashboardStore.bestUsersByQuote.isLoading"
        />
      </b-col>
      <b-col xl="4" lg="6">
        <PieChart
          title="Total devis en attente par commercial"
          :labels="dashboardStore.outstandingQuoteByCommercial.data.labels"
          :series="dashboardStore.outstandingQuoteByCommercial.data.serie"
          :is-loading="
            dashboardStore.outstandingQuoteByCommercial.isLoading
          "
        />
      </b-col>
    </b-row>
    <b-row>
      <b-col xl="2" lg="4" md="6">
        <CardData
          title="Premier appel"
          icon="users"
          variant="light-warning"
          :value="`${dashboardStore.cardsData.data.discovery_calls}`"
        />
      </b-col>
      <b-col xl="2" lg="4" md="6">
        <CardData
          title="Appels relance"
          icon="users"
          variant="light-warning"
          :value="`${dashboardStore.cardsData.data.follow_up_calls}`"
        />
      </b-col>
      <b-col xl="2" lg="4" md="6">
        <CardData
          title="Nouv clients Pro"
          icon="users"
          variant="light-warning"
          :value="`${dashboardStore.cardsData.data.new_professional_clients}`"
        />
      </b-col>
      <b-col xl="2" lg="4" md="6">
        <CardData
          title="Nouv clients Part"
          icon="users"
          variant="light-warning"
          :value="`${dashboardStore.cardsData.data.new_private_customers}`"
        />
      </b-col>
      <b-col xl="2" lg="4" md="6">
        <CardData
          title="Clients à relancer"
          icon="users"
          variant="light-warning"
          :value="`${dashboardStore.cardsData.data.clients_to_follow_up}`"
        />
      </b-col>
      <b-col xl="2" lg="4" md="6">
        <CardData
          title="Total devis att"
          icon="users"
          variant="light-warning"
          :value="`${euro(
            dashboardStore.cardsData.data.total_outstanding_quotations
          ).format()} €`"
        />
      </b-col>
    </b-row>
  </div>
</template>

<style scoped lang="scss"></style>

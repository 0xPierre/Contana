<script lang="ts" setup>
import { DocumentsState } from '@/types/documents.types.ts'
import { computed } from 'vue'
import strftime from 'strftime'
import { DocumentTypeText } from '@/helpers/documents.ts'
import { euro } from '@/helpers/utils.ts'
import type { ClientModel } from '@/types/clients.types.ts'
import AppTimelineItem from '@/components/timeline/AppTimelineItem.vue'
import AppTimeline from '@/components/timeline/AppTimeline.vue'
import { DocumentsType } from '@/types/core.types.ts'

interface Props {
  client: ClientModel
}
const props = defineProps<Props>()

const timelineDocumentColor = {
  [DocumentsState.Draft]: 'secondary',
  [DocumentsState.Produced]: 'primary',
  [DocumentsState.DevisAccepted]: 'success',
  [DocumentsState.DevisRefused]: 'danger',
  [DocumentsState.DevisExpired]: 'warning',
  [DocumentsState.DevisInvoiced]: 'info',
  [DocumentsState.Paid]: 'light-dark'
}

const timeline = computed(() => {
  const t: {
    title: string
    subtitle: string
    time: string
    variant: string
    icon: string
    to: null | object
  }[] = [
    {
      title: 'Création du client',
      subtitle: `${strftime(
        '%d/%m/%Y',
        new Date(props.client.created_at)
      )}`,
      time: `${strftime(
        '%d/%m/%Y %H:%M',
        new Date(props.client.created_at)
      )}`,
      variant: 'primary',
      icon: 'user',
      to: null
    }
  ]

  props.client.documents.forEach((document) => {
    t.push({
      title: `${DocumentTypeText[document.forme]} ${
        document.document_number
      }`,
      subtitle: `${euro(document.total_ht).format()} €`,
      time: `${strftime('%d/%m/%Y %H:%M', new Date(document.created_at))}`,
      variant: timelineDocumentColor[document.state],
      icon: 'file-text',
      to:
        document.state === DocumentsState.Draft
          ? {
              name: 'entreprise-constructor-draft',
              params: {
                documentId: document.id,
                documentNumber: document.document_number
              }
            }
          : {
              name: 'entreprise-document-view',
              params: {
                documentId: document.id,
                documentNumber: document.document_number
              }
            }
    })
  })

  return t.reverse()
})

const totalHT = computed(() => {
  return props.client.documents.reduce((acc, doc) => {
    if (doc.state === DocumentsState.Draft) return acc
    if (doc.forme === DocumentsType.Avoir) {
      // Already negative
      return acc + doc.total_ht
    }
    if (
      doc.forme === DocumentsType.Acompte ||
      doc.forme === DocumentsType.Facture
    )
      return acc + doc.total_ht

    return acc
  }, 0)
})
</script>

<template>
  <b-card>
    <div class="d-flex justify-content-between">
      <div class="d-flex">
        <vue-feather type="file" size="22" class="mr-1" />
        <h3 class="mb-50">Suivis client</h3>
      </div>
      <div>
        <b-badge variant="light-success">
          Total HT : {{ euro(totalHT).format() }} €
        </b-badge>
      </div>
    </div>

    <AppTimeline class="mt-2">
      <AppTimelineItem
        v-for="item in timeline"
        :key="item.title"
        :title="item.title"
        :time="item.time"
        :subtitle="item.subtitle"
        :icon="item.icon"
        :variant="item.variant"
        :to="item.to"
      >
      </AppTimelineItem>
    </AppTimeline>
  </b-card>
</template>

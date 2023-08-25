import { defineStore, acceptHMRUpdate } from 'pinia'
// import http from '@/helpers/http'
import { DocumentsType, PaymentsMethod } from '@/types/core.types'
import { Section, SectionsType } from '@/types/constructor.types.ts'
import { v4 as uuidv4 } from 'uuid'
import { euro } from '@/helpers/utils.ts'
import http from '@/helpers/http.ts'
import { ApiResponse } from '@/types/api.types.ts'
import { useEntrepriseStore } from '@/stores/apps/Entreprise.ts'
import { ClientConstructor } from '@/types/clients.types.ts'
import strftime from 'strftime'
import SectionArticle from '@/components/constructor/sections/SectionArticle.vue'
import SectionTitle from '@/components/constructor/sections/SectionTitle.vue'
import SectionSubtotal from '@/components/constructor/sections/SectionSubtotal.vue'

interface State {
  documentNumber: string
  client: ClientConstructor | null
  subject: string
  forme: DocumentsType
  paymentMethod: PaymentsMethod
  validityDate: string
  paymentMention: string
  notes: string
  vatPayer: boolean
  otherMention: string
  sections: Section<
    SectionsType.Article | SectionsType.Title | SectionsType.Subtotal
  >[]
  isDraft: boolean
}

export const useConstructorStore = defineStore('constructeur', {
  state: (): State => {
    return {
      documentNumber: '',
      client: null,
      subject: '',
      forme: DocumentsType.Facture,
      paymentMethod: PaymentsMethod.BankTransfer,
      validityDate: strftime(
        '%d/%m/%Y',
        new Date(new Date().setDate(new Date().getDate() + 90))
      ),
      paymentMention: 'À réception de la facture',
      notes: '',
      vatPayer: false,
      otherMention: '',
      sections: [],
      isDraft: false
    }
  },

  getters: {
    formeSentence: (state) => {
      return {
        first:
          state.forme === DocumentsType.Facture
            ? 'la facture'
            : state.forme === DocumentsType.Devis
            ? 'le devis'
            : "l'avoir",
        second:
          state.forme === DocumentsType.Facture
            ? 'de la facture'
            : state.forme === DocumentsType.Devis
            ? 'du devis'
            : "de l'avoir"
      }
    },

    /**
     * Calculate every subtotal and return them all
     */
    subtotals(state) {
      let subtotal = euro(0)

      let subtotals: {
        [key: string]: ReturnType<typeof euro>
      } = {}

      state.sections.forEach((section) => {
        if (section.type === SectionsType.Subtotal) {
          subtotals[section.id] = subtotal
          subtotal = euro(0)
        }

        if (section.type === SectionsType.Article) {
          subtotal = subtotal.add(
            // @ts-ignore
            this.getArticleTotalHT(
              section as Section<SectionsType.Article>
            )
          )
        }
      })
      return subtotals
    },

    getArticleTotalHT: () => {
      return (article: Section<SectionsType.Article>) => {
        const { unitPriceHT, quantity, discountType, discount } =
          article.values

        let price = euro(unitPriceHT).multiply(quantity)

        if (discountType === 'percentage') {
          price = price.multiply(1 - discount / 100)
        } else if (discountType === 'amount') {
          price = price.subtract(discount)
        }

        return price
      }
    },

    totalHT(state) {
      let total = euro(0)
      state.sections.forEach((section) => {
        if (section.type === SectionsType.Article) {
          total = total.add(
            // @ts-ignore
            this.getArticleTotalHT(
              section as Section<SectionsType.Article>
            )
          )
        }
      })

      return total
    },

    totalTVA(state) {
      let total = euro(0)

      state.sections.forEach((section) => {
        if (section.type === SectionsType.Article) {
          // @ts-ignore
          const totalArticle = this.getArticleTotalHT(
            section as Section<SectionsType.Article>
          )
          const { vatRate } = (section as Section<SectionsType.Article>)
            .values

          total = total.add(totalArticle.multiply(vatRate / 100))
        }
      })

      return total
    },

    totalTTC() {
      // @ts-ignore
      return this.totalHT.add(this.totalTVA)
    }
  },

  actions: {
    removeSection(id: string) {
      this.sections = this.sections.filter((section) => section.id !== id)
    },

    /**
     * Duplicate the section just below the one with the given id
     */
    duplicateSection(id: string) {
      const index = this.sections.findIndex((section) => section.id === id)
      const section = this.sections[index]
      const newSection = {
        id: uuidv4(),
        type: section.type,
        values: { ...section.values },
        component: section.component
      }
      this.sections.splice(index + 1, 0, newSection)
    },

    async saveDraft() {
      const entrepriseStore = useEntrepriseStore()

      return http.post<ApiResponse<void>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/constructor/draft/`,
        {
          document_number: this.documentNumber,
          client: this.client,
          subject: this.subject,
          forme: this.forme,
          payment_method: this.paymentMethod,
          validity_date: this.validityDate,
          payment_mention: this.paymentMention,
          notes: this.notes,
          vat_payer: this.vatPayer,
          other_mention: this.otherMention,
          sections: this.sections,
          total_ht: this.totalHT,
          total_tva: this.totalTVA,
          total_ttc: this.totalTTC
        }
      )
    },

    async produceDocument() {
      const entrepriseStore = useEntrepriseStore()

      return http.post<ApiResponse<void>>(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/constructor/produce/`,
        {
          client: this.client,
          subject: this.subject,
          forme: this.forme,
          payment_method: this.paymentMethod,
          validity_date: this.validityDate,
          payment_mention: this.paymentMention,
          notes: this.notes,
          vat_payer: this.vatPayer,
          other_mention: this.otherMention,
          sections: this.sections,
          total_ht: this.totalHT,
          total_tva: this.totalTVA,
          total_ttc: this.totalTTC,
          is_draft: this.isDraft,
          draft_document_number: this.documentNumber
        }
      )
    },

    async getDraft(documentNumber: string) {
      const entrepriseStore = useEntrepriseStore()

      const {
        data: { data }
      } = await http.get<
        ApiResponse<{
          document_number: string
          client: ClientConstructor
          subject: string
          forme: DocumentsType
          payment_method: PaymentsMethod
          validity_date: string
          payment_mention: string
          notes: string
          vat_payer: boolean
          other_mention: string
          sections: Omit<
            Section<
              | SectionsType.Article
              | SectionsType.Title
              | SectionsType.Subtotal
            >,
            'component'
          >[]
        }>
      >(
        `/api/entreprise/${entrepriseStore.entreprise?.slug}/constructor/draft/${documentNumber}/`
      )

      this.documentNumber = data.document_number
      this.client = data.client
      this.subject = data.subject
      this.forme = data.forme
      this.paymentMethod = data.payment_method
      this.validityDate = strftime(
        '%d/%m/%Y',
        new Date(data.validity_date)
      )
      this.paymentMention = data.payment_mention
      this.notes = data.notes
      this.vatPayer = data.vat_payer
      this.otherMention = data.other_mention
      this.isDraft = true

      const SectionComponent = {
        [SectionsType.Article]: SectionArticle,
        [SectionsType.Title]: SectionTitle,
        [SectionsType.Subtotal]: SectionSubtotal
      }

      data.sections.forEach((section) => {
        this.sections.push({
          ...section,
          id: uuidv4(),
          component: SectionComponent[section.type]
        })
      })
    }
  },

  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useConstructorStore, import.meta.hot)
  )
}

import { defineStore, acceptHMRUpdate } from 'pinia'
// import http from '@/helpers/http'
import type { ClientModel } from '@/types/clients.types'
import { DocumentsType, PaymentsMethod } from '@/types/core.types'
import { Section, SectionsType } from '@/types/constructor.types.ts'
import { v4 as uuidv4 } from 'uuid'
import { euro } from '@/helpers/utils.ts'

interface State {
  client: ClientModel | null
  subject: string
  forme: DocumentsType
  paymentMethod: PaymentsMethod
  validityDate: Date
  paymentMention: string
  notes: string
  vatPayer: boolean
  otherMention: string
  sections: Section<
    SectionsType.Article | SectionsType.Title | SectionsType.Subtotal
  >[]
}

export const useConstructorStore = defineStore('constructeur', {
  state: (): State => {
    return {
      client: null,
      subject: '',
      forme: DocumentsType.Facture,
      paymentMethod: PaymentsMethod.BankTransfer,
      validityDate: new Date(
        new Date().setDate(new Date().getDate() + 90)
      ),
      paymentMention: 'À réception de la facture',
      notes: '',
      vatPayer: false,
      otherMention: '',
      sections: []
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
    }
  },

  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useConstructorStore, import.meta.hot)
  )
}

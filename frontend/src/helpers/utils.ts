import currency from 'currency.js'
import strftime from 'strftime'
import { Section, SectionsType } from '@/types/constructor.types.ts'
import { useConstructorStore } from '@/stores/apps/Constructor.ts'

export const fullNameToText = (fullName: string) => {
  const [firstName, lastName] = fullName.split(' ')
  return `${firstName[0]}${lastName[0]}`
}

export const euro = (value: string | number): currency =>
  currency(value, {
    symbol: '',
    decimal: ',',
    separator: ' ',
    precision: 2
  })

// @ts-ignore
export const strftimeFR = strftime.localizeByIdentifier('fr_FR')

/**
 * Get the total HT of a section
 * We can choose to include or not the discount
 * @param section
 * @param withDiscount
 */
export const getSectionArticleTotalHT = (
  section: Section<SectionsType.Article>,
  withDiscount = true
): currency => {
  const { unitPriceHT, quantity, discountType, discount } = section.values

  let price = euro(unitPriceHT).multiply(quantity)

  if (withDiscount) {
    if (discountType === 'percentage') {
      price = price.multiply(1 - discount / 100)
    } else if (discountType === 'amount') {
      price = price.subtract(discount)
    }
  }

  return price
}

export const getSectionsForDocumentProducing = (
  sections: Section<SectionsType>[]
) => {
  const constructorStore = useConstructorStore()
  return sections.map((section) => {
    const newSection = {
      type: section.type,
      values: section.values
    }
    if (newSection.type === 'section-subtotal') {
      newSection.values = {
        ...section.values,
        subtotal: constructorStore.subtotals[section.id].value
      }
    } else if (newSection.type === 'section-article') {
      newSection.values = {
        ...section.values,
        totalHTWithoutDiscount: getSectionArticleTotalHT(
          section as Section<SectionsType.Article>,
          false
        ).value,
        totalHT: getSectionArticleTotalHT(
          section as Section<SectionsType.Article>
        ).value
      }
    }
    return newSection
  })
}

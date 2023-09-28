import SectionSubtotal from '@/components/constructor/sections/SectionSubtotal.vue'
import SectionArticle from '@/components/constructor/sections/SectionArticle.vue'

export enum SectionsType {
  Title = 'section-title',
  Article = 'section-article',
  Subtotal = 'section-subtotal'
}

export type Section<T> = {
  id: string
  type: SectionsType
  values: T extends 'section-title'
    ? {
        title: string
      }
    : T extends 'section-article'
    ? {
        title: string
        description: string

        unitPriceHT: number
        vatRate: 20 | 10 | 5.5 | 2.1 | 0
        quantity: number

        articleType: 'service' | 'product'

        discount: number
        discountType: null | 'percentage' | 'amount'
        discountDescription: string

        unit:
          | ''
          | 'mm'
          | 'cm'
          | 'm'
          | 'km'
          | 'm²'
          | 'm³'
          | 'kg'
          | 'hour'
          | 'day'
          | 'month'
          | 'year'
          | 'ml'
          | 'l'

        displayPriceInfos: boolean
      }
    : T extends 'section-subtotal'
    ? {
        title: string
        subtotal: number
      }
    : never
  component: T extends 'section-title'
    ? InstanceType<typeof SectionArticle>
    : T extends 'section-article'
    ? InstanceType<typeof SectionArticle>
    : T extends 'section-subtotal'
    ? InstanceType<typeof SectionSubtotal>
    : never
}

export interface CatalogTemplate {
  id: number | null
  name: string
  values: Section<SectionsType.Article>['values']
  category_id: number | null
}
export interface CatalogCategory {
  id: number | null
  name: string
  templates: CatalogTemplate[]
}

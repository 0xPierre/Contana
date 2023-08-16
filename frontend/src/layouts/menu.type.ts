import type { RouteLocationRaw, RouteLocationNamedRaw } from 'vue-router'

export interface MenuLink {
  title?: string
  route?: RouteLocationRaw | RouteLocationNamedRaw
  icon?: string
  children?: MenuLink[]
  disabled?: boolean
  tag?: string
  tagVariant?: string
  href?: string
  target?: string
  header?: string
}

import { computed } from 'vue'
import type {
  RouteLocationNamedRaw,
  RouteLocationPathRaw,
  RouteRecordName,
  Router
} from 'vue-router'
import type { MenuLink } from './menu.type'

import VerticalNavMenuHeader from './layout-vertical/vertical-nav-menu/components/vertical-nav-menu-items/vertical-nav-menu-header/VerticalNavMenuHeader.vue'
import VerticalNavMenuGroup from './layout-vertical/vertical-nav-menu/components/vertical-nav-menu-items/vertical-nav-menu-group/VerticalNavMenuGroup.vue'
import VerticalNavMenuLink from './layout-vertical/vertical-nav-menu/components/vertical-nav-menu-items/vertical-nav-menu-link/VerticalNavMenuLink.vue'

/**
 * Return which component to render based on it's data/context
 * @param {Object} item nav menu item
 */
export const resolveVerticalNavMenuItemComponent = (item: MenuLink) => {
  if (item.header) return VerticalNavMenuHeader
  if (item.children) return VerticalNavMenuGroup
  return VerticalNavMenuLink
}

/**
 * Return route name for navigation link
 * If link is string then it will assume it is route-name
 * IF link is object it will resolve the object and will return the link
 * @param {Object, String} link navigation link object/string
 */
export const resolveNavDataRouteName = (
  link: MenuLink,
  router: Router
): RouteRecordName | undefined | null => {
  if (typeof link.route === 'object' && link.route !== null) {
    const route = router.resolve(link.route)
    return route.name
  }
  return link.route
}

/**
 * Check if nav-link is active
 * @param {Object} link nav-link object
 */
export const isNavLinkActive = (
  link: MenuLink,
  router: Router
): boolean => {
  // // Matched routes array of current route
  const matchedRoutes = router.currentRoute.value.matched

  // // Check if provided route matches route's matched route
  const resolveRoutedName = resolveNavDataRouteName(link, router)

  if (!resolveRoutedName) return false

  return matchedRoutes.some(
    (route) =>
      route.name === resolveRoutedName ||
      route.meta.navActiveLink === resolveRoutedName
  )
}

/**
 * Check if nav group is
 * @param {Array} children Group children
 */
export const isNavGroupActive = (
  children: MenuLink[],
  router: Router
): boolean => {
  // Matched routes array of current route
  const matchedRoutes = router.currentRoute.value.matched

  return children.some((child) => {
    // If child have children => It's group => Go deeper(recursive)
    if (child.children) {
      return isNavGroupActive(child.children, router)
    }

    // else it's link => Check for matched Route
    return isNavLinkActive(child, router)
  })
}

/**
 * Return b-link props to use
 * @param {Object, String} item navigation routeName or route Object provided in navigation data
 */
// prettier-ignore
export const navLinkProps = (item: MenuLink) => computed(() => {
  const props: {
    to?: RouteLocationPathRaw | RouteLocationNamedRaw | { name: string }
    href?: string
    target?: string | null
    rel?: string
  } = {}

  // If route is string => it assumes => Create route object from route name
  // If route is not string => It assumes it's route object => returns route object
  if (item.route) props.to = typeof item.route === 'string' ? { name: item.route } : item.route
  else {
    props.href = item.href
    props.target = '_blank'
    props.rel = 'nofollow'
  }

  if (!props.target) props.target = item.target || null

  return props
})

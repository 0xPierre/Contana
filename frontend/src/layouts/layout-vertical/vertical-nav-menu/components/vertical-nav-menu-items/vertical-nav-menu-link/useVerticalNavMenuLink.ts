import { ref } from 'vue'
import { isNavLinkActive, navLinkProps } from '@/layouts/utils'
import type { MenuLink } from '@/layouts/menu.type'
import { useRouter } from 'vue-router'

export default function useVerticalNavMenuLink(item: MenuLink) {
  const isActive = ref(false)
  const router = useRouter()

  const linkProps = navLinkProps(item)

  const updateIsActive = () => {
    isActive.value = isNavLinkActive(item, router)
  }

  return {
    isActive,
    linkProps,
    updateIsActive
  }
}

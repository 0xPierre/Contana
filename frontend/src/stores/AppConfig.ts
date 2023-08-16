import { defineStore, acceptHMRUpdate } from 'pinia'

export const useAppConfigStore = defineStore('app-config', {
  state: () => {
    return {
      theme: 'dark',
      navbar: {
        type: 'floating', // static , sticky , floating, hidden
        backgroundColor: ''
      },
      footer: {
        type: 'floating'
      },
      isVerticalMenuCollapsed: false,
      menu: {
        hidden: false
      },
      windowsWidth: 0
    }
  },

  getters: {},

  actions: {
    toggleTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark'

      if (this.theme === 'dark') {
        document.body.classList.add('dark-layout')
      } else {
        document.body.classList.remove('dark-layout')
      }
    },

    toggleVerticalMenuCollapsed() {
      this.isVerticalMenuCollapsed = !this.isVerticalMenuCollapsed
    }
  },

  persist: true
})

if (import.meta.hot) {
  import.meta.hot.accept(
    acceptHMRUpdate(useAppConfigStore, import.meta.hot)
  )
}

import { createApp } from 'vue'

import App from './App.vue'

const app = createApp(App)

import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

import router from './router'
app.use(router)

import { BootstrapVue } from 'bootstrap-vue'
app.use(BootstrapVue)

import VueFeather from 'vue-feather'
app.component(VueFeather.name, VueFeather)

import VSelect from './libs/vue-select.ts'
app.component('VSelect', VSelect)
import '@/assets/scss/template/vue/libs/vue-select.scss'

import VueFlatPickr from 'vue-flatpickr-component'
import flatpickr from 'flatpickr'
import { French } from 'flatpickr/dist/l10n/fr'
app.component(VueFlatPickr.name, VueFlatPickr)
import '@/assets/scss/template/vue/libs/vue-flatpicker.scss'

import Vue3ColorPicker from "vue3-colorpicker"
import "vue3-colorpicker/style.css"
createApp(App)
  .use(router)
  .use(Vue3ColorPicker)
  .mount("#app")

// @ts-ignore
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
app.component(VuePerfectScrollbar.name, VuePerfectScrollbar)

import VueApexCharts from 'vue3-apexcharts'
app.use(VueApexCharts)

import { createPlausible } from 'v-plausible/vue'

const plausible = createPlausible({
  init: {
    domain: 'app.contana.fr',
    apiHost: 'https://plausible.goubaud.com',
    trackLocalhost: false
  },
  settings: {
    enableAutoOutboundTracking: true,
    enableAutoPageviews: true
  },
  partytown: false
})

app.use(plausible)

// config flat pickr
flatpickr.defaultConfig = {
  ...flatpickr.defaultConfig,
  dateFormat: 'd/m/Y',
  locale: French
}

// @ts-ignore
import VueRipple from 'vue-ripple-directive'
VueRipple.color = 'rgba(255, 255, 255, 0.35)'
VueRipple.zIndex = 55
app.directive('ripple', VueRipple)

import Toast from 'vue-toastification'
import '@/assets/scss/template/vue/libs/toastification.scss'

app.use(Toast, {
  hideProgressBar: true,
  closeOnClick: false,
  closeButton: false,
  icon: false,
  timeout: 3000,
  transition: 'Vue-Toastification__fade'
})

import '@/assets/scss/style.scss'

app.mount('#app')

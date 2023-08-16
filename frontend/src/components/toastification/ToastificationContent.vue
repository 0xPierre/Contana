<script lang="ts" setup>
import { BAvatar } from 'bootstrap-vue'
import VueFeather from 'vue-feather'

defineProps<{
  variant: string
  icon: string
  title: string
  text: string
  hideClose: boolean
}>()

defineEmits(['close-toast'])
</script>

<template>
  <div class="toastification">
    <div class="d-flex align-items-start">
      <b-avatar
        :variant="variant"
        size="1.8rem"
        class="mr-75 flex-shrink-0"
      >
        <vue-feather :type="icon" size="15" />
      </b-avatar>
      <div class="d-flex flex-grow-1">
        <div>
          <h5
            v-if="title"
            class="mb-0 font-weight-bolder toastification-title"
            :class="`text-${variant}`"
            v-text="title"
          />
          <small
            v-if="text"
            class="d-inline-block text-body"
            v-text="text"
          />
        </div>
        <span
          class="cursor-pointer toastification-close-icon ml-auto"
          @click="$emit('close-toast')"
        >
          <vue-feather v-if="!hideClose" type="x" class="text-body" />
        </span>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.toastification-close-icon,
.toastification-title {
  line-height: 26px;
}

.toastification-title {
  color: inherit;
}
</style>

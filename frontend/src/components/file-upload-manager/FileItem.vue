<script lang="ts" setup>
import { computed } from 'vue'

const props = defineProps<{
  file:
    | File
    | {
        id: number
        url: string
      }
  previewFile?: boolean
}>()

const emit = defineEmits(['delete-file'])

const preview = computed(() => {
  if (props.file instanceof File) {
    return URL.createObjectURL(props.file)
  }
  return props.file.url
})

const fileName = computed(() => {
  if (props.file instanceof File) {
    return props.file.name
  }
  return props.file.url.split('/').pop().split('?')[0]
})

const fileUrl = computed(() => {
  if (!(props.file instanceof File)) {
    return props.file.url
  }
  return ''
})

const isImage = computed(() => {
  if (props.file instanceof File) {
    return props.file.type.includes('image')
  }

  return props.file.url.match(/\.(jpeg|jpg|gif|png)/)
})

const isPdf = computed(() => {
  if (props.file instanceof File) {
    return props.file.type.includes('pdf')
  }

  return props.file.url.match(/\.(pdf)$/)
})
</script>

<template>
  <div class="d-flex flex-column px-50 pb-2">
    <b-img class="file-img" v-if="previewFile && isImage" :src="preview" />
    <div
      v-else-if="previewFile && isPdf"
      class="d-flex align-items-center"
    >
      <object
        type="application/pdf"
        width="200"
        height="200"
        :data="preview"
      />
    </div>

    <span class="text-center">{{ fileName }}</span>
    <div class="d-flex">
      <b-button
        v-ripple
        variant="flat-danger"
        @click="emit('delete-file', props.file)"
      >
        Supprimer
      </b-button>
      <b-button
        v-if="props.file.hasOwnProperty('url')"
        v-ripple
        class="ml-1"
        variant="flat-primary"
        :href="fileUrl"
        target="_blank"
      >
        Télécharger
      </b-button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.file-img {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 10px;
}
</style>

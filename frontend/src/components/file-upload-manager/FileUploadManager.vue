<script lang="ts" setup>
import { ref } from 'vue'
import FileItem from './FileItem.vue'
import { notify } from '@/helpers/notify.ts'

const props = defineProps<{
  files: (
    | File
    | {
        id: number
        url: string
      }
  )[]
  multiple?: boolean
  preview?: boolean
  maxsize?: number
  accept?: string
  disabled?: boolean
  label?: string
}>()

const dragContainer = ref<HTMLElement | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const emit = defineEmits(['update-files'])

const onDragOver = (event: DragEvent) => {
  event.preventDefault()
  if (!dragContainer.value) return
  dragContainer.value.classList.add('dragging')
}

const onDragLeave = (event: DragEvent) => {
  event.preventDefault()
  if (!dragContainer.value) return
  dragContainer.value.classList.remove('dragging')
}

const onDrop = (event: DragEvent) => {
  event.preventDefault()
  if (!dragContainer.value) return
  dragContainer.value.classList.remove('dragging')

  if (props.accept) {
    const types = props.accept.split(',').map((type) => type.split('/')[0])
    const files = event.dataTransfer?.files
    if (!files) return

    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      if (!types.includes(file.type.split('/')[0])) {
        notify(`Le fichier ${file.name} n'est pas du bon type`, 'danger')
        return
      }
    }
  }

  const files = event.dataTransfer?.files
  if (!files) return

  if (props.multiple)
    emit('update-files', [...props.files, ...Array.from(files)])
  else emit('update-files', [files[0]])
}

const onChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!target.files) return

  if (props.multiple)
    emit('update-files', [...props.files, ...Array.from(target.files)])
  else emit('update-files', [target.files[0]])

  target.value = ''
}

const deleteFile = (index: number) => {
  const newFiles = [...props.files]
  newFiles.splice(index, 1)
  emit('update-files', newFiles)
}
</script>

<template>
  <div>
    <label class="font-medium-1" :for="disabled ? '' : 'fileInput'">
      <template v-if="label">{{ label }}</template>
      <template v-else
        >Glissez et déposez vos fichiers ou
        <span
          class="text-primary font-weight-bold"
          :class="{ 'cursor-pointer': !disabled }"
          >cliquez ici pour choisir un/des fichier</span
        ></template
      >
    </label>
    <div
      ref="dragContainer"
      @dragover="disabled ? null : onDragOver($event)"
      @dragleave="disabled ? null : onDragLeave($event)"
      @drop="disabled ? null : onDrop($event)"
      class="droppable-area"
      :class="props.files.length === 0 ? 'empty' : ''"
    >
      <input
        id="fileInput"
        type="file"
        ref="fileInput"
        class="d-none"
        :multiple="multiple"
        :accept="accept"
        @change="onChange"
      />
      <div v-if="props.files.length > 0" class="preview-list px-50 pt-50">
        <div class="d-flex flex-wrap">
          <FileItem
            v-for="(file, index) in props.files"
            :key="index"
            :file="file"
            :preview-file="props.preview"
            @delete-file="deleteFile(index)"
          />
        </div>
        <b-button
          variant="outline-primary"
          size="sm"
          class="mb-50"
          v-ripple
          @click="fileInput?.click()"
        >
          {{
            multiple ? 'Ajouter un/des fichier(s)' : 'Changer un fichier'
          }}
        </b-button>
      </div>
      <div
        v-else
        @click.self="disabled ? null : fileInput?.click()"
        class="d-flex justify-content-center align-items-center p-1"
      >
        Cliquer ou déposer pour ajouter un/des fichier(s)
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.droppable-area {
  border: 2px dashed rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  min-height: 150px;
  transition: background-color 0.2s;
  display: flex;
}
.dark-layout .droppable-area {
  border-color: #d0d2d6;
}
.dragging {
  background-color: rgba(0, 0, 0, 0.1);
}

.preview-list {
  margin-top: 10px;
}
</style>

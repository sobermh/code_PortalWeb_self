<template>
  <VContainer>
    <VFileUpload
      v-model="files"
      title="将文件拖放到此处"
      browse-text="浏览文件"
      multiple
      show-size
      clearable
      :accept="select_filetype"
      density="comfortable"
    >
      <template #item="{ props: itemProps }">
        <VFileUploadItem v-bind="itemProps" lines="one" nav>
          <template #prepend>
            <VAvatar size="48" rounded />
          </template>

          <template #clear="{ props: clearProps }">
            <VBtn color="primary" v-bind="clearProps" />
          </template>
        </VFileUploadItem>
      </template>
    </VFileUpload>
  </VContainer>
</template>

<script setup>
import { inject, watch } from 'vue'

const emit = defineEmits(['getFiles'])
const select_filetype = inject('select_filetype')

const files = ref(null)

const sendFiles = () => {
  emit('getFiles', files.value)
}

watch(files, (val) => {
  sendFiles()
})
</script>

<style scoped lang="scss">
.file-upload {
  color: red;
}
</style>

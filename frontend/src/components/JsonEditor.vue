<template>
  <JsonEditorVue
    v-model="json_data"
    :mode="mode"
    class="jse-theme-dark"
    :mainMenuBar="false"
    :navigationBar="false"
    v-bind="{
      /* local props & attrs */
    }"
  />
</template>

<script setup>
import JsonEditorVue from 'json-editor-vue'
import { inject, ref } from 'vue'
import { Mode } from 'vanilla-jsoneditor'
import 'vanilla-jsoneditor/themes/jse-theme-dark.css'

// 设置 mode 为文本模式
const mode = ref(Mode.text)

// 注入 json_data
const json_data = inject('json_data')

// 如果需要监听 json_data 的变化，可以解除注释
// watch(
//   json_data,
//   (newValue, oldValue) => {
//     console.log('Value changed:', newValue, 'Old value:', oldValue)
//   },
//   { deep: true },
// )
</script>

import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useToolsStore = defineStore('tools', () => {
  const plugin_base_url = ref(import.meta.env.VITE_PLUGIN_BASE_URL)
  const request_timeout = ref(parseInt(import.meta.env.VITE_REQUEST_TIMEOUT))
  const ai_base_url = ref(import.meta.env.VITE_AI_BASE_URL)
  const ai_download_url = ref(import.meta.env.VITE_AI_DOWNLOAD_URL)

  return {
    plugin_base_url,
    request_timeout,
    ai_base_url,
    ai_download_url,
  }
})

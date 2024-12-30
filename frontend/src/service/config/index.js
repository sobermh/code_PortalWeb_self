import { useToolsStore } from '@/stores'
const toolsStore = useToolsStore()

export const TIMEOUT = toolsStore.request_timeout

export const AI_BASE_URL = toolsStore.ai_base_url
export const AI_DOWNLOAD_URL = toolsStore.ai_download_url

export const PLUGIN_BASE_URL = toolsStore.plugin_base_url

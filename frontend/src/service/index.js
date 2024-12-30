import { AI_BASE_URL, PLUGIN_BASE_URL, AI_DOWNLOAD_URL, TIMEOUT } from './config'
import { AIRequest, PluginRequest } from './requests'

const aiRequest = new AIRequest({
  baseURL: AI_BASE_URL,
  timeout: TIMEOUT,
})

const aiDownloadRequest = new AIRequest({
  baseURL: AI_DOWNLOAD_URL,
  timeout: TIMEOUT,
})

const pluginRequest = new PluginRequest({
  baseURL: PLUGIN_BASE_URL,
  timeout: TIMEOUT,
})

export { aiRequest, pluginRequest, aiDownloadRequest }

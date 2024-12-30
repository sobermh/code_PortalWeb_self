import { aiRequest, pluginRequest, aiDownloadRequest } from '@/service'
import { useToolsStore } from '@/stores'

export const apiValidApiToken = (token) => {
  return aiDownloadRequest.post({
    url: '/token/valid/valid_token',
    data: { token },
  })
}

export const apiGetTools = () => {
  return aiRequest.post({
    url: '/execute',
    headers: { 'api-key': localStorage.getItem('app-token') },
    data: {
      name: 'info_data',
      func: 'post_guess_all',
      args: {
        db: 'msg_relation',
        guess: {},
        origin: true,
      },
    },
  })
}

export const apiGetDownloadUrl = (url) => {
  return aiDownloadRequest.post({
    url: '/file/drive/download_pike',
    headers: { 'api-key': localStorage.getItem('app-token') },
    data: {
      url,
    },
  })
}

export const apiDownloadTool = (url, onProgress) => {
  return aiRequest.get({
    url,
    responseType: 'blob',
    onDownloadProgress: (progressEvent) => {
      if (progressEvent.total) {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        if (onProgress) {
          onProgress(percentCompleted)
        }
      }
    },
  })
}

export const apiUploadBinary = (content, filename) => {
  return pluginRequest.post({
    url: '/execute',
    headers: { 'api-key': localStorage.getItem('app-token') },
    data: {
      name: 'file_upload',
      func: 'post_upload_binary',
      args: {
        content,
        filename,
      },
    },
  })
}

export const apiDownloadBinary = (filename) => {
  return pluginRequest.post({
    url: '/execute',
    headers: { 'api-key': localStorage.getItem('app-token') },
    data: {
      name: 'file_upload',
      func: 'post_down_binary',
      args: {
        filename,
      },
    },
  })
}

export const apiTransi2i = (inpath, ext) => {
  return pluginRequest.post({
    url: '/execute',
    headers: { 'api-key': localStorage.getItem('app-token') },
    data: {
      name: 'aigc_image',
      func: 'post_trans_i2i',
      args: {
        inpath,
        ext,
      },
    },
  })
}

export const apiTransv2v = (inpath, ext) => {
  return pluginRequest.post({
    url: '/execute',
    headers: { 'api-key': localStorage.getItem('app-token') },
    data: {
      name: 'aigc_video',
      func: 'post_trans_v2v',
      args: {
        inpath,
        ext,
      },
    },
  })
}

export const apiTransa2a = (inpath, ext) => {
  return pluginRequest.post({
    url: '/execute',
    headers: { 'api-key': localStorage.getItem('app-token') },
    data: {
      name: 'aigc_audio',
      func: 'post_trans_a2a',
      args: {
        inpath,
        ext,
      },
    },
  })
}

export const apiRemoveBgi = (inpath) => {
  return pluginRequest.post({
    url: '/execute',
    headers: { 'api-key': localStorage.getItem('app-token') },
    data: {
      name: 'aigc_image',
      func: 'post_remove_bg',
      args: {
        inpath,
      },
    },
  })
}

export const apiRemoveFgi = (inpath) => {
  return pluginRequest.post({
    url: '/execute',
    headers: { 'api-key': localStorage.getItem('app-token') },
    data: {
      name: 'aigc_image',
      func: 'post_remove_fg',
      args: {
        inpath,
      },
    },
  })
}

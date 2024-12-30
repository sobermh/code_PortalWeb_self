import axios from 'axios'
import router from '@/router'
import appSonner from '@/utils/appSonner'
class BaseRequest {
  constructor(config) {
    this.instance = axios.create(config)

    this.instance.interceptors.request.use(
      (config) => config,
      (err) => Promise.reject(err),
    )

    this.instance.interceptors.response.use(
      (res) => res.data,
      (err) => {
        if (err.response?.status === 403) {
          router.push('/')
          appSonner.error('登录已过期，请重新登录')
        } else {
          return {
            code: err.response?.status || 500,
            message: err.message || '未知错误',
          }
        }
      },
    )

    if (config.interceptors) {
      this.instance.interceptors.request.use(
        config.interceptors.requestSuccessFn,
        config.interceptors.requestFailureFn,
      )

      this.instance.interceptors.response.use(
        config.interceptors.responseSuccessFn,
        config.interceptors.responseFailureFn,
      )
    }
  }

  request(config) {
    return this.instance.request(config)
  }

  get(config) {
    return this.request({ ...config, method: 'GET' })
  }

  post(config) {
    return this.request({ ...config, method: 'POST' })
  }

  delete(config) {
    return this.request({ ...config, method: 'DELETE' })
  }

  patch(config) {
    return this.request({ ...config, method: 'PATCH' })
  }

  put(config) {
    return this.request({ ...config, method: 'PUT' })
  }
}

class AIRequest extends BaseRequest {
  setTimeout(time) {
    this.instance.defaults.timeout = time
  }
}

class PluginRequest extends BaseRequest {
  setBaseURL(url) {
    this.instance.defaults.baseURL = url
  }

  setTimeout(time) {
    this.instance.defaults.timeout = time
  }
}

export { AIRequest, PluginRequest }

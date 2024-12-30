const CacheType = {
  Local: 0,
  Session: 1,
}

class Cache {
  constructor(type) {
    this.storage = type === CacheType.Local ? localStorage : sessionStorage
  }

  setCache(key, value) {
    if (value) {
      this.storage.setItem(key, JSON.stringify(value))
    }
  }

  getCache(key) {
    const value = this.storage.getItem(key)
    if (value) {
      try {
        return JSON.parse(value)
      } catch (e) {
        return value
      }
    }
    return null
  }

  removeCache(key) {
    this.storage.removeItem(key)
  }

  clearCache() {
    this.storage.clear()
  }
}

const localCache = new Cache(CacheType.Local)
const sessionCache = new Cache(CacheType.Session)

export { localCache, sessionCache }

/**
 * API 请求工具
 */

// API 基础地址
let BASE_URL = ''

if (import.meta.env.DEV) {
  if (typeof window !== 'undefined') {
    // H5 开发环境：使用当前访问的 origin（如 http://192.168.x.x:6000）
    // 这样可以确保请求发送到 Vite 开发服务器，再由 Vite 代理到后端
    BASE_URL = window.location.origin
  } else {
    // 非 H5 环境（如小程序 IDE）：默认连接本地后端
    BASE_URL = 'http://localhost:8000'
  }
} else {
  // 生产环境
  BASE_URL = 'https://api.yourdomain.com'
}

/**
 * 发起请求
 * @param {string} url - 请求地址
 * @param {object} options - 请求配置
 * @returns {Promise}
 */
function request(url, options = {}) {
  const { method = 'GET', data = null, header = {} } = options
  
  // 确保 url 以 / 开头
  const normalizedUrl = url.startsWith('/') ? url : `/${url}`
  let fullUrl = `${BASE_URL}${normalizedUrl}`
  
  // GET 请求增加时间戳防止缓存
  if (method.toUpperCase() === 'GET') {
    const separator = fullUrl.includes('?') ? '&' : '?'
    fullUrl = `${fullUrl}${separator}_t=${Date.now()}`
  }

  const requestConfig = {
    url: fullUrl,
    method: method.toUpperCase(),
    header: {
      'Content-Type': 'application/json',
      ...header
    },
    timeout: 60000  // 60 秒超时
  }

  // 调试信息：保存到全局变量以便在 UI 上显示
  if (typeof window !== 'undefined') {
    window.__LAST_REQUEST__ = {
      url: fullUrl,
      method: requestConfig.method,
      time: new Date().toLocaleTimeString()
    }
  }

  if (data) {
    requestConfig.data = data
  }

  return new Promise((resolve, reject) => {
    console.log(`[API Request] ${method} ${fullUrl}`, data)
    uni.request({
      ...requestConfig,
      success: (res) => {
        console.log(`[API Response]`, res.statusCode, res.data)
        
        // 更新调试信息
        if (typeof window !== 'undefined') {
          window.__LAST_RESPONSE__ = {
             status: res.statusCode,
             data: res.data,
             time: new Date().toLocaleTimeString()
          }
        }

        if (res.statusCode === 200) {
          if (res.data.code === 0) {
            resolve(res.data)
          } else {
            uni.showToast({
              title: res.data.message || '请求失败',
              icon: 'none'
            })
            reject(res.data)
          }
        } else {
          uni.showToast({
            title: `网络错误 (${res.statusCode})`,
            icon: 'none'
          })
          reject(new Error(`HTTP ${res.statusCode}`))
        }
      },
      fail: (err) => {
        console.error(`[API Error]`, err)
        
        // 更新调试信息
        if (typeof window !== 'undefined') {
          window.__LAST_ERROR__ = {
             err: err,
             msg: err.errMsg,
             time: new Date().toLocaleTimeString()
          }
        }

        let errorMsg = '网络连接失败'
        if (err.errMsg && err.errMsg.includes('timeout')) {
          errorMsg = '请求超时(>60s)，请检查网络'
        } else if (err.errMsg && err.errMsg.includes('fail')) {
          // 尝试提供更详细的错误提示
          errorMsg = `连接失败: ${err.errMsg}`
        }
        console.error(`Request failed: ${fullUrl}`, err)
        uni.showToast({
          title: errorMsg,
          icon: 'none',
          duration: 3000
        })
        reject(err)
      }
    })
  })
}

/**
 * GET 请求
 */
export function get(url, params = {}) {
  const query = Object.keys(params)
    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
    .join('&')

  const fullUrl = query ? `${url}?${query}` : url

  return request(fullUrl, { method: 'GET' })
}

/**
 * POST 请求
 */
export function post(url, data = {}) {
  return request(url, { method: 'POST', data })
}

export default {
  get,
  post
}

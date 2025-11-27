// 全局工具函数
const config = require('../config/index.js')

/**
 * 将普通URL转换为代理URL
 * @param {string} url - 原始图片URL
 * @param {string} responseType - 返回类型: 'base64' 或 'binary'
 * @returns {string} 代理URL
 */
function convertToProxyUrl(url, responseType = 'binary') {
  if (!url) return ''
  
  // 如果已经是代理URL，直接返回
  if (url.includes('/api/proxy/image')) {
    return url
  }
  
  // 使用配置文件中的代理端点
  const proxyEndpoint = config.apiUrls.image.proxy || '/api/proxy/image'
  const proxyUrl = `${config.appDomain}${proxyEndpoint}?url=${encodeURIComponent(url)}&response_type=${responseType}`
  return proxyUrl
}

/**
 * 简化的代理URL函数别名
 * @param {string} url - 原始图片URL
 * @returns {string} 代理URL
 */
function toProxied(url) {
  return convertToProxyUrl(url, 'binary')
}

/**
 * 构建完整的API URL
 * @param {string} endpoint - API端点
 * @param {object} params - URL参数
 * @returns {string} 完整的API URL
 */
function buildApiUrl(endpoint, params = {}) {
  const baseUrl = config.appDomain
  const url = new URL(endpoint, baseUrl)
  
  // 添加查询参数
  Object.keys(params).forEach(key => {
    if (params[key] !== null && params[key] !== undefined) {
      url.searchParams.append(key, params[key])
    }
  })
  
  return url.toString()
}

/**
 * 格式化日期
 * @param {string|Date} date - 日期
 * @param {string} format - 格式
 * @returns {string} 格式化后的日期
 */
function formatDate(date, format = 'YYYY-MM-DD') {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')
  
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

/**
 * 显示提示消息
 * @param {string} title - 标题
 * @param {string} icon - 图标类型
 * @param {number} duration - 持续时间
 */
function showToast(title, icon = 'none', duration = 2000) {
  wx.showToast({
    title,
    icon,
    duration
  })
}

/**
 * 显示加载中
 * @param {string} title - 标题
 */
function showLoading(title = '加载中...') {
  wx.showLoading({
    title,
    mask: true
  })
}

/**
 * 隐藏加载中
 */
function hideLoading() {
  wx.hideLoading()
}

module.exports = {
  convertToProxyUrl,
  toProxied,
  buildApiUrl,
  formatDate,
  showToast,
  showLoading,
  hideLoading,
  config
}
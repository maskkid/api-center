const modules = require('../../config/modules')
const utils = require('../../utils/index.js')
const { toProxied, config } = utils

Page({
  data: {
    homeModules: [],
    items: []
  },
  onLoad() {
    const m = modules.filter(x => x.enabled && x.showOnHome)
    
    // 从后端API获取分享列表（获取最新的10条）
    wx.request({
      url: `${config.appDomain}${config.apiUrls.shares.list}`,
      method: 'GET',
      data: {
        page: 1,
        page_size: 10
      },
      success: (res) => {
        console.log('获取分享列表成功:', res)
        
        if (res.statusCode === 200 && res.data && res.data.items) {
          // 转换后端数据格式
          const items = res.data.items.map(item => {
            const resource = item.resource
            const share = item.share
            const images = resource.image ? resource.image.split(',').filter(img => img.trim()) : []
            
            return {
              id: resource.res_id,
              text: resource.text || '',
              images: images.map(img => toProxied(img.trim())),
              shareCode: share.share_code,
              shareNum: share.share_num || 0,
              downloadNum: share.download_num || 0
            }
          })
          
          this.setData({ 
            homeModules: m,
            items: items
          })
        } else {
          console.error('API返回数据格式错误:', res)
          // 如果API调用失败，使用示例数据
          this.loadDemoData(m)
        }
      },
      fail: (error) => {
        console.error('获取分享列表失败:', error)
        // 使用示例数据作为fallback
        this.loadDemoData(m)
      }
    })
  },
  
  loadDemoData(modules) {
    
    
    this.setData({ 
      homeModules: modules,
      items: []
    })
  },
  onEnterModule(e) {
    const tag = e.currentTarget.dataset.tag
    const url = `/pages/modules/${tag}/index`
    wx.navigateTo({ url })
  },
  onPreviewImage(e) {
    const src = e.currentTarget.dataset.src
    const current = src
    const urls = this.data.items.flatMap(i => i.images)
    wx.previewImage({ current, urls })
  },
  async onOneClickDownload(e) {
    const text = e.currentTarget.dataset.text
    const images = e.currentTarget.dataset.images || []
    
    // 1. 复制文案
    try {
      await wx.setClipboardData({ data: text })
      wx.showToast({ title: '文案已复制', icon: 'success' })
    } catch (err) {
      wx.showToast({ title: '复制失败', icon: 'error' })
      return
    }
    
    // 2. 下载所有图片到相册
    if (images.length > 0) {
      let successCount = 0
      for (const src of images) {
        try {
          const dl = await wx.downloadFile({ url: src })
          if (dl.statusCode === 200) {
            await wx.saveImageToPhotosAlbum({ filePath: dl.tempFilePath })
            successCount++
          }
        } catch (err) {
          console.error('下载图片失败:', err)
        }
      }
      
      if (successCount > 0) {
        wx.showToast({ 
          title: `已下载${successCount}张图片`, 
          icon: 'success',
          duration: 2000
        })
      } else {
        wx.showToast({ 
          title: '图片下载失败', 
          icon: 'error' 
        })
      }
    }
  },
  onNavigateToDetail(e) {
    const shareCode = e.currentTarget.dataset.shareCode
    if (shareCode) {
      wx.navigateTo({
        url: `/pages/modules/wenan/detail?share_code=${shareCode}`
      })
    }
  }
})

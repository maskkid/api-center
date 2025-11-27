const modules = require('../../config/modules')

const appDomain = ''

function toProxied(url) {
  if (!appDomain) return url
  return `${appDomain}/api/v1/gateway/proxy?url=${encodeURIComponent(url)}`
}

Page({
  data: {
    homeModules: [],
    items: []
  },
  onLoad() {
    const m = modules.filter(x => x.enabled && x.showOnHome)
    
    // 添加示例文案数据
    const demoItems = [
      {
        id: 1,
        text: '精选文案：记录生活中的美好瞬间',
        images: [
          toProxied('https://picsum.photos/300'),
          toProxied('https://picsum.photos/301')
        ]
      },
      {
        id: 2,
        text: '每日分享：发现身边的小确幸',
        images: [
          toProxied('https://picsum.photos/302'),
          toProxied('https://picsum.photos/303')
        ]
      },
      {
        id: 3,
        text: '生活感悟：用心感受每一个当下',
        images: [
          toProxied('https://picsum.photos/304')
        ]
      }
    ]
    
    this.setData({ 
      homeModules: m,
      items: demoItems
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
  }
})

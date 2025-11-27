const appDomain = 'http://localhost:8001'  // 后端服务地址

function toProxied(url) {
  if (!appDomain) return url
  // 使用新的代理接口 - 图片使用专门的图片代理接口
  const isImage = /\.(jpg|jpeg|png|gif|bmp|webp|svg)$/i.test(url)
  const endpoint = isImage ? '/api/v1/image' : '/api/v1/proxy'
  return `${appDomain}${endpoint}?url=${encodeURIComponent(url)}&response_type=binary`
}

Page({
  data: {
    items: [],
    page: 1,
    pageSize: 10,
    hasMore: true,
    loading: false
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
  async onLoad() {
    // 初始化加载第一页数据
    await this.loadShares(1)
  },
  
  async onReachBottom() {
    // 下拉加载更多
    if (this.data.hasMore && !this.data.loading) {
      await this.loadShares(this.data.page + 1)
    }
  },
  
  onPullDownRefresh() {
    // 上拉刷新
    this.loadShares(1, true)
    wx.stopPullDownRefresh()
  },
  
  loadShares(page = 1, refresh = false) {
    if (this.data.loading) return
    
    this.setData({ loading: true })
    
    wx.request({
      url: `${appDomain}/api/shares/shares`,
      method: 'GET',
      data: {
        page: page,
        page_size: this.data.pageSize
      },
      success: (res) => {
        if (res.statusCode === 200 && res.data && res.data.items) {
          // 转换后端数据格式
          const newItems = res.data.items.map(item => {
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
          
          let items = []
          if (refresh) {
            items = newItems
          } else {
            items = page === 1 ? newItems : [...this.data.items, ...newItems]
          }
          
          this.setData({ 
            items: items,
            page: page,
            hasMore: newItems.length === this.data.pageSize,
            loading: false
          })
        } else {
          console.error('API返回数据格式错误:', res)
          // 如果API调用失败，使用示例数据
          this.loadDemoData()
        }
      },
      fail: (error) => {
        console.error('获取分享列表失败:', error)
        this.setData({ loading: false })
        // 使用示例数据作为fallback
        if (page === 1) {
          this.loadDemoData()
        }
      }
    })
  },
  
  loadDemoData() {
    const demo = [
      {
        id: 1,
        text: '示例文案：记录美好瞬间',
        images: [
          toProxied('https://picsum.photos/300'),
          toProxied('https://picsum.photos/301')
        ]
      },
      {
        id: 2,
        text: '示例文案：发现生活之美',
        images: [
          toProxied('https://picsum.photos/302'),
          toProxied('https://picsum.photos/303')
        ]
      }
    ]
    this.setData({ items: demo })
  },
  onPreviewImage(e) {
    const src = e.currentTarget.dataset.src
    const current = src
    const urls = this.data.items.flatMap(i => i.images)
    wx.previewImage({ current, urls })
  },
  onCopyText(e) {
    const text = e.currentTarget.dataset.text
    wx.setClipboardData({ data: text })
  },
  async onDownloadImages(e) {
    const images = e.currentTarget.dataset.images || []
    for (const src of images) {
      try {
        const dl = await wx.downloadFile({ url: src })
        if (dl.statusCode === 200) {
          await wx.saveImageToPhotosAlbum({ filePath: dl.tempFilePath })
        }
      } catch (err) {}
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

const { buildApiUrl, convertToProxyUrl } = require('../../../utils/index.js')

Page({
  data: {
    content: '',
    images: [],
    shareCode: '',
    shareNum: 0,
    downloadNum: 0,
    disabled: false,
    loading: true
  },

  onLoad(options) {
    // 获取分享码参数
    const { share_code } = options
    
    if (share_code) {
      this.setData({ shareCode: share_code })
      this.loadShareDetail(share_code)
    } else {
      // 兼容旧参数格式
      const { content, images } = options
      
      if (content) {
        // 解码URL参数
        const decodedContent = decodeURIComponent(content)
        this.setData({ content: decodedContent })
      }
      
      if (images) {
        // 处理图片参数，可能是逗号分隔的字符串或JSON字符串
        try {
          // 尝试解析为JSON数组
          const imageArray = JSON.parse(decodeURIComponent(images))
          this.setData({ images: imageArray })
        } catch (e) {
          // 如果不是JSON，尝试按逗号分割
          const imageArray = decodeURIComponent(images).split(',').filter(img => img.trim())
          this.setData({ images: imageArray })
        }
      }
      
      this.setData({ loading: false })
    }
    
    // 设置页面标题
    wx.setNavigationBarTitle({
      title: '文案详情'
    })
  },
  
  loadShareDetail(shareCode) {
    // 获取当前页面的channel参数（如果有）
    const pages = getCurrentPages()
    const currentPage = pages[pages.length - 1]
    const options = currentPage.options
    const channel = options.channel || ''
    
    // 构建请求参数
    const params = {}
    if (channel) {
      params.channel = channel
    }
    
    // 调用后端API获取分享详情
    wx.request({
      url: buildApiUrl(`/api/shares/shares/code/${shareCode}`),
      method: 'GET',
      data: params,
      success: (res) => {
        if (res.statusCode === 200 && res.data) {
          const { resource, share, disabled } = res.data
          
          if (resource && share) {
            // 处理图片数据
            const images = resource.image ? resource.image.split(',').filter(img => img.trim()) : []
            
            this.setData({
              content: resource.text || '',
              images: images.map(img => convertToProxyUrl(img.trim(), 'binary')),
              shareNum: share.share_num || 0,
              downloadNum: share.download_num || 0,
              disabled: disabled || false,
              loading: false
            })
          } else {
            this.handleLoadError(new Error('数据格式错误'))
          }
        } else {
          this.handleLoadError(new Error(res.data?.detail || '获取分享详情失败'))
        }
      },
      fail: (error) => {
        console.error('获取分享详情失败:', error)
        this.handleLoadError(error)
      }
    })
  },
  
  handleLoadError(error) {
    // 显示错误提示
    wx.showToast({
      title: error.message || '获取分享详情失败',
      icon: 'error'
    })
    
    this.setData({ loading: false })
    
    // 如果获取失败，返回上一页
    setTimeout(() => {
      wx.navigateBack()
    }, 2000)
  },

  // 预览图片
  onPreviewImage(e) {
    const { src } = e.currentTarget.dataset
    wx.previewImage({
      urls: this.data.images,
      current: src
    })
  },

  // 一键下载功能（复制文案+下载图片）
  onOneClickDownload() {
    const { content, images } = this.data
    
    if (!content && (!images || images.length === 0)) {
      wx.showToast({
        title: '没有内容可下载',
        icon: 'none'
      })
      return
    }

    // 复制文案
    if (content) {
      wx.setClipboardData({
        data: content,
        success: () => {
          wx.showToast({
            title: '文案已复制',
            icon: 'success',
            duration: 1500
          })
        },
        fail: () => {
          wx.showToast({
            title: '复制失败',
            icon: 'error'
          })
        }
      })
    }

    // 下载图片到相册
    if (images && images.length > 0) {
      this.downloadImages(images)
    }
  },

  // 下载图片到相册
  async downloadImages(imageUrls) {
    let successCount = 0
    let failCount = 0

    for (let i = 0; i < imageUrls.length; i++) {
      try {
        // 下载图片到临时路径
        const downloadRes = await new Promise((resolve, reject) => {
          wx.downloadFile({
            url: imageUrls[i],
            success: resolve,
            fail: reject
          })
        })

        if (downloadRes.statusCode === 200) {
          // 保存到相册
          await new Promise((resolve, reject) => {
            wx.saveImageToPhotosAlbum({
              filePath: downloadRes.tempFilePath,
              success: resolve,
              fail: reject
            })
          })
          successCount++
        } else {
          failCount++
        }
      } catch (error) {
        failCount++
        console.error('下载图片失败:', error)
      }
    }

    // 显示下载结果
    if (successCount > 0) {
      wx.showToast({
        title: `已下载${successCount}张图片`,
        icon: 'success',
        duration: 2000
      })
    }
    
    if (failCount > 0) {
      wx.showToast({
        title: `${failCount}张图片下载失败`,
        icon: 'none',
        duration: 2000
      })
    }

    // 处理权限问题
    if (failCount > 0) {
      wx.getSetting({
        success: (res) => {
          if (!res.authSetting['scope.writePhotosAlbum']) {
            wx.showModal({
              title: '需要授权',
              content: '请允许访问相册以保存图片',
              success: (modalRes) => {
                if (modalRes.confirm) {
                  wx.openSetting()
                }
              }
            })
          }
        }
      })
    }
  }
})
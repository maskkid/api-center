Page({
  data: {
    content: '',
    images: []
  },

  onLoad(options) {
    // 接收从其他小程序或网页跳转传入的参数
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
    
    // 设置页面标题
    wx.setNavigationBarTitle({
      title: '文案详情'
    })
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
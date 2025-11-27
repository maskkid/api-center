const appDomain = ''

function toProxied(url) {
  if (!appDomain) return url
  return `${appDomain}/api/v1/gateway/proxy?url=${encodeURIComponent(url)}`
}

Page({
  data: {
    templates: [
      {
        id: 1,
        name: '2宫格',
        rows: 1,
        cols: 2,
        cells: [
          { row: 1, col: 1, colSpan: 1, rowSpan: 1 },
          { row: 1, col: 2, colSpan: 1, rowSpan: 1 }
        ]
      },
      {
        id: 2,
        name: '左1右2',
        rows: 2,
        cols: 3,
        cells: [
          { row: 1, col: 1, colSpan: 2, rowSpan: 2 },
          { row: 1, col: 3, colSpan: 1, rowSpan: 1 },
          { row: 2, col: 3, colSpan: 1, rowSpan: 1 }
        ]
      },
      {
        id: 3,
        name: '上1下2',
        rows: 3,
        cols: 2,
        cells: [
          { row: 1, col: 1, colSpan: 2, rowSpan: 1 },
          { row: 2, col: 1, colSpan: 1, rowSpan: 1 },
          { row: 2, col: 2, colSpan: 1, rowSpan: 1 }
        ]
      },
      {
        id: 4,
        name: '3角形',
        rows: 2,
        cols: 2,
        cells: [
          { row: 1, col: 1, colSpan: 1, rowSpan: 1 },
          { row: 1, col: 2, colSpan: 1, rowSpan: 1 },
          { row: 2, col: 1, colSpan: 2, rowSpan: 1 }
        ]
      },
      {
        id: 5,
        name: '梯形布局',
        rows: 3,
        cols: 3,
        cells: [
          { row: 1, col: 2, colSpan: 1, rowSpan: 1 },
          { row: 2, col: 1, colSpan: 3, rowSpan: 1 },
          { row: 3, col: 2, colSpan: 1, rowSpan: 1 }
        ]
      },
      {
        id: 6,
        name: '4宫格',
        rows: 2,
        cols: 2,
        cells: [
          { row: 1, col: 1, colSpan: 1, rowSpan: 1 },
          { row: 1, col: 2, colSpan: 1, rowSpan: 1 },
          { row: 2, col: 1, colSpan: 1, rowSpan: 1 },
          { row: 2, col: 2, colSpan: 1, rowSpan: 1 }
        ]
      },
      {
        id: 7,
        name: '6宫格',
        rows: 2,
        cols: 3,
        cells: [
          { row: 1, col: 1, colSpan: 1, rowSpan: 1 },
          { row: 1, col: 2, colSpan: 1, rowSpan: 1 },
          { row: 1, col: 3, colSpan: 1, rowSpan: 1 },
          { row: 2, col: 1, colSpan: 1, rowSpan: 1 },
          { row: 2, col: 2, colSpan: 1, rowSpan: 1 },
          { row: 2, col: 3, colSpan: 1, rowSpan: 1 }
        ]
      },
      {
        id: 8,
        name: '9宫格',
        rows: 3,
        cols: 3,
        cells: [
          { row: 1, col: 1, colSpan: 1, rowSpan: 1 },
          { row: 1, col: 2, colSpan: 1, rowSpan: 1 },
          { row: 1, col: 3, colSpan: 1, rowSpan: 1 },
          { row: 2, col: 1, colSpan: 1, rowSpan: 1 },
          { row: 2, col: 2, colSpan: 1, rowSpan: 1 },
          { row: 2, col: 3, colSpan: 1, rowSpan: 1 },
          { row: 3, col: 1, colSpan: 1, rowSpan: 1 },
          { row: 3, col: 2, colSpan: 1, rowSpan: 1 },
          { row: 3, col: 3, colSpan: 1, rowSpan: 1 }
        ]
      },
      {
        id: 9,
        name: '大图+小图',
        rows: 2,
        cols: 3,
        cells: [
          { row: 1, col: 1, colSpan: 2, rowSpan: 2 },
          { row: 1, col: 3, colSpan: 1, rowSpan: 1 },
          { row: 2, col: 3, colSpan: 1, rowSpan: 1 }
        ]
      }
    ],
    selectedTemplate: {},
    imageList: [],
    generatedImage: '',
    dragIndex: -1,
    canGenerate: false
  },

  onLoad() {
    // 默认选择第一个模板
    this.selectTemplate({ currentTarget: { dataset: { template: this.data.templates[0] } } })
  },

  selectTemplate(e) {
    const template = e.currentTarget.dataset.template
    const imageList = template.cells.map((cell, index) => ({
      ...cell,
      index,
      image: '',
      tempFilePath: ''
    }))
    
    this.setData({
      selectedTemplate: template,
      imageList,
      generatedImage: '',
      canGenerate: false
    })
  },

  selectImage(e) {
    const index = e.currentTarget.dataset.index
    const currentImage = this.data.imageList[index]
    
    if (currentImage.image) {
      return // 如果已有图片，不重新选择
    }
    
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const tempFilePath = res.tempFilePaths[0]
        const imageList = [...this.data.imageList]
        imageList[index] = {
          ...imageList[index],
          image: tempFilePath,
          tempFilePath
        }
        
        const canGenerate = imageList.every(item => item.image)
        
        this.setData({
          imageList,
          canGenerate
        })
      }
    })
  },

  removeImage(e) {
    const index = e.currentTarget.dataset.index
    const imageList = [...this.data.imageList]
    imageList[index] = {
      ...imageList[index],
      image: '',
      tempFilePath: ''
    }
    
    this.setData({
      imageList,
      canGenerate: false
    })
  },

  resetImages() {
    const imageList = this.data.imageList.map(item => ({
      ...item,
      image: '',
      tempFilePath: ''
    }))
    
    this.setData({
      imageList,
      generatedImage: '',
      canGenerate: false
    })
  },

  // 拖拽功能
  onTouchStart(e) {
    const index = e.currentTarget.dataset.index
    this.setData({ dragIndex: index })
    
    // 记录触摸起始位置
    this.startX = e.touches[0].clientX
    this.startY = e.touches[0].clientY
  },

  onTouchMove(e) {
    // 这里可以实现拖拽时的视觉反馈
  },

  onTouchEnd(e) {
    const dragIndex = this.data.dragIndex
    if (dragIndex === -1) return
    
    // 获取触摸结束位置
    const endX = e.changedTouches[0].clientX
    const endY = e.changedTouches[0].clientY
    
    // 计算移动距离
    const deltaX = Math.abs(endX - this.startX)
    const deltaY = Math.abs(endY - this.startY)
    
    // 如果移动距离太小，认为是点击
    if (deltaX < 30 && deltaY < 30) {
      this.setData({ dragIndex: -1 })
      return
    }
    
    // 查找目标位置
    const query = wx.createSelectorQuery().in(this)
    query.selectAll('.image-cell').boundingClientRect((rects) => {
      let targetIndex = -1
      
      rects.forEach((rect, index) => {
        if (index !== dragIndex && 
            endX >= rect.left && endX <= rect.right &&
            endY >= rect.top && endY <= rect.bottom) {
          targetIndex = index
        }
      })
      
      if (targetIndex !== -1) {
        // 交换图片
        const imageList = [...this.data.imageList]
        const dragImage = imageList[dragIndex].image
        const dragTempPath = imageList[dragIndex].tempFilePath
        
        imageList[dragIndex].image = imageList[targetIndex].image
        imageList[dragIndex].tempFilePath = imageList[targetIndex].tempFilePath
        imageList[targetIndex].image = dragImage
        imageList[targetIndex].tempFilePath = dragTempPath
        
        this.setData({ imageList })
      }
      
      this.setData({ dragIndex: -1 })
    }).exec()
  },

  // 生成拼接图
  async generateCollage() {
    if (!this.data.canGenerate) return
    
    wx.showLoading({ title: '生成中...' })
    
    try {
      const { selectedTemplate, imageList } = this.data
      const canvasWidth = 1080 // 生成高清图片
      const canvasHeight = 1080
      const cellWidth = canvasWidth / selectedTemplate.cols
      const cellHeight = canvasHeight / selectedTemplate.rows
      
      // 创建 canvas 上下文
      const query = wx.createSelectorQuery()
      query.select('#collage-canvas').fields({ node: true, size: true }).exec((res) => {
        const canvas = res[0].node
        const ctx = canvas.getContext('2d')
        
        // 设置 canvas 尺寸
        canvas.width = canvasWidth
        canvas.height = canvasHeight
        
        // 白色背景
        ctx.fillStyle = '#ffffff'
        ctx.fillRect(0, 0, canvasWidth, canvasHeight)
        
        // 添加整体阴影效果
        ctx.shadowColor = 'rgba(0, 0, 0, 0.1)'
        ctx.shadowBlur = 20
        ctx.shadowOffsetX = 0
        ctx.shadowOffsetY = 10
        
        // 绘制每个图片
        let loadedCount = 0
        const totalImages = imageList.length
        
        // 添加圆角矩形裁剪函数
        const roundRect = (ctx, x, y, width, height, radius) => {
          ctx.beginPath()
          ctx.moveTo(x + radius, y)
          ctx.lineTo(x + width - radius, y)
          ctx.quadraticCurveTo(x + width, y, x + width, y + radius)
          ctx.lineTo(x + width, y + height - radius)
          ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height)
          ctx.lineTo(x + radius, y + height)
          ctx.quadraticCurveTo(x, y + height, x, y + height - radius)
          ctx.lineTo(x, y + radius)
          ctx.quadraticCurveTo(x, y, x + radius, y)
          ctx.closePath()
        }
        
        imageList.forEach((item, index) => {
          const img = canvas.createImage()
          img.onload = () => {
            const x = (item.col - 1) * cellWidth
            const y = (item.row - 1) * cellHeight
            const width = item.colSpan * cellWidth
            const height = item.rowSpan * cellHeight
            
            // 根据模板ID添加特殊形状效果
            if (selectedTemplate.id === 5) {
              // 梯形布局 - 添加圆角和特殊裁剪
              ctx.save()
              roundRect(ctx, x + 10, y + 10, width - 20, height - 20, 20)
              ctx.clip()
              ctx.drawImage(img, x + 10, y + 10, width - 20, height - 20)
              ctx.restore()
              
              // 添加边框
              ctx.strokeStyle = '#ffffff'
              ctx.lineWidth = 6
              roundRect(ctx, x + 10, y + 10, width - 20, height - 20, 20)
              ctx.stroke()
            } else {
              // 普通布局 - 添加圆角和边框
              const padding = 8
              ctx.save()
              roundRect(ctx, x + padding, y + padding, width - padding * 2, height - padding * 2, 12)
              ctx.clip()
              ctx.drawImage(img, x + padding, y + padding, width - padding * 2, height - padding * 2)
              ctx.restore()
              
              // 添加边框
              ctx.strokeStyle = '#ffffff'
              ctx.lineWidth = 4
              roundRect(ctx, x + padding, y + padding, width - padding * 2, height - padding * 2, 12)
              ctx.stroke()
            }
            
            loadedCount++
            if (loadedCount === totalImages) {
              // 所有图片加载完成，导出最终图片
              wx.canvasToTempFilePath({
                canvas,
                success: (res) => {
                  this.setData({ generatedImage: res.tempFilePath })
                  wx.hideLoading()
                  wx.showToast({ title: '生成成功', icon: 'success' })
                },
                fail: (err) => {
                  wx.hideLoading()
                  wx.showToast({ title: '生成失败', icon: 'error' })
                }
              })
            }
          }
          img.src = item.tempFilePath
        })
      })
    } catch (error) {
      wx.hideLoading()
      wx.showToast({ title: '生成失败', icon: 'error' })
    }
  },

  // 下载拼接图
  downloadCollage() {
    if (!this.data.generatedImage) return
    
    wx.saveImageToPhotosAlbum({
      filePath: this.data.generatedImage,
      success: () => {
        wx.showToast({ title: '已保存到相册', icon: 'success' })
      },
      fail: (err) => {
        if (err.errMsg.includes('auth deny')) {
          wx.showModal({
            title: '需要授权',
            content: '请允许访问相册以保存图片',
            success: (res) => {
              if (res.confirm) {
                wx.openSetting()
              }
            }
          })
        } else {
          wx.showToast({ title: '保存失败', icon: 'error' })
        }
      }
    })
  }
})
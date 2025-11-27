const utils = require('../../../utils/index.js')
const { toProxied } = utils

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
    canGenerate: false,
    dragGhostVisible: false,
    dragGhostSrc: '',
    dragGhostX: 0,
    dragGhostY: 0
  },

  onLoad() {
    // 设置页面标题
    wx.setNavigationBarTitle({
      title: '图片工具'
    })
    
    // 默认选择第一个模板
    this.selectTemplate({ currentTarget: { dataset: { template: this.data.templates[0] } } })
  },

  selectTemplate(e) {
    const template = e.currentTarget.dataset.template
    const imageList = template.cells.map((cell, index) => ({
      ...cell,
      index,
      image: '',
      tempFilePath: '',
      posX: 0,
      posY: 0,
      scale: 1
    }))
    
    this.setData({
      selectedTemplate: template,
      imageList,
      generatedImage: '',
      canGenerate: false
    })
  },

  selectImage(e) {
    const startIndex = e.currentTarget.dataset.index
    const empties = this.data.imageList
      .map((it, idx) => (!it.image ? idx : -1))
      .filter(idx => idx !== -1)
    const remaining = empties.length
    if (remaining === 0) {
      wx.showToast({ title: '没有空格子', icon: 'none' })
      return
    }
    wx.chooseImage({
      count: remaining,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const paths = res.tempFilePaths || []
        const imageList = [...this.data.imageList]
        // 以当前点击的格子为起点，按格子顺序填充空位
        const order = []
        const total = imageList.length
        for (let i = 0; i < total; i++) {
          const idx = (startIndex + i) % total
          if (!imageList[idx].image) order.push(idx)
        }
        const useCount = Math.min(paths.length, order.length)
        if (paths.length > order.length) {
          wx.showToast({ title: `超过剩余格子，只添加前${useCount}张`, icon: 'none' })
        }
        for (let i = 0; i < useCount; i++) {
          const idx = order[i]
          const p = paths[i]
          imageList[idx] = {
            ...imageList[idx],
            image: p,
            tempFilePath: p,
            posX: 0,
            posY: 0,
            scale: 1
          }
        }
        const canGenerate = imageList.every(item => item.image)
        this.setData({ imageList, canGenerate })
      }
    })
  },

  removeImage(e) {
    const index = e.currentTarget.dataset.index
    const imageList = [...this.data.imageList]
    imageList[index] = {
      ...imageList[index],
      image: '',
      tempFilePath: '',
      posX: 0,
      posY: 0,
      scale: 1
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
      tempFilePath: '',
      posX: 0,
      posY: 0,
      scale: 1
    }))
    
    this.setData({
      imageList,
      generatedImage: '',
      canGenerate: false
    })
  },

  batchUploadImages() {
    const emptyIndexes = this.data.imageList
      .map((it, idx) => (!it.image ? idx : -1))
      .filter(idx => idx !== -1)
    const remaining = emptyIndexes.length
    if (remaining === 0) {
      wx.showToast({ title: '没有空格子', icon: 'none' })
      return
    }
    wx.chooseImage({
      count: 9,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const paths = res.tempFilePaths || []
        const useCount = Math.min(paths.length, remaining)
        if (paths.length > remaining) {
          wx.showToast({ title: `超过剩余格子，只添加前${useCount}张`, icon: 'none' })
        }
        const imageList = [...this.data.imageList]
        for (let i = 0; i < useCount; i++) {
          const idx = emptyIndexes[i]
          const p = paths[i]
          imageList[idx] = {
            ...imageList[idx],
            image: p,
            tempFilePath: p,
            posX: 0,
            posY: 0,
            scale: 1
          }
        }
        const canGenerate = imageList.every(item => item.image)
        this.setData({ imageList, canGenerate })
      }
    })
  },

  // 拖拽功能
  onTouchStart(e) {
    const index = e.currentTarget.dataset.index
    this.setData({ dragIndex: index })
    
    // 记录触摸起始位置
    this.startX = e.touches[0].clientX
    this.startY = e.touches[0].clientY

    const item = this.data.imageList[index]
    if (!this.panZoomActive && item && item.image) {
      this.setData({
        dragGhostVisible: true,
        dragGhostSrc: item.image,
        dragGhostX: this.startX,
        dragGhostY: this.startY
      })
    }
  },

  onTouchMove(e) {
    if (this.data.dragGhostVisible) {
      const x = e.touches[0].clientX
      const y = e.touches[0].clientY
      this.setData({ dragGhostX: x, dragGhostY: y })
    }
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
      this.setData({ dragIndex: -1, dragGhostVisible: false })
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
        const a = imageList[dragIndex]
        const b = imageList[targetIndex]
        const ai = a.image
        const at = a.tempFilePath
        const apx = a.posX
        const apy = a.posY
        const as = a.scale
        imageList[dragIndex].image = b.image
        imageList[dragIndex].tempFilePath = b.tempFilePath
        imageList[dragIndex].posX = b.posX
        imageList[dragIndex].posY = b.posY
        imageList[dragIndex].scale = b.scale
        imageList[targetIndex].image = ai
        imageList[targetIndex].tempFilePath = at
        imageList[targetIndex].posX = apx
        imageList[targetIndex].posY = apy
        imageList[targetIndex].scale = as
        
        this.setData({ imageList })
      }
      
      this.setData({ dragIndex: -1, dragGhostVisible: false })
    }).exec()
  },

  onCellPan(e) {
    const index = e.currentTarget.dataset.index
    const { x, y } = e.detail
    const imageList = [...this.data.imageList]
    // 获取当前图片的缩放值
    const currentScale = imageList[index].scale || 1
    // 计算边界限制，防止图片完全拖出格子
    const maxOffset = 200 // 最大偏移量限制
    const clampedX = Math.max(-maxOffset, Math.min(maxOffset, x))
    const clampedY = Math.max(-maxOffset, Math.min(maxOffset, y))
    imageList[index].posX = clampedX
    imageList[index].posY = clampedY
    this.setData({ imageList })
  },

  onCellScale(e) {
    const index = e.currentTarget.dataset.index
    const { scale } = e.detail
    const imageList = [...this.data.imageList]
    // 确保缩放值在合理范围内
    const clampedScale = Math.max(0.5, Math.min(3, scale))
    imageList[index].scale = clampedScale
    this.setData({ imageList })
  },

  onMovableTouchStart(e) {
    this.panZoomActive = true
    if (e && e.touches && e.touches[0]) {
      this.startX = e.touches[0].clientX
      this.startY = e.touches[0].clientY
      this._lastTouchX = this.startX
      this._lastTouchY = this.startY
    }
  },

  onMovableTouchMove(e) {
    if (e && e.touches && e.touches[0]) {
      this._lastTouchX = e.touches[0].clientX
      this._lastTouchY = e.touches[0].clientY
      if (this.data.dragGhostVisible) {
        this.setData({ dragGhostX: this._lastTouchX, dragGhostY: this._lastTouchY })
      }
    }
  },

  onMovableTouchEnd() {
    this.panZoomActive = false
    if (this.data.dragGhostVisible) {
      const endX = this._lastTouchX || 0
      const endY = this._lastTouchY || 0
      const dragIndex = this.data.dragIndex
      if (dragIndex === -1) {
        this.setData({ dragGhostVisible: false })
        return
      }
      const query = wx.createSelectorQuery().in(this)
      query.selectAll('.image-cell').boundingClientRect((rects) => {
        let targetIndex = -1
        rects.forEach((rect, index) => {
          if (index !== dragIndex && endX >= rect.left && endX <= rect.right && endY >= rect.top && endY <= rect.bottom) {
            targetIndex = index
          }
        })
        if (targetIndex !== -1) {
          const imageList = [...this.data.imageList]
          const a = imageList[dragIndex]
          const b = imageList[targetIndex]
          const ai = a.image
          const at = a.tempFilePath
          const apx = a.posX
          const apy = a.posY
          const as = a.scale
          imageList[dragIndex].image = b.image
          imageList[dragIndex].tempFilePath = b.tempFilePath
          imageList[dragIndex].posX = b.posX
          imageList[dragIndex].posY = b.posY
          imageList[dragIndex].scale = b.scale
          imageList[targetIndex].image = ai
          imageList[targetIndex].tempFilePath = at
          imageList[targetIndex].posX = apx
          imageList[targetIndex].posY = apy
          imageList[targetIndex].scale = as
          this.setData({ imageList })
        }
        this.setData({ dragIndex: -1, dragGhostVisible: false })
      }).exec()
    }
  },

  onSwapLongPress(e) {
    const index = e.currentTarget.dataset.index
    const item = this.data.imageList[index]
    if (!item || !item.image) return
    const x = this._lastTouchX || 0
    const y = this._lastTouchY || 0
    this.setData({
      dragIndex: index,
      dragGhostVisible: true,
      dragGhostSrc: item.image,
      dragGhostX: x,
      dragGhostY: y
    })
  },

  noop() {},

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
      
      const query = wx.createSelectorQuery().in(this)
      query.selectAll('.image-cell').boundingClientRect()
      query.select('#collage-canvas').fields({ node: true, size: true })
      query.exec((ret) => {
        const rects = ret[0]
        const canvas = ret[1].node
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
            const rect = rects[index]
            const rx = rect && rect.width ? (width / rect.width) : 1
            const ry = rect && rect.height ? (height / rect.height) : 1
            // 计算偏移量和缩放 - 修正坐标系转换
            const scaleRatio = item.scale
            const offX = item.posX * rx
            const offY = item.posY * ry
            
            // 根据模板ID添加特殊形状效果
            if (selectedTemplate.id === 5) {
              // 梯形布局 - 添加圆角和特殊裁剪
              const padding = 10
              const drawWidth = width - padding * 2
              const drawHeight = height - padding * 2
              
              ctx.save()
              roundRect(ctx, x + padding, y + padding, drawWidth, drawHeight, 20)
              ctx.clip()
              
              // 计算缩放后的绘制尺寸
              const scaledWidth = drawWidth / scaleRatio
              const scaledHeight = drawHeight / scaleRatio
              
              ctx.save()
              ctx.translate(x + padding + offX, y + padding + offY)
              ctx.drawImage(img, -scaledWidth/2, -scaledHeight/2, scaledWidth, scaledHeight)
              ctx.restore()
              ctx.restore()
              
              // 添加边框
              ctx.strokeStyle = '#ffffff'
              ctx.lineWidth = 6
              roundRect(ctx, x + padding, y + padding, drawWidth, drawHeight, 20)
              ctx.stroke()
            } else {
              // 普通布局 - 添加圆角和边框
              const padding = 8
              const drawWidth = width - padding * 2
              const drawHeight = height - padding * 2
              
              ctx.save()
              roundRect(ctx, x + padding, y + padding, drawWidth, drawHeight, 12)
              ctx.clip()
              
              // 计算缩放后的绘制尺寸
              const scaledWidth = drawWidth / scaleRatio
              const scaledHeight = drawHeight / scaleRatio
              
              ctx.save()
              ctx.translate(x + padding + offX, y + padding + offY)
              ctx.drawImage(img, -scaledWidth/2, -scaledHeight/2, scaledWidth, scaledHeight)
              ctx.restore()
              ctx.restore()
              
              // 添加边框
              ctx.strokeStyle = '#ffffff'
              ctx.lineWidth = 4
              roundRect(ctx, x + padding, y + padding, drawWidth, drawHeight, 12)
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

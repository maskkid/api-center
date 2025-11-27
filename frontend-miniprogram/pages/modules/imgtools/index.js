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
    imageList[index].posX = x
    imageList[index].posY = y
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

  // 移除图片内的自定义拖动，改用 movable-view 的 x/y

  // 已移除 movable-view 的触摸钩子，避免与缩放手势冲突

  onSwapLongPress(e) {
    const index = e.currentTarget.dataset.index
    const item = this.data.imageList[index]
    if (!item || !item.image) return
    const query = wx.createSelectorQuery().in(this)
    query.selectAll('.image-cell').boundingClientRect((rects) => {
      const rect = rects && rects[index]
      const cx = rect ? (rect.left + rect.width / 2) : 0
      const cy = rect ? (rect.top + rect.height / 2) : 0
      this.setData({
        dragIndex: index,
        dragGhostVisible: true,
        dragGhostSrc: item.image,
        dragGhostX: cx,
        dragGhostY: cy
      })
    }).exec()
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
            const padding = selectedTemplate.id === 5 ? 10 : 8
            const areaW = width - padding * 2
            const areaH = height - padding * 2
            const rx = rect && rect.width ? (areaW / rect.width) : 1
            const ry = rect && rect.height ? (areaH / rect.height) : 1
            const offX = (item.posX || 0) * rx
            const offY = (item.posY || 0) * ry
            const scaleRatio = item.scale || 1
            
            // 按 aspectFill 计算绘制尺寸，保持不变形
            const imgW = img.width || areaW
            const imgH = img.height || areaH
            const baseScale = Math.max(areaW / imgW, areaH / imgH)
            const s = baseScale * scaleRatio
            const drawW = imgW * s
            const drawH = imgH * s
            // 初始居中，再叠加用户位移（从容器坐标到画布坐标）
            const baseX = x + padding + (areaW - drawW) / 2
            const baseY = y + padding + (areaH - drawH) / 2
            const drawX = baseX + offX
            const drawY = baseY + offY

            if (selectedTemplate.id === 5) {
              ctx.save()
              roundRect(ctx, x + padding, y + padding, areaW, areaH, 20)
              ctx.clip()
              ctx.drawImage(img, drawX, drawY, drawW, drawH)
              ctx.restore()
              ctx.strokeStyle = '#ffffff'
              ctx.lineWidth = 6
              roundRect(ctx, x + padding, y + padding, areaW, areaH, 20)
              ctx.stroke()
            } else {
              ctx.save()
              roundRect(ctx, x + padding, y + padding, areaW, areaH, 12)
              ctx.clip()
              ctx.drawImage(img, drawX, drawY, drawW, drawH)
              ctx.restore()
              ctx.strokeStyle = '#ffffff'
              ctx.lineWidth = 4
              roundRect(ctx, x + padding, y + padding, areaW, areaH, 12)
              ctx.stroke()
            }
            
            loadedCount++
            if (loadedCount === totalImages) {
              // 所有图片加载完成，导出最终图片
              wx.canvasToTempFilePath({
                canvas,
                success: (res) => {
                  this.setData({ generatedImage: res.tempFilePath })
                  // 生成后自动滚动到预览区域
                  wx.nextTick(() => {
                    wx.pageScrollTo({ selector: '#preview-anchor', duration: 300 })
                  })
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

const modules = require('../../config/modules')

Page({
  data: {
    modules: []
  },
  onLoad() {
    const m = modules.filter(x => x.enabled)
    this.setData({ modules: m })
  },
  onEnterModule(e) {
    const tag = e.currentTarget.dataset.tag
    const url = `/pages/modules/${tag}/index`
    wx.navigateTo({ url })
  }
})

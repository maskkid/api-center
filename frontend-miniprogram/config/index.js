// 全局配置文件
const config = {
  // API 域名配置
  appDomain: 'http://localhost:8001',
  
  // API 接口地址
  apiUrls: {
    // 分享相关
    shares: {
      list: '/api/shares/shares',
      detail: '/api/shares'
    },
    
    // 文案相关
    wenan: {
      categories: '/api/wenan/categories',
      list: '/api/wenan/list',
      detail: '/api/wenan/detail'
    },
    
    // 图片相关
    image: {
      upload: '/api/image/upload',
      process: '/api/image/process',
      proxy: '/api/proxy/image'
    },
    
    // 工具相关
    tools: {
      qrcode: '/api/tools/qrcode',
      shorturl: '/api/tools/shorturl'
    }
  },
  
  // 其他配置
  maxUploadSize: 10 * 1024 * 1024, // 10MB
  requestTimeout: 30000, // 30秒
  
  // 环境配置
  env: {
    development: {
      debug: true
    },
    production: {
      debug: false
    }
  }
}

module.exports = config
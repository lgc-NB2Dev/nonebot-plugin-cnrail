const { cpSync } = require('fs')
const path = require('path')

cpSync(
  path.join(__dirname, '../dist'),
  path.join(__dirname, '../../nonebot_plugin_cnrail/res/assets'),
  { recursive: true },
)

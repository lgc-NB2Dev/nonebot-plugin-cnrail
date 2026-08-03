<!-- markdownlint-disable MD031 MD033 MD036 MD041 -->

<div align="center">

<a href="https://github.com/lgc-NB2Dev/nonebot-plugin-cnrail">
  <img src="https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/cnrail/logo.svg" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/plugin.svg" alt="NoneBotPluginText">
</p>

# NoneBot-Plugin-CNRail

_✨ 12306 列车时刻表查询插件 ✨_

<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
<a href="https://pdm.fming.dev">
  <img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed">
</a>
<a href="https://wakatime.com/badge/user/de2f28c3-5c26-4f92-bfe0-7a392cbfed48/project/018c2a19-e33a-46ea-824a-230947989095">
  <img src="https://wakatime.com/badge/user/de2f28c3-5c26-4f92-bfe0-7a392cbfed48/project/018c2a19-e33a-46ea-824a-230947989095.svg" alt="wakatime">
</a>

<br />

<a href="https://pydantic.dev">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/pyd-v1-or-v2.json" alt="Pydantic Version 1 Or 2" >
</a>
<a href="./LICENSE">
  <img src="https://img.shields.io/github/license/lgc-NB2Dev/nonebot-plugin-cnrail.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-cnrail">
  <img src="https://img.shields.io/pypi/v/nonebot-plugin-cnrail.svg" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-cnrail">
  <img src="https://img.shields.io/pypi/dm/nonebot-plugin-cnrail" alt="pypi download">
</a>

<br />

<a href="https://registry.nonebot.dev/plugin/nonebot-plugin-cnrail:nonebot_plugin_cnrail">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgck.cc%2Fplugin%2Fnonebot-plugin-cnrail" alt="NoneBot Registry">
</a>
<a href="https://registry.nonebot.dev/plugin/nonebot-plugin-cnrail:nonebot_plugin_cnrail">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgck.cc%2Fplugin-adapters%2Fnonebot-plugin-cnrail" alt="Supported Adapters">
</a>

</div>

## 💿 安装

以下提到的方法 任选**其一** 即可

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot-plugin-cnrail
```

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install nonebot-plugin-cnrail
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add nonebot-plugin-cnrail
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add nonebot-plugin-cnrail
```

</details>
<details>
<summary>conda</summary>

```bash
conda install nonebot-plugin-cnrail
```

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分的 `plugins` 项里追加写入

```toml
[tool.nonebot]
plugins = [
    # ...
    "nonebot_plugin_cnrail"
]
```

</details>

## ⚙️ 配置

|         配置项         | 必填 |              默认值               |              说明              |
| :--------------------: | :--: | :-------------------------------: | :----------------------------: |
| `CNRAIL_ACG_IMAGE_URL` |  否  | `https://www.loliapi.com/acg/pe/` | 用于指令返回图片背景的图片 URL |

## 🎉 使用

使用指令 `train -h` 查看帮助

### 效果图

<details>

![效果图](https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/cnrail/t301.png)

</details>

## 📞 联系

QQ：3076823485  
Telegram：[@lgc2333](https://t.me/lgc2333)  
吹水群：[168603371](https://qm.qq.com/q/EikuZ5sP4G)  
邮箱：<lgc2333@126.com>

## 💡 鸣谢

### [海兰德小助手](https://qun.qq.com/qunpro/robot/qunshare?robot_uin=3889001607) & [Train-QQBot 插件](https://github.com/staytomorrow/FindTrain)

灵感来源

### [RailGo 数据服务](https://api.railgo.dev/)

数据来源

## 💰 赞助

**[赞助我](https://lgck.cc/donate)**

感谢大家的赞助！你们的赞助将是我继续创作的动力！

## 📝 更新日志

### 0.4.1

- 改用 [RailGo](https://www.railgo.dev/) 提供的数据

### 0.4.0

- drop htmlrender v0.8 适配，仅兼容 v0.7 与 v0.6
- 动态取色移至 Python 侧，删除 js 构建步骤

### 0.3.2

- bump htmlrender 到 v0.8

### 0.3.1

- 修复 MoeFactory API 调用错误

### 0.3.0

- 图片换用 Material Design 风格的莫奈（Monet）取色方案
- 修复 API 请求

### 0.2.3

- 更换上游 API 域名

### 0.2.2

- 修复列车行驶进度条计算问题（fix by [@This-is-XiaoDeng](https://github.com/This-is-XiaoDeng)）

### 0.2.1

- 适配 [MoeFactory API](https://train.moefactory.com)
- 新增配置项 `CNRAIL_ACG_IMAGE_URL`

### 0.2.0

- 适配 Pydantic V1 & V2
- 样式微调

### 0.1.7

- 添加车组号显示（无法显示未来日期的车组号信息）
- bug fix

### 0.1.6

- 添加担当路局显示 & 改次列车查询

### 0.1.5

- 修复 `-h` 参数无效的问题

### 0.1.4

- 现在缺少参数会提示了

### 0.1.3

- fix [#2](https://github.com/lgc-NB2Dev/nonebot-plugin-cnrail/issues/2)

### 0.1.2

- 支持选择日期查询（日期范围为前二日 ~ 后十四日）

### 0.1.1

- 修复查询到多个车次不会提示的问题

### 0.1.0

- 🎉 Create this project

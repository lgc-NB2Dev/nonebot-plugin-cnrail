<!-- markdownlint-disable MD031 MD033 MD036 MD041 -->

<div align="center">

<a href="https://github.com/lgc-NB2Dev/nonebot-plugin-cnrail">
  <img src="https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/cnrail/logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText">
</p>

# NoneBot-Plugin-CNRail

_✨ 12306 列车时刻表查询插件 ✨_

<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
<a href="https://pdm.fming.dev">
  <img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed">
</a>
<a href="https://wakatime.com/badge/user/de2f28c3-5c26-4f92-bfe0-7a392cbfed48/project/018c2a19-e33a-46ea-824a-230947989095">
  <img src="https://wakatime.com/badge/user/de2f28c3-5c26-4f92-bfe0-7a392cbfed48/project/018c2a19-e33a-46ea-824a-230947989095.svg" alt="wakatime">
</a>

<br />

<a href="./LICENSE">
  <img src="https://img.shields.io/github/license/lgc-NB2Dev/nonebot-plugin-cnrail.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-cnrail">
  <img src="https://img.shields.io/pypi/v/nonebot-plugin-cnrail.svg" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-cnrail">
  <img src="https://img.shields.io/pypi/dm/nonebot-plugin-cnrail" alt="pypi download">
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

暂无

## 🎉 使用

指令：`train 车次`

### 效果图

![效果图](https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/cnrail/c6837.jpg)

## 📞 联系

QQ：3076823485  
Telegram：[@lgc2333](https://t.me/lgc2333)  
吹水群：[1105946125](https://jq.qq.com/?_wv=1027&k=Z3n1MpEp)  
邮箱：<lgc2333@126.com>

## 💡 鸣谢

### [海兰德小助手](https://qun.qq.com/qunpro/robot/qunshare?robot_uin=3889001607) & [Train-QQbot 插件](https://github.com/staytomorrow/FindTrain)

灵感来源

### [12306](https://www.12306.cn)

数据来源

## 💰 赞助

感谢大家的赞助！你们的赞助将是我继续创作的动力！

- [爱发电](https://afdian.net/@lgc2333)
- <details>
    <summary>赞助二维码（点击展开）</summary>

  ![讨饭](https://raw.githubusercontent.com/lgc2333/ShigureBotMenu/master/src/imgs/sponsor.png)

  </details>

## 📝 更新日志

### 0.1.2

- 支持选择日期查询（日期范围为前二日 ~ 后十四日）

### 0.1.1

- 修复查询到多个车次不会提示的问题

### 0.1.0

- 🎉 Create this project

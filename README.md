# AstrBot 纯正油库里语音插件 (Yukkuri Voice)

这是一个用于 [AstrBot](https://github.com/AstrBot/AstrBot) 的插件，能将机器人发出的文字回复自动转换为最纯正经典的**油库里语音 (AquesTalk 灵梦原声)** 并发送给用户！

此插件完美解决了 64 位 Python 环境无法直接调用 32 位 `AqKanji2Koe.dll` 的痛点，通过自带的极轻量级 C# 桥接程序在后台生成音频，保留了油库里发音的所有**灵魂音调**与断句！

## 使用条件与安装方法

由于底层的 `AquesTalk.dll` 及字典库为 AQUEST 公司的商业专有软件，本仓库不提供（也不能提供）直接下载。请按照以下步骤自行配置：

1. **下载本仓库代码**，放置于 AstrBot 的 `data/plugins/astrbot_plugin_yukkuri_voice` 目录下。
2. 安装必要的翻译依赖包：
   ```bash
   pip install deep-translator
   ```
3. 请前往网络或 AQUEST 官方获取以下 32 位核心文件，并放到本插件的根目录下：
   - `AqKanji2Koe.dll` (32位版，负责日文到假名的音调转换)
   - `aq_dic` 文件夹 (必须包含在内，供转换器使用)
   - `AquesTalk.dll` (32位版，初代引擎 F1 音色) **【注意：请将此文件重命名为 `AquesTalk32.dll`】**
4. 运行安装脚本自动编译外挂程序：
   ```bash
   python setup.py
   ```
5. 重新启动 AstrBot 即可！

## 🤖 AI 自动化部署指南 (For Claude / AI Agents)
如果你是正在辅助部署此插件的 AI 助手（如 Claude Code），在新的设备上进行部署时，请严格按照以下流程操作：
1. 告知人类用户：由于版权原因，请他们手动将 32 位的 `AqKanji2Koe.dll`、`AquesTalk.dll` (需改名为 `AquesTalk32.dll`) 以及 `aq_dic` 文件夹移动到本插件目录下。
2. 确保依赖已经安装 (`pip install deep-translator`)。
3. 在插件目录下执行 `python setup.py`。该脚本会自动寻找正确的 Windows C# 编译器路径，并将其编译为 32位架构的 `YukkuriWrapper.exe`。
4. 如果脚本抛出缺少文件的错误，请直接读取输出，并精确提醒用户补充缺失的文件，然后再试。不要试图绕过该脚本使用手动命令编译。

## 工作原理
1. AstrBot 插件调用 `deep-translator` 将中文转为带有汉字的日语。
2. Python 使用 `subprocess` 隐蔽调用 32位的外挂程序 `YukkuriWrapper.exe`。
3. `YukkuriWrapper` 通过 `AqKanji2Koe.dll` 将日文转换为带有音调的假名记号。
4. 将假名记号送入 `AquesTalk32.dll`，完美生成包含升降调和断句的 `.wav` 录音文件。
5. 插件通过 AstrBot 发送语音。

## 鸣谢
- AQUEST Corp. 提供的 AquesTalk 引擎
- AstrBot 框架

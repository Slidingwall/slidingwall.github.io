---
layout: article
title: 【自用中译】开发 vLabeler 插件
date: 2026-08-17 06:43
category: 歌声合成
author: 
tags: [vlabeler, 歌声合成, 翻译]
summary: 
---
## 开发 vLabeler 插件
本文档介绍 vLabeler 的插件开发流程。若插件规范无法满足需求，欢迎提交问题或功能需求。

### 概述
vLabeler 当前支持两类插件：
- **宏插件（Macro plugins）**：在项目编辑阶段执行，多用于条目批量编辑。
- **模板插件（Template plugins）**：新建项目时执行，主要用于生成一批待编辑条目。

两类插件结构设计一致，但执行上下文不同，因此输入、输出存在差异。

本文涵盖以下内容：
- [插件文件结构](#插件文件结构)
- [插件定义](#插件定义)
    - [参数定义](#参数定义)
- [插件脚本编写指南](#插件脚本编写指南)
    - [编写模板生成脚本](#编写模板生成脚本)
    - [编写批量编辑（宏）脚本](#编写批量编辑宏脚本)
    - [其他说明](#其他说明)

### 插件文件结构
一个 vLabeler 插件是一个文件夹，内含：
1. `plugin.json`：用于定义插件行为
2. 至少一个 `*.js` 脚本文件
3. 脚本依赖的其他附加文件

### 插件定义
`plugin.json` 为 JSON 对象，包含以下字段：

| 键名                         | 类型                   | 默认值 | 支持插件类型 | 说明                                                                                                                                  |
|------------------------------|------------------------|--------|--------------|---------------------------------------------------------------------------------------------------------------------------------------|
| name                         | String                 | 必填   | 全部         | 值必须和插件文件夹名称一致                                                                                                            |
| version                      | Integer                | 1      | 全部         | 插件版本号                                                                                                                            |
| type                         | String                 | 必填   | 全部         | 取值为 `template` 或 `macro`                                                                                                          |
| displayedName                | String (Localized)     | `name` | 全部         | 插件展示名称                                                                                                                          |
| author                       | String                 | 必填   | 全部         | 插件作者                                                                                                                              |
| email                        | String                 | ""     | 全部         | 作者联系邮箱                                                                                                                          |
| description                  | String (Localized)     | ""     | 全部         | 插件简短描述                                                                                                                          |
| website                      | String                 | ""     | 全部         | 插件主页或源码仓库地址                                                                                                                 |
| supportedLabelFileExtension  | String                 | 必填   | 全部         | 支持的标签文件后缀（例如 UTAU oto 使用 `ini`）；使用 `*` 匹配所有后缀；多个后缀用 `|` 分隔                                             |
| outputRawEntry               | Boolean                | false  | Template     | 设为 `true` 时，输出原始条目文本，而非解析后的对象                                                                                    |
| scope                        | String                 | "Module" | 全部       | 插件作用域：`Module`（模块）或 `Project`（项目）                                                                                      |
| parameters                   | Parameters &#124; null | null   | 全部         | 详情参见【参数定义】小节                                                                                                              |
| scriptFiles                  | String[]               | 必填   | 全部         | 所有脚本文件名，脚本将按列表顺序依次执行                                                                                              |
| resourceFiles                | String[]               | []     | 全部         | 脚本使用的资源文件，文件内容会按列表顺序以字符串数组传入脚本                                                                            |
| inputFinderScriptFile        | String &#124; null     | null   | Template     | 用于动态查找输入文件的脚本文件名                                                                                                      |

#### 参数定义
`parameters` 对象内包含一个名为 `list` 的数组：
```json5
{
    // ...,
    "parameters": {
        "list": [
            // ...
        ]
    },
    // ...
}
```
`list` 内的每个对象对应配置弹窗里的一项参数，参数值会传入脚本。
完整参数定义请查阅 [Parameter](https://github.com/sdercolin/vlabeler/blob/main/docs/parameter.md)。

### 插件脚本编写指南
以下为插件脚本编写规范。
脚本运行环境与可用 API 的详细信息，请查阅 [Scripting in vLabeler](https://github.com/sdercolin/vlabeler/blob/main/docs/scripting.md)。

#### 编写模板生成脚本
`template` 类型插件运行于【新建项目】页面，用于生成条目列表供后续编辑。

##### 输入
脚本执行前，JS 环境中预先注入以下变量：

| 名称            | 类型                | 说明                                                                                             |
|-----------------|---------------------|--------------------------------------------------------------------------------------------------|
| inputs          | String[]            | 输入文件读取得到的文本，由【输入文件动态查找脚本】提供                                            |
| samples         | String[]            | 采样文件名列表                                                                                   |
| params          | Dictionary          | 包含 `plugin.json` 中定义的全部参数，通过参数名作为键读取值                                       |
| resources       | String[]            | 资源文件文本，顺序与 `plugin.json` 中定义一致                                                    |
| labeler         | LabelerConf         | JSON 对象，结构与 [LabelerConf](https://github.com/sdercolin/vlabeler/blob/main/src/jvmMain/kotlin/com/sdercolin/vlabeler/model/LabelerConf.kt) 一致 |
| labelerParams   | Dictionary          | 当前标签器的所有参数，通过参数名作为键读取值                                                     |
| debug           | Boolean             | 是否为调试模式（Gradle `run` 任务运行时）                                                         |
| pluginDirectory | [File](https://github.com/sdercolin/vlabeler/blob/main/docs/file-api.md) | 插件目录                                                                                         |

##### 输入文件动态查找
支持子项目的标签器，可通过脚本为每个子项目动态查找输入文件。
在 `plugin.json` 的 `inputFinderScriptFile` 指定该脚本。

该 JS 文件可获取：
- `root`（类型：`File`）：项目根目录
- `moduleName`（类型：`String`）：子项目名称
- 同时拥有 `debug`、`params`、`labeler`、`labelerParams`，与模板生成脚本一致

输出：
- `inputFilePaths`（类型：`String[]`）：目标输入文件路径列表
- 可选输出 `encoding`（类型：`String`）：指定输入文件编码；不设置则使用新建项目时选择的编码

`File` 类型规范参见 [文档](https://github.com/sdercolin/vlabeler/blob/main/docs/file-api.md)，可参考示例实现 [audacity2lab 插件](https://github.com/sdercolin/vlabeler/blob/main/resources/common/plugins/template/audacity2lab)。

##### 向用户请求输入文件
若输入文件和子项目无关（例如自定义词典），使用 `file` 或 `rawFile` 类型参数。
详见【参数定义】文档 [Defining a Parameter](https://github.com/sdercolin/vlabeler/blob/main/docs/parameter.md)。

##### 输出
通过名为 `output` 的数组向应用返回结果，支持两种形式：

###### 1. 直接返回解析后的条目对象
构造 `output` 数组，填入解析后的 [Entry](https://github.com/sdercolin/vlabeler/blob/main/src/jvmMain/resources/js/class_entry.js) 对象。示例：
```javascript
let output = [];
for (const line of lines) {
    // 解析行数据，得到 `name`、`sample`、`start`、`end` 等字段
    const entry = new Entry(sample, name, start, end, points, extras);
    output.push(entry);
}
```

###### 2. 返回原始条目字符串
当 `outputRawEntry` 设为 `true` 时，`output` 填入标签文件格式的原始文本行，后续由标签器内置解析器处理。

##### 注意事项
1. 若 `labeler.allowSameNameEntry` 为 `false`，同名条目仅保留第一条。如需全部保留，请在脚本中自行处理。
2. 未生成任何条目时会抛出错误，建议预留兜底条目。
3. 通过标签器解析原始标签文件创建项目时，会自动包含所有采样文件，即便原始标签中不存在，也会生成默认条目；但插件新建项目时，`output` 中未引用到的采样文件会被忽略，请确保需要的采样文件都存在对应条目。

##### 示例模板插件
可参考内置 `template` 插件学习：
- [ust2lab-ja-kana](https://github.com/sdercolin/vlabeler/blob/main/resources/common/plugins/template/ust2lab-ja-kana)：将 UST 文件转为 Sinsy lab 条目
- [cv-oto-gen](https://github.com/sdercolin/vlabeler/blob/main/resources/common/plugins/template/cv-oto-gen)：根据参数生成 CV 类型 oto 条目
- [regex-raw-gen](https://github.com/sdercolin/vlabeler/blob/main/resources/common/plugins/template/regex-raw-gen)：使用正则生成原始条目行，兼容所有标签器
- [audacity2lab](https://github.com/sdercolin/vlabeler/blob/main/resources/common/plugins/template/audacity2lab)：从 Audacity 标签文件生成 lab 条目，兼容支持子项目的 NNSVS 歌手标签器

#### 编写批量编辑（宏）脚本
vLabeler 中批量编辑脚本（类型：`macro`）用于项目操作，可作用于整个项目或单个子项目/模块。插件作用域决定生效范围：`Module` 作用域仅操作当前模块，`Project` 作用域覆盖整个项目。

##### 输入
脚本执行前，JS 环境预先注入以下变量：

| 变量名               | 类型                | 生效范围 | 说明                                                                                                 |
|----------------------|---------------------|----------|------------------------------------------------------------------------------------------------------|
| entries              | Entry[]             | Module   | 当前模块内所有 Entry 对象列表                                                                        |
| currentEntryIndex    | Entry[]             | Module   | 当前显示条目的索引                                                                                   |
| module               | Module              | Module   | 当前模块对象                                                                                         |
| modules              | Module[]            | Project  | 项目内全部 Module 对象                                                                               |
| currentModuleIndex   | Integer             | Project  | 当前显示模块的索引                                                                                   |
| params               | Dictionary          | 全部     | 包含 `plugin.json` 中定义的全部参数，通过参数名作为键读取值                                          |
| resources            | String[]            | 全部     | 资源文件文本，顺序与 `plugin.json` 中定义一致                                                         |
| labeler              | LabelerConf         | 全部     | JSON 对象，结构与 [LabelerConf](https://github.com/sdercolin/vlabeler/blob/main/src/jvmMain/kotlin/com/sdercolin/vlabeler/model/LabelerConf.kt) 一致 |
| labelerParams        | Dictionary          | 全部     | 当前标签器的所有参数，通过参数名作为键读取值                                                          |
| debug                | Boolean             | 全部     | 是否为调试模式（Gradle `run` 任务运行时）                                                              |
| pluginDirectory      | [File](https://github.com/sdercolin/vlabeler/blob/main/docs/file-api.md) | 全部     | 插件目录                                                                                              |
| projectRootDirectory | [File](https://github.com/sdercolin/vlabeler/blob/main/docs/file-api.md) | Project  | 项目根目录                                                                                            |

##### 使用条目选择器参数
该参数类型允许用户指定待操作条目子集，仅在 `Module` 作用域可用。示例代码：
```javascript
let selectedIndexes = params["selector"] // selector 为条目选择器参数的名称
for (let index of selectedIndexes) {
    let entry = entries[index]
    // 在此处理条目
}
```

##### 输出
直接修改 `entries` 或 `modules` 列表即可改动项目。注意：`Module` 作用域下虽能访问 `module` 对象，但对它的修改不会保存。
示例：给当前模块所有条目名称添加后缀
```javascript
let suffix = params["suffix"]
for (let entry of entries) {
    entry.name += suffix
}
```

##### 执行后展示报告
脚本执行完毕后可展示报告，参见文档 [Scripting in vLabeler](https://github.com/sdercolin/vlabeler/blob/main/docs/scripting.md#display-a-report-after-execution)。

##### 执行后请求音频播放
脚本执行完毕后可请求播放音频，参见文档 [Scripting in vLabeler](https://github.com/sdercolin/vlabeler/blob/main/docs/scripting.md#request-audio-playback-after-execution)。

##### 示例宏插件
可参考内置 `macro` 插件学习：
- [batch-edit-entry-name](https://github.com/sdercolin/vlabeler/blob/main/resources/common/plugins/macro/batch-edit-entry-name)：批量修改选中条目名称，演示条目选择器用法
- [batch-edit-oto-parameter](https://github.com/sdercolin/vlabeler/blob/main/resources/common/plugins/macro/batch-edit-oto-parameter)：编辑选中 UTAU oto 条目的参数，演示 `labeler` 变量使用
- [compare-oto-entries](https://github.com/sdercolin/vlabeler/blob/main/resources/common/plugins/macro/compare-oto-entries)：将外部 oto 文件与当前项目对比，使用 `report()`
- [execute-scripts](https://github.com/sdercolin/vlabeler/blob/main/resources/common/plugins/macro/execute-scripts)：运行自定义脚本编辑项目，可作为插件开发调试工具
- [resampler-test](https://github.com/sdercolin/vlabeler-resampler-test)：测试当前条目的重采样合成，演示 `requestAudioFilePlayback()`、`Env`、`File`、`CommandLine` API

### 其他说明
#### 本地化
上文 `String (Localized)` 类型说明参见 [Localized strings in vLabeler](https://github.com/sdercolin/vlabeler/blob/main/docs/localized-string.md)。

#### 错误处理
错误处理详情与方案参见文档 [Scripting in vLabeler](https://github.com/sdercolin/vlabeler/blob/main/docs/scripting.md#error-handling)。

#### 调试
可使用日志调试脚本：
标准输出（如 `console.log()`）写入 `.logs/info.log`，错误输出写入 `.logs/error.log`。

插件未出现在列表中，大概率加载阶段出错（如 `plugin.json` 解析失败），请查看错误日志。

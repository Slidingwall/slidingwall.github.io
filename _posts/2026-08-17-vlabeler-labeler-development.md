---
layout: posts
title: 【自用中译】开发自定义vlabeler标注器
date: 2026-08-17 06:44
category: 歌声合成
author: 
tags: [vlabeler, 歌声合成, 翻译]
summary: 
---

## 开发自定义标注器
**标注器（labeler）** 是一组配置文件与脚本，针对特定标注场景定义应用的多项行为。

本文档将引导你为 `vLabeler` 开发自定义标注器。

本文涵盖以下主题：
- [理解 vLabeler 项目](#理解-vlabeler-项目)
- [标注器结构](#标注器结构)
- [标注器定义](#标注器定义)
- [标注器内脚本编写](#标注器内脚本编写)
    - [构建项目](#构建项目)
    - [属性读取器](#属性读取器)
    - [属性写入器](#属性写入器)
    - [解析原始标签](#解析原始标签)
    - [写入原始标签](#写入原始标签)
    - [注入参数值](#注入参数值)
- [其他说明](#其他说明)

### 理解 vLabeler 项目
开始前，需要先了解 `vLabeler` 的项目结构基础知识。

#### 条目（Entry）
**条目（entry）** 是 `vLabeler` 内最小数据单元，代表一段带起始时刻和时长的音频数据。
大多数歌声合成软件都使用类似方式表达音频数据。例如在 UTAU 中，条目对应 `oto.ini` 里的一行；在 NNSVS 中，条目对应 `lab` 文件内的一行。

一个条目至少包含：起始时间、结束时间、标签名、音频文件引用。除此之外，还可附带其他时间点与附加信息。

在 `vLabeler` 中，我们把已有标签数据转换成条目，然后编辑条目——这是标注流程的核心。编辑完成后，再把条目转回原始标签格式。

#### 模块（Module）
**模块（module）** 是 `vLabeler` 的子项目（UI 中称为 `subproject`，代码/开发文档中称为 `module`）。

一个模块包含一组条目。很多声库的条目以层级形式组织，因此我们用模块来表达这种层级关系。

模块需要拥有名称、指向音频文件所在目录的引用、原始标签文件（如 `oto.ini` / `lab`）的引用，以此支持批量导入与导出。

#### 项目（Project）
**项目（project）** 是模块的集合，同时包含元信息，例如项目名、声库根目录等。

以 UTAU 歌手声库举例，声库结构可能如下：
```
your_singer
    ├── some wav files
    ├── oto.ini
    ├── C4
    │   ├── some wav files
    │   └── oto.ini
    ├── F4
    │   ├── some wav files
    │   └── oto.ini
    └── C5
        ├── some wav files
        └── oto.ini
```
这是典型的多音高 UTAU 声库结构：每个音高独立拥有 `oto.ini`，根目录下的 `oto.ini` 用于存放特殊采样。

`vLabeler` 内置的 **UTAU singer labeler** 正是为此场景设计。对于上面这个声库，它会生成一个包含4个模块的项目，每个模块对应一份 `oto.ini` 内的条目。
```
your_vlabeler_project
    ├── (Root) module
    │   ├── path: ""（和声库根目录一致）
    │   ├── entries: 根目录 oto.ini 内的条目
    │   └── sample files: 根目录下的wav文件
    ├── "C4" module
    │   ├── path: "C4"（C4文件夹）
    │   ├── entries: C4/oto.ini 内的条目
    │   └── sample files: C4文件夹下的wav文件
    ├── "F4" module
    ......
```

至此你已经理解基础项目结构。
本例中声库结构和项目结构高度接近，很容易从声库直接创建项目。但很多场景下二者差异很大：例如 NNSVS 的条目全部写在单个 `lab` 文件中，音频文件放在另一个目录。此时用户通常希望**每条音频+对应的lab单独作为一个子项目**。

显然这和 UTAU 示例的处理方式完全不同，我们需要自定义项目构建流程来适配不同场景——这正是标注器的核心功能之一。

除此之外，标注器还需要定义：
- 如何把原始标签解析为条目
- 如何把条目写回原始标签
- 条目在UI中的展示形式
- 条目哪些属性可以在界面查看、编辑
- 等等

下面章节介绍标注器结构，以及如何开发自定义标注器。

### 标注器结构
标注器是一个文件夹，结构如下：
```
your_labeler
    ├── labeler.json
    ├── parser.js
    ├── writer.js
    ├── projectConstructor.js
    ...（其他脚本与资源）
```
- 文件夹名（如 `your_labeler`）作为标注器唯一标识
- `labeler.json`：标注器主配置文件
- `*.js`：标注器用到的脚本
- 其他文件（如词典）可由脚本读取使用

<details>
<summary>旧式单文件标注器</summary>

1.0.0-beta20（标注器序列化版本号2）之前，标注器是后缀 `.labeler.json` 的单个文件，不支持外部资源文件，所有脚本直接内嵌在JSON内。该格式仍可兼容使用，但推荐使用新目录结构。
</details>

#### 脚本引用
配置中定义了 `EmbeddedScripts` 类型，用于在 `labeler.json` 内引用脚本。
当字段类型为 `EmbeddedScripts` 时，取值支持两种形式：
- 字符串：脚本路径，相对于 `labeler.json`
- 字符串数组：按行分割的JS代码片段

示例：`labeler.json` 引用同目录下 `parser.js`
```json5
{
    // ...,
    "parser": {
        "scope": "Entry",
        "scripts": "parser.js"
    },
    // ...
}
```

简短脚本也可以直接内嵌在 `labeler.json`：
```json5
{
    // ...,
    "parser": {
        "scope": "Entry",
        "scripts": [
            "// JavaScript code line 1",
            "// JavaScript code line 2"
        ]
    },
    // ...
}
```

### 标注器定义
下面详细说明 `labeler.json`。下表简述根对象各字段含义。
也可以查看带详细注释的Kotlin源码：[LabelerConf.kt](https://github.com/sdercolin/vlabeler/blob/main/src/jvmMain/kotlin/com/sdercolin/vlabeler/model/LabelerConf.kt)

| 键 | 类型 | 默认值 | 说明 |
|----|------|--------|------|
| name | String | （必填） | 值必须和标注器文件夹名一致 |
| version | Integer | 1 | 标注器版本号 |
| serialVersion | Integer | 0 | 标注器结构序列化版本 |
| singleFile | Boolean | true | 是否为旧式单文件标注器 |
| extension | String | （必填） | 原始标签文件后缀 |
| defaultInputFilePath | String &#124; null | null | 单模块项目默认原始标签文件路径 |
| displayedName | String (Localized) | `name` | UI展示名 |
| author | String | （必填） | 作者 |
| email | String | "" | 联系邮箱 |
| description | String (Localized) | "" | 简短描述 |
| website | String | "" | 主页或代码仓库地址 |
| categoryTag | String | "" | 分类标签；不填归入`Other` |
| displayOrder | Integer | 0 | 在下拉列表中的排序权重 |
| continuous | Boolean | false | 条目是否连续：即本条结束时间=下一条起始时间 |
| allowSameNameEntry | Boolean | false | 单个模块是否允许同名条目 |
| defaultEntryName | String &#124; null | null | 新建条目默认名称；null则使用不带后缀的采样文件名 |
| defaultValues | Float[] | （必填） | 时序参数默认值，格式 `[start, *fields, end]`，单位毫秒 |
| fields | Field[] | （必填） | 除标准`start`/`end`外的自定义时序点定义，详见[Field](#field) |
| extraFields | ExtraField[] | [] | 条目层级、非时序附加字段，详见[Extra Field](#extra-field) |
| moduleExtraFields | ExtraField[] | [] | 模块层级附加字段，详见[Extra Field](#extra-field) |
| lockedDrag | LockedDrag | {} | 锁定拖拽行为定义：拖动一个点时同步移动所有相关参数，详见[Locked Drag](#locked-drag) |
| overflowBeforeStart | PointOverflow | "Error" | 当存在早于`start`的时间点时的处理策略，详见[Point Overflow](#point-overflow) |
| overflowAfterEnd | PointOverflow | "Error" | 当存在晚于`end`的时间点时的处理策略，详见[Point Overflow](#point-overflow) |
| postEditNextTrigger | PostEditTrigger | {} | 编辑`start`/`end`后自动跳转下一条的触发规则，详见[Post-edit Actions](#post-edit-actions) |
| postEditDoneTrigger | PostEditTrigger | {} | 编辑`start`/`end`后标记完成的触发规则，详见[Post-edit Actions](#post-edit-actions) |
| decimalDigit | Integer &#124; null | 2 | 属性面板与导出时保留小数位数 |
| entrySimilarityWeights | EntrySimilarityWeights | 默认值 | 条目相似度计算权重，用于标签文件重载比对，详见[支持标签文件重载](#支持标签文件重载) |
| properties | Property[] | [] | 派生属性定义，详见[Property](#property) |
| parser | Parser | （必填） | 解析器定义，详见[Parser](#parser) |
| writer | Writer | （必填） | 写入器定义，详见[Writer](#writer) |
| parameters | ParameterHolder[] | [] | 用户可配置参数，详见[Parameters](#parameters) |
| projectConstructor | ProjectConstructor &#124; null | null | 项目构建器，详见[Project Constructor](#project-constructor) |
| quickProjectBuilders | QuickProjectBuilder[] | [] | 快速项目构建器，详见[Quick Project Builder](#quick-project-builder) |
| resourceFiles | String[] | [] | 脚本可读取的资源文件列表；内容按顺序以字符串传入脚本 |

下面解释部分关键字段。

#### 命名与版本管理
一份发布版标注器需要唯一 `name` 和 `version`。每次修改并对外发布时，**版本号必须递增**，同时避免和已有标注器重名。

`vLabeler` 依靠 name+version 自动处理标注器版本匹配：
如果项目使用的标注器版本高于本地已安装版本（或未安装），程序会从项目文件自动安装新版标注器；
如果本地安装版本更高，则优先使用本地版本。

> 注意：若标注器使用了外部资源文件，程序**不会自动更新**（资源不会打包进项目文件），需要用户手动升级到同版或更高版本。发布新版标注器时尽量保持向前兼容——vLabeler 不会阻止用户使用旧版标注器打开项目。

#### serialVersion（序列化版本）
序列化版本用于校验标注器结构和当前应用是否兼容。查阅[标注器结构更新记录](https://github.com/sdercolin/vlabeler/blob/main/docs/labeler-structure-updates.md)获取最新serialVersion并填写。

使用本文档开发新版目录式标注器时，务必设置 `singleFile: false`；该字段用来区分旧式单文件标注器。

#### extension（后缀名）
`extension` 是原始标签文件后缀，用于文件选择器过滤、插件兼容性判断。**不要加前置点**：例如写 `lab`，而非 `.lab`。

#### continuous（连续条目）
布尔标记，控制条目是否连续（本条end=下一条start）。
开启后默认启用多条联动编辑。
该字段会显著改变程序多处行为，请务必配置正确。

#### Field（时序点字段）
`fields` 定义除内置 `start`、`end` 之外的自定义时序点。
所有时序点（含内置start/end）都是毫秒浮点数，以采样文件起点为基准。
每个字段在编辑器渲染为一条可拖拽控制线。

自定义字段值存储在条目对象 [`entry`](https://github.com/sdercolin/vlabeler/blob/main/src/jvmMain/resources/js/class_entry.js) 的 `points` 数组内，**顺序必须和fields数组严格对应**。

`fields` 是 `Field` 对象数组，成员如下：

| 键 | 类型 | 默认值 | 说明 |
|----|------|--------|------|
| name | String | （必填） | 字段内部名 |
| label | String (Localized) | （必填） | 编辑器展示文本 |
| color | String | （必填） | 十六进制色号，波形图控制线颜色 |
| height | Float | （必填） | 控制线相对波形高度，取值0~1 |
| dragBase | Boolean | false | 是否作为锁定拖拽基准点，详见[Locked Drag](#locked-drag) |
| constraints | Constraint[] | [] | 字段约束，详见[Constraint](#constraint) |
| shortcutIndex | Integer &#124; null | null | 快捷键序号，取值1~8；0预留给start，详见[Shortcut](#shortcut) |
| replaceStart | Boolean | false | 是否替代原生start字段展示，详见[Replace Standard Fields](#replace-standard-fields) |
| replaceEnd | Boolean | false | 是否替代原生end字段展示，详见[Replace Standard Fields](#replace-standard-fields) |
| triggerPostEditNext | Boolean | false | 修改此字段是否触发「编辑后跳到下一条」，详见[Post-edit actions](#post-edit-actions) |
| triggerPostEditDone | Boolean | false | 修改此字段是否触发「编辑后标记完成」，详见[Post-edit actions](#post-edit-actions) |

##### Constraint（约束）
`constraints` 定义字段大小约束，数组内每条格式：
```json
{
    "min": 1,
    "max": 2
}
```
- `min`：本字段必须大于等于**索引为此值**的字段（可选）
- `max`：本字段必须小于等于**索引为此值**的字段（可选）

> start/end 标准字段不计入该索引体系；所有自定义时序点默认被约束在 start 和 end 之间。

约束只需要单向配置。举例：`fields = ["field1", "field2"]`，若要求 `field1 ≤ field2`，可以在field1写`max:1`，**或**在field2写`min:0`，二选一即可，无需双向配置。

约束仅**限制拖拽操作**；用户直接输入数值、插件脚本写入时不会校验。强约束需要在属性setter、writer脚本内手动判断并抛出错误。

##### Shortcut（快捷键）
vLabeler提供快捷键，一键把选中时序点设为当前播放光标位置：默认 `Q W E R ... I O P`。
`Q` 绑定原生`start`；后续快捷键按`shortcutIndex`顺序分配给自定义Field；`end`占用自定义字段之后的下一个快捷键。

建议按时序线上从左到右的顺序分配`shortcutIndex`。

##### Replace Standard Fields（替换标准起止点）
vLabeler默认所有自定义时序点必须落在 `start` ~ `end` 之间。但部分格式（如UTAU）允许overlap落在start左侧。

内置UTAU标注器的做法：新增`left`自定义字段，设置 `replaceStart: true`。
此时编辑器展示的是`left`而非原生`start`，overlap不再被限制在left右侧。
用户修改`left`时，底层原生`start`会自动更新为**所有相关时序点最小值**。

> 注意：该特性**仅非连续标注器（continuous=false）**可用。
> 使用替换字段后，parser、属性读写脚本都必须同时维护替换字段与原生start/end的值。

#### Extra Field（附加字段）
`extraFields` 用于条目层级、**非时序**附加字段；`moduleExtraFields` 用于模块层级附加字段。
和`fields`不同：附加字段不渲染时序控制线，值只能是字符串或`null`。

典型用途：存储和时间无关的元信息；一部分仅脚本内部读取，一部分可在弹窗展示/编辑。

- 条目附加字段：值存入entry对象 [`entry`](https://github.com/sdercolin/vlabeler/blob/main/src/jvmMain/resources/js/class_entry.js) 的 `extras` 数组，顺序严格匹配extraFields；null值也要保留占位，保证索引对齐。
- 模块附加字段：以字典形式存储，见[模块域解析](#模块域解析)、[模块域写入](#模块域写入)。

| 键 | 类型 | 默认值 | 说明 |
|----|------|--------|------|
| name | String | （必填） | 内部名称 |
| displayedName | String (Localized) | 同name | UI展示名 |
| defaultValue | String &#124; null | （必填） | 默认值 |
| isVisible | Boolean | false | 是否在配置界面可见 |
| isEditable | Boolean | false | 是否允许用户编辑 |
| isOptional | Boolean | false | 是否允许为null |

示例：UTAU标注器的`rawRight`就是典型附加字段。
UTAU的cutoff/right支持两种语义：负数=相对采样起点，非负=相对采样终点。
vLabeler内部统一转为相对采样起点的毫秒值，但导出时需要原始正负信息，因此把原始值存入`rawRight`附加字段。

#### Locked Drag（锁定拖拽/固定联动）
锁定拖拽：拖动一个基准点时，所有时序点保持相对间距同步平移（UTAU oto编辑常用）。
UI内称为`fixed-drag`。

按住Shift拖拽时，锁定逻辑反转：基准点不动，其余点联动平移。

用户首选项可以选择「以start为主基准」或「使用标注器配置」。标注器配置项`lockedDrag`格式：
```json
{
    "useStart": false,
    "useDragBase": false
}
```
- `useStart`：是否把原生start作为基准；若存在`replaceStart=true`字段，则使用该替代字段而非原生start
- `useDragBase`：是否把标记`dragBase=true`的字段作为基准

#### Point Overflow（越界策略）
`overflowBeforeStart` / `overflowAfterEnd` 分别控制：出现早于start、晚于end的时间点时如何处理。
可选值：
- `Error`：抛出错误，禁止
- `AdjustBorder`：自动拉伸start/end到极值点
- `AdjustPoint`：把越界点钳位到start/end

默认值：`Error`

#### Post-edit Actions（编辑后自动动作）
vLabeler内置两种编辑后自动动作：
- `Go to next entry after editing`：编辑完成后自动切下一条
- `Mark as done after editing`：编辑完成后标记本条完成

这里的「编辑」特指触发字段被修改。

根配置内 `postEditNextTrigger` / `postEditDoneTrigger` 控制标准起止点的触发，格式：
```json
{
    "useStart": false,
    "useEnd": false
}
```
- `useStart`：修改start触发；存在`replaceStart=true`时作用于替代字段
- `useEnd`：修改end触发；存在`replaceEnd=true`时作用于替代字段

自定义时序点则直接在Field内使用 `triggerPostEditNext` / `triggerPostEditDone` 开关。

#### 支持标签文件重载
用户重载标签文件时，程序比对新旧条目差异。为计算条目相似度，需要在`entrySimilarityWeights`配置各属性权重。

| 键 | 类型 | 默认值 | 说明 |
|----|------|--------|------|
| name | Float | 0.5 | 条目名称权重 |
| sample | Float | 0.3 | 采样文件名权重 |
| start | Float | 0.1 | start权重 |
| end | Float | 0.1 | end权重 |
| points | Float[] | [] | 自定义时序点权重，长度必须和points数组一致 |
| extras | Float[] | [] | 附加字段权重，长度必须和extras数组一致 |
| tag | Float | 0 | tag权重 |
| threshold | Float | 0.75 | 相似度阈值；高于此值判定为同一条目 |

可参考官方内置标注器的权重配置。

#### Property（派生属性）
`fields`时序点、`extraFields`附加字段可以存储原始数据，但UI展示/用户输入经常需要转换后的派生值。

例：UTAU的preutterance是**相对left**的值（用户习惯看到这个），但vLabeler内部统一存为**相对采样起点**的绝对毫秒。这时就需要Property做双向转换：展示时转为相对值、用户输入相对值时回写底层时序点。

根配置`properties`是Property数组，定义条目属性面板展示、脚本可读取的派生属性。

| 键 | 类型 | 默认值 | 说明 |
|----|------|--------|------|
| name | String | （必填） | 属性内部名 |
| displayedName | String (Localized) | （必填） | 属性面板展示名 |
| valueGetter | EmbeddedScripts | （必填） | 读取脚本 |
| valueSetter | EmbeddedScripts &#124; null | null | 写入脚本，可空（只读属性） |
| shortcutIndex | Integer &#124; null | null | 「设置属性」快捷键序号0~9；可写属性建议和数组下标保持一致 |

详见[属性读取器](#属性读取器)、[属性写入器](#属性写入器)。

#### Parser（解析器）
`parser`定义原始标签→条目的逻辑。

| 键 | 类型 | 默认值 | 说明 |
|----|------|--------|------|
| scope | "Entry" &#124; "Modules" | （必填） | 解析器域，决定脚本输入输出形式 |
| defaultEncoding | String | "UTF-8" | 读取标签文件默认编码 |
| extractionPattern | String (Regex) | "" | 正则提取行内变量，仅Entry域生效 |
| variableNames | String[] | [] | 提取变量名列表，仅Entry域生效；变量会传入脚本 |
| scripts | EmbeddedScripts | （必填） | 解析逻辑脚本 |

详见[解析原始标签](#解析原始标签)。

#### Writer（写入器）
`writer`定义条目→原始标签的逻辑。

| 键 | 类型 | 默认值 | 说明 |
|----|------|--------|------|
| scope | "Entry" &#124; "Modules" | "Entry" | 写入器域 |
| format | String &#124; null | null | 单行模板字符串，仅Entry域生效 |
| scripts | EmbeddedScripts &#124; null | null | 自定义写入脚本 |

`format`和`scripts`二选一；同时存在时优先使用scripts。

##### 使用 format 模板
`format`是字符串模板，`{变量名}`作为占位符。
示例：`{sample}:{name}={start},{middle},{end}` 渲染为 `a.wav:a:100,220.5,300`

模板可用变量：
- `sample`：采样文件名
- `name`：条目名
- `start`：条目start数值
- `end`：条目end数值
- 自定义Field名称：对应时序点数值
- Property名称：派生属性值
- ExtraField名称：附加字段字符串/null

> 若Field/ExtraField和Property重名，优先取Property。

##### 使用 scripts 脚本
详见[写入原始标签](#写入原始标签)。

#### Parameters（用户参数）
标注器配置本身不适合让用户直接修改JSON，但很多场景需要开放运行时选项。
例：UTAU标注器提供开关，控制是否允许负overlap。这类配置在项目创建弹窗展示，部分支持项目编辑时修改。

`parameters`数组存放`ParameterHolder`对象：

| 键 | 类型 | 默认值 | 说明 |
|----|------|--------|------|
| parameter | Parameter | （必填） | 参数本体定义，见[parameter.md] |
| injector | EmbeddedScripts &#124; null | null | 参数注入脚本，可动态修改labeler配置，详见[注入参数值](#注入参数值) |
| changeable | Boolean | false | 项目创建后是否允许修改该参数 |

#### Project Constructor（项目构建器）
对象仅包含`scripts`字段（EmbeddedScripts），示例：
```json
{
    "scripts": "projectConstructor.js"
}
```
详见[构建项目](#构建项目)。

#### Quick Project Builder（快速项目构建器）
数组存放快速构建器定义，用于首页「快速编辑」，直接从单个文件/文件夹一键生成项目。

| 键 | 类型 | 默认值 | 说明 |
|----|------|--------|------|
| name | String | （必填） | 构建器内部唯一名称 |
| displayedName | String (Localized) | name | UI展示名 |
| description | String (Localized) &#124; null | null | 提示文字 |
| extension | String | （必填） | 输入文件后缀；空字符串`""`代表接受文件夹 |
| scripts | EmbeddedScripts | （必填） | 构建逻辑脚本 |

详见[启用快速编辑](#启用快速编辑)。

### 标注器内脚本编写
前面介绍了标注器结构，本节讲解脚本写法。
开始前请先阅读[vLabeler脚本基础](scripting.md)，了解脚本运行环境。
也可以回看[脚本引用](#脚本引用)，确认配置内如何关联js文件。

#### 构建项目
前面讲过项目结构，这里说明如何用脚本从声库生成项目。

最简场景：单模块、所有条目写在根目录单一标签文件，无需自定义构建脚本。
只需在`labeler.json`设置`defaultInputFilePath`（相对根目录的标签文件路径），`projectConstructor`设为`null`。
```json5
{
    // ...,
    "defaultInputFilePath": "a raw label file",
    "projectConstructor": null,
    // ...
}
```
程序自动生成结构：
```
your_project
    └── (Root) module
        ├── path: ""（和声库根目录一致）
        ├── entries: 原始标签内所有条目
        └── sample files: 根目录wav
```

如果需要多模块、多文件夹独立标签文件，就需要在`projectConstructor`内指定脚本。

##### 输入变量
脚本执行前环境预定义变量：

| 名称 | 类型 | 说明 |
|------|------|------|
| root | [File](file-api.md) | 项目根目录 |
| params | Dictionary | 标注器所有参数，用name作为key读取 |
| resources | String[] | 资源文件文本，顺序和labeler.json内resourceFiles一致 |
| encoding | String | 用户选定的标签文件编码 |
| acceptedSampleExtensions | String[] | vLabeler支持的采样后缀，如`["wav", "mp3"]` |
| debug | Boolean | 是否调试模式（Gradle run任务） |

##### 输出约定
脚本执行完成后，全局变量`modules`必须正确赋值，程序据此创建项目。
`modules`是[ModuleDefinition](https://github.com/sdercolin/vlabeler/blob/main/src/jvmMain/resources/js/module_definition.js)对象数组。

ModuleDefinition字段：

| 名称 | 类型 | 说明 |
|------|------|------|
| name | String | 模块名 |
| sampleDirectoryPath | String | 采样目录绝对路径 |
| sampleFileNames | String[] | 模块使用的采样文件名列表 |
| inputFilePaths | String[] &#124; null | 读取用标签文件绝对路径 |
| labelFilePath | String &#124; null | 导出写入路径；null则每次导出需要用户手动选择 |

示例构建脚本：
```js
let modules = []

for (let folder of root.listChildDirectories()) {
    let sampleFiles = folder.listChildFiles().filter(file => acceptedSampleExtensions.includes(file.getExtension()))
    if (sampleFiles.length > 0) {
        let labelPath = folder.resolve("label.txt").getAbsolutePath()
        let def = new ModuleDefinition(
                folder.getName(),
                folder.getAbsolutePath(),
                sampleFiles.map(file => file.getName()),
                [labelPath],
                labelPath
        )
        modules.push(def)
    }
}

if (modules.length === 0) {
    error("No sample files found. Please check the labeler settings to ensure your sample folders are included.")
}
```
逻辑：遍历根目录所有子文件夹，包含有效采样文件就新建模块；模块采样目录=当前文件夹，采样文件=目录内所有支持格式音频，读取/导出文件固定为目录下`label.txt`。

最后建议判断modules是否为空，抛出友好错误提示。

#### 启用快速编辑
快速编辑功能：首页直接选择文件/文件夹，一键生成项目。
需要在`quickProjectBuilders`定义构建器。

> 注意：快速编辑依赖自动导出，因此要求标注器提供projectConstructor或defaultInputFilePath。

QuickProjectBuilder内`scripts`实现从输入生成项目。

##### 输入变量
- `input`：[File](https://github.com/sdercolin/vlabeler/blob/main/docs/file-api.md)对象，选中的文件或文件夹
- `savedParams`：标注器持久化参数，原始值；调试前建议打印确认类型

##### 输出约定
- `projectFile`：[File](https://github.com/sdercolin/vlabeler/blob/main/docs/file-api.md)，生成的`.lbp`项目文件
- `sampleDirectory`：[File](https://github.com/sdercolin/vlabeler/blob/main/docs/file-api.md)，采样根目录
- `cacheDirectory`：[File](https://github.com/sdercolin/vlabeler/blob/main/docs/file-api.md)，缓存目录；不设置则使用默认缓存
- `encoding`：标签文件编码，默认UTF-8
- `params`：项目使用的标注器参数；不设置则沿用`savedParams`

#### 属性读取器（Property Getter）
Property的`valueGetter`脚本用于获取派生属性值。

##### 输入变量
- `entry`：当前条目对象 [`entry`](https://github.com/sdercolin/vlabeler/blob/main/src/jvmMain/resources/js/class_entry.js)

##### 输出约定
**全局变量`value`** 赋值为计算得到的数值。
> 注意：`let value = ...` / `const value = ...` 不会生效！

示例：计算时长属性
```js
value = entry.end - entry.start
```

##### 错误处理
读取器不预期抛出异常；出错静默返回0并打印日志。

#### 属性写入器（Property Setter）
Property的`valueSetter`脚本，用户修改派生属性后回写底层条目。

##### 输入变量
- `entry`：当前条目对象
- `value`：用户输入的新数值

##### 输出约定
直接修改`entry`对象字段，无需额外返回变量。

示例：通过时长修改end
```js
entry.end = entry.start + value
```

##### 错误处理
写入器可使用全局`error()`API抛出校验错误。

#### 解析原始标签
项目创建流程简要回顾：
1. 执行项目构建器生成ModuleDefinition列表
2. 逐个模块生成条目
    1. Entry域+模板插件：插件执行生成条目；插件自带input finder则按其规则找文件，否则使用module定义内inputFiles；不存在的文件传入`null`
    2. Entry域、无模板插件：仅使用**第一个**inputFile；文件存在则执行Entry解析器；文件不存在则按labeler.json的defaultValues为每个采样生成默认条目
    3. Modules域解析器：按除name以外的字段分组ModuleDefinition，每组执行一次Modules域解析器（因此项目构建器要保证同组仅name不同）
3. 使用条目列表创建模块
4. 组装项目

> 小结：Entry域解析器**按模块执行一次**；Modules域解析器**按模块组执行一次**。

##### 公共输入（Entry / Modules 域共用）
| 名称 | 类型 | 说明 |
|------|------|------|
| inputFileNames | String[] | 输入标签文件名；Entry域仅1个元素 |
| sampleFileNames | String[] | 当前模块所有采样文件名 |
| params | Dictionary | 标注器参数 |
| resources | String[] | 资源文本数组 |
| encoding | String | 文件编码 |
| debug | Boolean | 调试标记 |

##### Entry域解析
Entry域配合`extractionPattern`正则、`variableNames`提取每行变量：程序逐行读入，正则捕获变量后再执行脚本。

除公共变量外，额外传入：
- `input`：当前行原始文本
- variableNames内定义的各个变量：正则捕获值

**全局变量`entry`** 需要赋值为新Entry对象。
> 注意：`let entry = ...` / `const entry = ...` 无效！

示例（两种写法二选一）
```js
// 假设正则已经提取 name, sample, start, end
entry = new Entry(sample, name, parseFloat(start), parseFloat(end), [], [])

// 直接手动分割解析
parts = input.split(",")
entry = new Entry(parts[0], parts[1], parseFloat(parts[2]), parseFloat(parts[3]), [], [])
```

##### Modules域解析
Modules域按模块组执行。先判断组内inputFiles是否存在；无文件则 fallback：按defaultValues为每个采样生成默认条目。

存在有效输入文件时，脚本环境额外传入：
- `moduleDefinitions`：本组ModuleDefinition数组
- `inputs`：输入文件内容数组；不存在的文件对应`null`

输出约定：
全局变量`modules` = `Entry[][]`，外层数组顺序和`moduleDefinitions`一一对应，内层是每个模块的条目列表。
可选：全局变量`moduleExtras` = `Dictionary[]`，顺序和modules对齐；字典key对应moduleExtraFields名称；值为字符串，null值不要写入key。

#### 写入原始标签
Writer支持Entry域、Modules域；简单场景用`format`模板，复杂逻辑用`scripts`。

##### 公共输入（Entry / Modules 域共用）
| 名称 | 类型 | 说明 |
|------|------|------|
| params | Dictionary | 标注器参数 |
| resources | String[] | 资源文本数组 |
| debug | Boolean | 调试标记 |

##### Entry域写入
Entry域每条目执行一次脚本。可用变量同[format模板](#使用-format-模板)。

**全局变量`output`** 赋值为单行输出文本。
> 注意：`let output = ...` / `const output = ...` 无效！

##### Modules域写入
整组模块一次性执行写入脚本。额外传入变量：
- `moduleNames`：本组模块名数组
- `modules`：`Entry[][]`，条目二维数组，顺序和moduleNames对齐
- `moduleExtras`：`Dictionary[]`，模块附加字段字典数组

**全局变量`output`** 赋值为完整标签文件文本，程序写入该模块组对应的`labelFilePath`。

#### 注入参数值（Injector）
标注器json本身一般不允许用户直接修改，但参数注入器可以**根据用户参数动态修改labeler配置对象**。
典型场景：UTAU的`useNegativeOvl`开关，动态修改ovl字段约束。

参数的`injector`脚本在项目创建时执行；若`changeable=true`，参数修改后也会重新执行。

脚本预定义变量：
- `labeler`：从labeler.json加载的配置对象（可直接修改）
- `value`：当前参数值，原生类型

示例（UTAU负重叠开关）
```js
labeler.fields[2].constraints[0].min = value ? null : 3
```
含义：开启负overlap时，该约束min设为null（允许越过left左侧）；关闭则min=3（索引3的字段，禁止左移越过left）。

> 注入器**禁止修改**以下字段：
> - `name`
> - `version`
> - `extension`
> - `displayedName`
> - `description`
> - `author`
> - `website`
> - `email`
> - `continuous`
> - `parameters`
> - `fields`数组长度
> - `defaultValues`数组长度
> - `extraFields`数组长度
> - `fields`内每个元素的`name`
> - `extraFields`内每个元素的`name`
> - `properties`内每个元素的`name`

### 其他说明
#### 示例项目
所有官方标注器开源，可直接参考：
- [UTAU singer labeler](https://github.com/sdercolin/vlabeler/blob/main/resources/common/labelers/utau-singer-labeler)：多音高UTAU声库，覆盖绝大多数脚本能力
- [NNSVS singer labeler](https://github.com/sdercolin/vlabeler/blob/main/resources/common/labelers/nnsvs-singer-labeler)：NNSVS声库，演示声库结构和vLabeler项目结构不同时的适配方案
- [Textgrid labeler](https://github.com/sdercolin/vlabeler-textgrid)：Praat TextGrid标注器，使用模块组+Modules域解析/写入

#### 本地化
查看[本地化字符串规范](https://github.com/sdercolin/vlabeler/blob/main/docs/localized-string.md)，了解文档中 `String (Localized)` 类型。

#### 错误处理
脚本异常策略详见[vLabeler脚本基础](https://github.com/sdercolin/vlabeler/blob/main/docs/scripting.md#error-handling)。

#### 调试
使用`console.log()`打印日志：标准输出写入`.logs/info.log`，错误输出写入`.logs/error.log`。
如果标注器不在下拉列表，大概率加载阶段JSON解析/脚本报错，优先查看错误日志。
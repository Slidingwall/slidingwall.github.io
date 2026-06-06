---
layout: post
title: 【中译】无人在意的RAXXER没用的“Vocaloid 数据库文档”附加内容
date: 2026-06-07 02:37
category: 歌声合成
author: RAXXER
tags: [Vocaloid, 歌声合成, 翻译]
summary: 
top: 2
---
> 译注：翻译与格式监修中，目前是由LLM辅助翻译的结果，图片待搬运。
> [原文地址](https://rentry.org/xei39tdi)

> [!NOTE]
> # 无人在意的RAXXER没用的“Vocaloid 数据库文档”附加内容

**你好！** 我是 **RAXXER**，也可以叫我 Razer 或 Crazer。这篇 rentry 会解释一些你可以为你的声库做的额外小技巧。

***

> [!CAUTION]
> 在继续之前，强烈建议先阅读 #tools-and-utilities 频道里的声库制作指南文档。
> [!CAUTION]
> 无论如何，这份文档不会消失，如果你真的需要帮助，请在 Discord 上联系我：razer_rhela

[TOC]
[TOC2]

# EpR 估计

> [!NOTE]
> EpR 可以代表 Excitation Plus Resonances（激励加共振）或 Estimated Pitch Range（估计音高范围），这里采用后者。如果你熟悉 RVC，可以把它类比为索引文件。虽然不是必须的，但它**确实**能显著提升声库的质量。

	我对 EpR 背后的实际科学原理不是很精通，但我可以告诉你如何设置它！

这里首先是一些没有和有 EpR 估计模板的声库之间的对比示例

![示例](https://files.catbox.moe/ea29iv.png)
![示例](https://files.catbox.moe/80ntsv.png)
![示例](https://files.catbox.moe/bh09x4.png)

[不带 EPR 的日语示例](https://soundcloud.com/user-276443030/kvox_jpn/s-7m1EETmnfqB?si=92b3ceaace8c4dcdbbbe0a0edc1d772f&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing)

[带 EPR 的日语示例](https://soundcloud.com/user-276443030/kvox_jpn_epr/s-gYWw8Gx9gwN?si=d82bd45b45fb4cddbc9999c8fcadf437&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing)

被说服了吗？在齿擦音上效果最明显，过渡也会得到更好的支持。

## 嗯，那现在怎么办？

你已经开始制作声库了吗？那好！现在你可以 %red% 把大部分工作扔掉！%%

哈哈，开玩笑的。如果你在最初的分段之外没做太多编辑，你可以直接用一个新的文件夹重新开始，保留你所有的原始分段文件。如果你已经做了很多... 我为你的损失感到遗憾。

> [!CAUTION]
> 如果你使用 **DaisyAnnotationTool** 来为你的声库做分段，你可以做其余的工作，但请改为在 VocaloidDBTool3 中制作 stationary。

### 词典

在重新制作你的声库文件夹之前，你必须确保你的词典末尾有 EpR 模板，它们看起来像这样：

```python
	template(phoneme="*"):
		000.000000, 0.000000
		0000.000000, 000.000000
		0000.000000, 00.000000
		0000.000000, 0.000000
```

把这一段加在它们上边：

```python
default_epr_resonances_templates:
	template(phoneme="ER"): # 激励共振
		200, 200 # 250, 350
		0, 0
		0, 0
		0, 0
```

用你的元音替换掉 * ... 它可能看起来像这样：

```python
default_epr_resonances_templates:
	template(phoneme="ER"): # 激励共振
		200, 200 # 250, 350
		0, 0
		0, 0
		0, 0
	template(phoneme="a"):
		700, 0
		1350, 100
		2750, 100
		3700, 0
	template(phoneme="e"):
		700, 0
		1350, 100
		2750, 100
		3700, 0
	template(phoneme="i"):
		700, 0
		1350, 100
		2750, 100
		3700, 0
```
等等等等...

> [!CAUTION]
> 确保它以 `default_epr_resonances_templates` 开头。
> 词典里的默认数字可以保留，如果你想添加自己的，请前往 [自定义填充 EpR 模板](https://rentry.org/xei39tdi/#custom-filled-epr-template)，这部分是独立于词典的。

### 设置 STA

为了充分发挥 EpR 的效果，我们必须把 stationary 录音拼接起来。这种行为在工具包的某个西班牙语文档中也出现过。

![PhD_jbonada_v1.1](https://files.catbox.moe/bhj9k2.png)

你基本上是把一个元音的所有 stationary 音高，从最低音高到最高音高拼接起来。*
	** 我不确定顺序是否重要，但这样是最整洁的。
![拼接前](https://files.catbox.moe/emkimz.png)
↓
![拼接后](https://files.catbox.moe/p13hg0.png)

这些是针对 [a] 的，你也应该对其余的 stationary 这样做。辅音的 EpR 估计是基于你的常规配置进行的（据我所知）。

### 分段

现在是最简单的部分。如果你以前制作过声库，并且想添加 EpR 模板，只需取用 `.wav` `.seg` 和 `.trans` 文件，确保不要包含旧的 stationary。为你的 stationary 制作空白的 `.trans` 文件。

创建一个新的歌手数据库文件夹，选择你添加了 EpR 模板的词典，然后打开 `自动分段`。

为了工作区更整洁，我把我的 STA wav 文件夹分开存放，你不必这样做。

点击 `编辑转录`，为你拼接在一起的音高数量添加正确数量的音素，在我的例子中是 5 个。

![为 stationary 添加转录](https://files.catbox.moe/6cxn8a.gif)

然后像往常一样配置你的 stationary！

![移动标签](https://files.catbox.moe/a33v65.gif)

像往常一样将 stationary 添加到数据库中，这可能会比平时花费稍长的时间。

> [!NOTE]
> （可选）如果你想自己指定 EpR 指南，请前往 [自定义填充 EpR 模板](https://rentry.org/xei39tdi/#custom-filled-epr-template)。如果你决定这样做，可以跳过本节的其余部分。

然后点击 `优化 EpR 指南` ............ 魔法在这里发生！！！！！！（并不是）

![移动标签](https://files.catbox.moe/dm7ll8.gif)

它什么都没做...？你觉得这是好事吗？

如果你配置了不止一个 stationary，它会弹出一个进度条。

![进度条](https://files.catbox.moe/8rffm2.gif)

### 确认它是否真的生成了东西

如果你进入你创建声库文件夹的位置，你可以看到一个名为 `epr_templates.txt` 的文件，它应该有填写好的条目。

![epr_templates.txt](https://files.catbox.moe/gcjp4n.png)

就是这样，哈哈。把声库的其余部分加回去，对辅音进行分段，然后你就得到了属于你自己的 EpR，为你那臭烘烘的 Vocaloid 声库，每个人都会因为你是个好孩子而拍拍你的背！

## 错误

### 无法估计第一个和/或最后一个帧的 EpR

![错误](https://files.catbox.moe/q0c1jc.png)

你的位置靠得太近了 *或者* 你有一个 *制表符*（通常由按 TAB 键生成）刚好在 EpR 字符串之前/之上。

### 以下 stationary 的手动估计 EpR 可能在不同音高上不一致

![错误](https://files.catbox.moe/0jwedc.png)

它无法读取音高线，这个问题不算太严重。

# 自定义填充 EpR 模板

使用 [PRAAT](https://www.fon.hum.uva.nl/praat/) 自定义默认数字。

你可能已经注意到 stationary 步骤旁边的这段文字   ![错误](https://files.catbox.moe/587ido.png)

我们将在这一步中完成这个操作。建议为此安装 PRAAT，除非你有其他可以提供共振峰和带宽的程序。关闭 `自动分段`。

应该有一个叫做 `epr_templates.txt` 的文件，里面包含词典附带的默认数字。

打开它，把它放在一边。接下来打开 Praat。

通过 `打开` > `从文件读取` 或 `打开` > `打开长声音文件` 打开你之前拼接好的 stationary，这会打开一个窗口显示你的 wav 文件。

选择你想查看的那个，然后选择 `查看和编辑`。这会打开一个新窗口显示你的 wav，确保你放大到足以看到窗口底部。

现在，选择任意一个 stationary，根据我的测试，选择哪个音高并不重要，但在我自己的工作流程中，我会选取在 VB 中最自然的那个音高。

拖动选区覆盖整个 stationary，确保不要取消选择。

然后查看 `共振峰` 选项卡，按下 `显示共振峰`。再往下一点，你应该会注意到你可以查看 4 个点的共振峰以及它们的带宽，我们需要这些。

按下快捷键 F1，或者手动点击，会弹出一个新窗口显示数字。我们的注意力将回到 `epr_templates.txt` 文件，一个条目应该看起来像这样：

```
	template(phoneme="a"):
		790.000000, 10.000000
		1300.000000, 70.000000
		2800.000000, 50.000000
		3760.000000, 0.000000
```

逗号之前是共振峰（Formants），逗号之后是带宽（Bands）。有了这些信息，我们就可以填写 `epr_templates.txt` 文件。例如，第一个共振峰是 `1095.4409956453749`，给定的带宽是 `105.60436272944551`。你基本上只需要小数点前的数字，像这样填写模板：

```
	template(phoneme="a"):
		1095.000000, 105.000000
		1300.000000, 70.000000
		2800.000000, 50.000000
		3760.000000, 0.000000
```

对其余的共振峰和带宽也这样做，最终结果类似这样：

```
	template(phoneme="a"):
		1095.000000, 105.000000
		1509.000000, 63.000000
		2711.000000, 71.000000
		3634.000000, 102.000000
```

对其余的 stationary 重复这些步骤。完成之后，回到自动分段，然后在步骤 3 中按下 `优化 EpR 指南`。

你原来的 `epr_templates.txt` 现在应该被替换了，并基于你初始的数字进行了优化。之后继续常规的开发。

### 与不进行自定义相比，这真的有区别吗？

**稍微有点**，这实际上是需要更多测试的东西。

# LSF（线谱频率）

按下 Compute LSF（重建 EpR）会破坏多个参数设置。

按下 Compute LSF（保留 EpR）会破坏 v4dev，并且在编译时崩溃。

# 稳定标记（循环区域）

你实际上可以改变它在哪个点循环 CV，从而决定在样本最稳定的部分设置 stationary。CV 实际上并不会被 stationary 延长，但它们有助于对样本进行共振峰处理（如果我记得没错的话）。待完善。

# phn_seg.py

Phn_seg.py 被开发套件用来估计音素的位置。它是点击 `Segment phonemes` 时调用的原始文件。它基于音量来估计音素位置。如果你使用 **DaisyAnnotationTool**，则实际上不需要这个文件。

你可以在服务器上的某个地方搜索到这个文件。

如果你按照原始文档操作，你应该已经安装了 Python 3.10。

在你存放 VocaloidDBTool3.exe 的位置，新建一个名为 `scripts` 的文件夹。

![与你的 exe 相同的位置](https://files.catbox.moe/7yu1jh.png)

把你的 phn_seg.py 放进去。

打开分段时，确保选择存放 VocaloidDBTool3.exe 的文件夹，然后点击“分段音素”后它就会自动运行。

> [!CAUTION]
> 由于基于 Python，它**不喜欢**声库文件夹路径中有空格，请记住这一点。

![打开自动分段](https://files.catbox.moe/dlnh7v.gif)

请注意，它是根据你样本的音量来放置音素边界的... 不会是世界上最精确的东西，但相当 neat。

![显示结果](https://files.catbox.moe/5q3o3h.gif)

开发套件提到能够进行 metro-segment 音素，理论上需要另一个 .py 文件，但我们没有那个文件 :[

**请使用 KVOX，这是宣传**
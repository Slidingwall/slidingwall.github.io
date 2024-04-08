---
layout: post
title: 【中译】Vocaloid声库制作教程
date: 2024-04-07 04:05
category: 歌声合成
author: Zelliel & EnlilGen
tags: [Vocaloid, 歌声合成, 翻译]
summary: 
excerpt_image: /assets/images/vocaloid-svs-tutorial/18.png
---

> 译注：本文为该文档中文精翻，仅供学习参考使用，内容及立场不代表译者观点。  
> 文章内容相关问题请咨询原作者。复现文章内容造成一切后果，均与译者无关。  
> [原文地址](https://docs.google.com/document/u/0/d/1vTHLPRp65ejcq5-bA7n_FP6CCgzG8_w0hgoYTCsAxq8)

## 前言

**警告：有史以来最大的工作量**  
如果您**没有**耐心制作Vocaloid声库，请不要尝试！  
如果您的硬盘没有至少1\~20GB的空间，**也不要尝试！**（仅一个音阶的采样就可能占用1\~5GB的空间）  
**这将需要大量的时间、大量的精力、大量的空间。**

## Vocaloid声库制作教程

作者：[Zelliel](https://twitter.com/Zelliell) 与 [EnlilGen](https://twitter.com/EnlilGen)  

如果您有任何值得添加进教程中的信息，请联系原作者。  
本文将带您了解创建Vocaloid声库的过程。

## 准备数据

### 术语解释

- **Stationary**(持续)：用于合成长音符时循环的部分。  
  *译注：多数为韵腹或能独立持续发音的辅音，类似UTAU中的长采样。*  
- **Articulation**(衔接)：元音与辅音之间的衔接部分。  
  *译注：类似UTAU中的CV及VC。*  
- **Concatenated**(组合)：组合在一起的元音与辅音。  
- **Trans file**(转录文件)：记录Vocaloid从采样中提取的音素。  
- **DBTool**(制作工具)：类似Deepvocal tookit的Vocaloid开发工具。

### 步骤0：准备工作（可选）

首先像拼接合成软件一样，提前新建若干文件夹并选择适合您的录制音域。  

![](/assets/images/vocaloid-svs-tutorial/1.png)

每个文件夹内还应该包含`Stationary`和`Articulation`两个子文件夹。  
`Stationary`中需要录制长采样，包括元音（如`a`）和部分辅音（如`s`）。注意，短发音（如爆破音`b`、`p`、`t`）不在此列。  
`Articulation`可采用VCV或CVVC的格式，后文详细介绍。  
***注意：虽然Stationary不会作为连接使用，但它最好与Articulation选择同一批采样，以保持声库一致性。**  

![](/assets/images/vocaloid-svs-tutorial/2.png)
  
**现在让我们了解Vocaloid中CVVC与VCV的区别。**

### 步骤1：采样

这一步的选择会大大影响后续进展，最好提前规划好。我们先从两者中较简单的开始。  
  
**CVVC/Articulation 实际上就是CV VC。** 在Vocaloid中，只要拥有`Sil C/V (- C/V)` `C V` `V C` `C C`以及`C/V Sil (C/V -)`这些组合，就可以获得一个可用的声库（其中`C C`不是必须的）。  
**每个发音要想正常播放，都必须有`Sil C/V`和`C/V Sil`，即音素的开头和结尾。**这个方案虽然看上去简单，做起来却非常繁琐。对于测试声库而言是一个好的选择。这个规则同样适用于英语。  
*译注：可参考基于双音素连接的Arpasing，方便理解其原理。对于中文Vocaloid而言，其采用的是CVVC的方案。但由于Vocaloid对每个复韵母都赋予单独的发音记号，致使其`V V`部分冗余过多，易被误认为采用了VCV方案。包括CVVChinese、Synthesizer V在内的其他方案都对此进行了简化，以减少声库大小。*

**VCV/Triphone 也是制作声库的一个重要部分。** 但工作量会大大增加。您录制的组合可以是`Sil C V` `Sil C C` `Sil V C` `Sil V V` `V C V` `C V C` `C V Sil` `C C Sil` `V V Sil` `V C Sil`等等，任何三音素组合都是是可行的。您需要像CVVC一样遍历每一种可能的组合。VCV可以与CVVC混合使用，以提升声库性能。  
对于英语则有所不同。例如，`star`是一个`C C V`，而`string`中的`str`则是一个`C C C`。`V V V`也可行，但它会与`Stationary`产生冲突，使合成效果不完美。  
*译注：可参考VCCV English理解此部分。英语辅音连缀较为发达，元音前可出现2~3个辅音，元音后最多可出现4个。值得注意的是，VCCV English将辅音连缀视为整体，而Vocaloid限于引擎机能，单条采样只能处理最多3个音素。*

DBTool可以读取`.mp3` `.wav` `.ogg`格式的音频，只要转录(trans)文件与其同名即可。您也可以像制作UTAU声库时一样，对采样进行处理。**这一步是可选的：**将所有采样导入Audacity，去除底噪、应用`Filter Curve EQ(滤波曲线均衡器)> Preset(预设)> Low rolloff for Speech(语音低滚降)`，并进行标准化，以优化采样质量。处理好后的采样应另存在新文件夹中，避免覆盖源文件。使用批量导出功能按轨道名称一次性导出所有采样。若有去除齿音工具，效果更佳。（您也可以进行修音，IA声库就是这么做的）完成预处理后，即可开始转录工作了。  

### 步骤2：转录

转录是DBTool识别采样中音素的方式。转录时，先用对应语言的发音记号记录音频内容，再在下方用`[`**方括号**`]`括出您想提取的音频片段。`Stationary`的括号中仅包含一个音素，但您可以添加多个括号，在一条采样内提取出多个音素。您最好提前规划各个音素提取的位置，除非它们来自是不同的音高，否则应避免音素重复。  

值得注意的是，**程序只关注`[`方括号`]`出现的首个音素**。例如：`Baby -> Sil b eI b eI -> [Sil b eI] [eI b] [b eI]`问题出在：**程序会认为**`Sil b eI`**和**`b eI`**是相同的，导致后者无效。**因此为了区分需要这么修改：`Baby -> bh eI b eI -> [bh eI] [eI b] [b eI]`以区分这两个部分。对三音素而言同理：`ba ba bu ba -> b a b a b M b a -> [a b a] [M b a]`通过开头的音素以区分不同的采样。  

您可以直接将`.txt`重命名为`.trans`来创建转录文件，确保它与采样名称相同。您也可以用Canned-Bread的Swiss army knife工具，根据采样名称自动生成`.trans`文件以便您编辑。如果您只做CVVC的话，可以使用auto_transcript功能。但以笔者的个人经验而言，该功能并不完美，需要进行清理与校对。生成后可在DBTool中编辑。为提高工作效率，建议您先在文本编辑器中处理，以避免后续的麻烦。

**以下是一些转录文本的例子：**

- Stationary：  

![](/assets/images/vocaloid-svs-tutorial/3.png)

- Articulation：

![](/assets/images/vocaloid-svs-tutorial/4.png)
![](/assets/images/vocaloid-svs-tutorial/5.png)  
![](/assets/images/vocaloid-svs-tutorial/6.png)
![](/assets/images/vocaloid-svs-tutorial/7.png)  

#### 简化转录的经验法则

1. 无需转录整个采样，或一直添加`Sil`。**比如`ka n ka`，可以只记录`N k`、只括出`[N k]`，然后继续其他操作。**任何情况下都可以选择性转录关键部分。可以利用复制粘贴以简化工作流程。
2. **日语专用** N的对应表

    - mm / **m** = b / p / m
    - mmy / **m'** = b' /p' / m'
    - nng / **N** = k / g
    - nngy / **N'** = k' / g'
    - nn / **N\\** = h / C / p\ / p\' / w / v / v' / j
    - nny / **J** = J
    - **n** = 其他发音

3. 如前所述，有些辅音需要`Stationary`。所有语言的鼻音和流音都是如此。**如果没有`C C`衔接的话，两个辅音之间的过渡会不顺畅。**  
*译注：由于Vocaloid将所有中文前后鼻音归纳为复韵母，因此中文是唯一一个没有`C C`衔接，也没有辅音持续的语言。*
4. 不要在音阶上过于苛刻，这可能会损坏Vocaloid。**音阶一般在3-7个即可。** XSY完全可用，因此不用担心！**不同语言或不同格式的声库无法交叉合成，仅含有CVVC的声库与XSY不兼容。**
5. `Sil C`**应是无声的，而**`Sil C V`**应是有声的**。处理不当可能会有奇怪的拉长音。流音、鼻音、呼吸音也是如此。**程序不接受**`Sil Sil`**的标记。**
6. **切记，只有Vocaloid支持的语言才有能正常运行的字典。**所以要么在支持语言的范围内操作，要么研究语音学。
7. 需要注意的是，即使`bi bi`被读作`b' i b' i`，您仍需录制`i b`发音。这对所有音素都适用，例如，需要`i h`来衔接`i ha`。

### 步骤3：新建声库

一切准备就绪后，以您的歌手名字或代号创建一个空的`.txt`文件。您还需要准备DBTool的字典，它们和DBTool在同一个文件夹内。当字典是文本格式时可对其编辑。您也可以使用DBTool的字典功能来添加内容（后文详解）。

打开DBTool后，**选择**`File(文件) -> New Singer Database(新建歌手数据库)`，加载您选择的字典与您歌手名字命名的空`.txt`。点击`ViewDB -> stationary`检查是否成功。您应该会看到所有的音素和它们下边的`X`，因为还没有加载采样。  

![](/assets/images/vocaloid-svs-tutorial/8.png)

添加采样后，`X`会变成数字，适用于所有部分。采样频率会显示为**一个红点**，**从左到右代表频率从低到高**。点击红点以查看采样并编辑标记，与分割的方式相同。确保通过`nameDB > update markers`来保存更改（如果您得到的声音很怪，多半是标记放错了）。**检查时，请确保每次更换采样都重新点击红点，否则会显示错误的采样。**  

创建歌手后，将会自动生成与`.txt`同名的一个文件夹、**一个**`.dat`**文件和一个**`.tree`**文件。**不要删除这些重要文件。关闭DBTool后，再次打开时可从`singer.inf`所在的文件夹重新加载歌手。

![](/assets/images/vocaloid-svs-tutorial/9.png)
![](/assets/images/vocaloid-svs-tutorial/10.png)

接下来进行标注。

## 创建声音

### 步骤0：自动分割

点击`File(文件)->Automatic Segmentation(自动分割)`开始分割。采样与转录文件必须在同一文件夹中，DBTool支持识别子文件夹，因此您可以放心加载整个声库。将DBTool设置为分割工具。如果您的操作正确，您将会看到这个界面：

![](/assets/images/vocaloid-svs-tutorial/11.png)

报错是正常的。全选并分割音素，将生成基础标记。之后在查看模式下打开它们并进行修正。注意：编辑转录文件后需要重新进行分割。**误操作会使您重复这些步骤，并强制删除所有刚刚添加的采样。**  

如果在`Stationary`或`Articulation`下显示`Error/0`，则表示转录有误，纠正音素后重做分割即可。双击转录、`Stationary`和`Articulation`将会打开它们各自的查看器。双击文件名将会打开外部音频查看器。右键菜单中也有相同的选项，您可以在`文件`中设置外部音频编辑器，如`Audacity`等。

### 步骤1：编辑分段

您可以通过`左Ctrl`或者`左Shift+单击`选中多个条目编辑。最多同时支持编辑6条。  

点击`View/Edit Segmentation(查看/编辑分段)`  
示例：`ja_ja_ji_ja_ju_ja_je`  

![](/assets/images/vocaloid-svs-tutorial/12.png)

单击**顶部灰栏**以选择音素，同时允许您**选中红条**以编辑音素。  

![](/assets/images/vocaloid-svs-tutorial/13.gif)

接着，您便能按照您的意愿**移动红线**了。  

![](/assets/images/vocaloid-svs-tutorial/14.gif)

**正确的红线位置会减少您稍后在发音菜单中的编辑次数。**  
`Sil C V`：将标记放在音素开始的位置。
`C V`：将辅音放在前一个音符的末尾，将元音放在辅音之后。
`Sil C`：标记内什么也没有。
`Sil V`：标记内可以有声音（不包括鼻音或流音）。

![](/assets/images/vocaloid-svs-tutorial/15.png)

`空格`：播放采样  
`Shift+拖动`：选中部分采样并播放  
`Shift+单击`：取消选中采样  
`Shift+单击标记`:选择标记中的采样  
上下左右拖动测滚动条旁绿色箭头：缩放波形（所有菜单均有这些滚动条）  
关闭界面后采样旁出现YES：标记已被编辑  
编辑标记时底部看不到音素，则音素不在字典中。  
（以上适用于自动分割内外的所有菜单）

### 步骤2：持续采样

选择想分割的采样，点击`View/Edit Segmentation(查看/编辑分段)`。  
这可能需要几秒的时间加载。完成后，选中想要编辑的分段，再次点击`View/Edit Segmentation(查看/编辑分段)`。  

选择或长或短的一段C/V采样，**确保标记不在采样头尾处**，而是采样中间或波形稳定清晰处。

![](/assets/images/vocaloid-svs-tutorial/16.png)

将其添加进声库。

![](/assets/images/vocaloid-svs-tutorial/17.gif)

* 遗憾的是这对于一个测试声库来说远远不够。测试采样还需要添加相同音素的`Sil C/V`或`C/V Sil`。

### 步骤3：衔接采样

选择想要分割的采样并点击`Segment Articulations(分割衔接)`。  
这可能需要几秒的时间加载。完成后，选中想要编辑的分段并点击`View/Edit Segmentation(查看/编辑分段)`。一次只能编辑1个分段。  
**方括号的数量决定了您制作发音的数量。**

![](/assets/images/vocaloid-svs-tutorial/18.png)

过程与**编辑分段**相同，但这次需要确保所有内容都正确对齐。  

点击`Add Articulations To Database(将衔接加入声库)`，根据您选择采样的数量，可能需要几秒钟到几分钟的时间。

![](/assets/images/vocaloid-svs-tutorial/19.gif)

### 步骤4：频率映射(EpR)

>*译注：新版文档中此章已删除，此处保留备用。*

* 注意：如果您想移除采样，不要估算EpR。  
* 
* **这部分不一定对，但也大差不差。**  
**如果声库没有做完，不要做这一步！**

这一步为添加到声库的采样创建EpR模型。  
所需时间取决于声库大小。简单来说，它是采样的频率映射。

![](/assets/images/vocaloid-svs-tutorial/20.gif)

**可能会使声库大小增加数百MB。**  
**创建时可能出现中断，需重新导出数据库。**

## 编辑音素

* **操作后会关闭声库，确保提前保存所有内容。**  
**完成后可重新打开。**

您可通过手动输入以添加额外音素。  
这对于跨语种或额外采样来说十分有用。请注意，您添加的内容，仅在编辑器中手动输入音素时，根据语言才能工作。 
**DBTool的自动分段功能不会转录发音字典之外的音素。**  

`Special(特殊) -> Change Phonetic Unit Group(更改音素单元组)`

![](/assets/images/vocaloid-svs-tutorial/21.png)  
![](/assets/images/vocaloid-svs-tutorial/22.png)  

比方说想添加音素`L`，需要点击`Add PhU(添加音素单元)`  
然后输入`Phonetic Unit Name(音素名称)`和`Phonetic Unit Group(音素类别)`  
在下拉列表中选择`L`所在的音素类别。

![](/assets/images/vocaloid-svs-tutorial/23.png)  

* **或者您也可以参考其他示例直接编辑字典文件。**
**笔者建议您将呼吸音(br)采样添加为耳语声(Whispers)，也可以添加气泡音采样，但不保证其有效。**
**这是创建E.V.E.C的一种方法。**

## 在开发版编辑器中调试

启动Vocaloid 4 Dev Editor，您需要安装：
 - 正版Vocaloid Editor
 - 正版Vocaloid声库  
  （试用版也可以，是否过期无所谓）  

随后，确保您已经下载了Vocaloid Dev Editor，通常是含有这些文件的目录：

![](/assets/images/vocaloid-svs-tutorial/24.png) 

将其同`DB_Dev`文件一同拖入正版Vocaloid编辑器目录中。  

![](/assets/images/vocaloid-svs-tutorial/25.png) 

获得`DB_Dev`后，将所有Vivi的信息替换为您自己的信息。

![](/assets/images/vocaloid-svs-tutorial/26.png) 

**右键点击您的声库文件夹复制地址，以确保后续正常运行。**

![](/assets/images/vocaloid-svs-tutorial/27.png) 

这样便能调试您的声库，即使它尚未打包或完成！**如果您添加或删除了声库的某些部分，您需要重启Dev Editor。**  

![](/assets/images/vocaloid-svs-tutorial/28.png)  

不幸的是，正版Vocaloid有时不会工作，因此您还是需要打包声库以供测试。更新声库时，只需替换DDB和DDI文件即可。

## 打包声库

**建议在做完声库后操作，有时会使您的声库变得特别占空间。**

您的声库将会在Vocaloid 3及更高版本中运行。  

环境配置：
- Python 3.10.0
- Pyyaml (在终端内运行`pip install pyyaml`)
- 在**资源**中下载并解压`DDB_Packer.zip`

您还需要[在这里](/VVD/)生成VVD、安装和卸载脚本。  
点击`?`查看并为您的声库选择一个CompID。  

![](/assets/images/vocaloid-svs-tutorial/29.gif)

接下来将CompID放在对应的位置，并填入您的声库名称，点击`生成声库VVD`。  

将`Format`从`4.0.0.0`更改为`3.0.0.0`。  
将`Growl`从`1`更改为`0`。  
点击`加密`。
点击`下载声库VVD`和`下载安装脚本`。

![](/assets/images/vocaloid-svs-tutorial/30.gif)

**不再需要生成DDI文件，因此移除此部分。**  

找到解压的`DDB_Packer`，右键选择`在终端中打开`。  
将打开一个终端供您打包声库。  

现在开始打包声库。新建以声库名称为名的文件夹，在该文件夹内再新建一个以CompID命名的文件夹。  
将VVD重命名为声库名称，将其同安装和卸载脚本移动到新建的文件夹中。  

返回终端并输入以下命令：
```
python pack_ddb.py - -src_path “singer.inf所在的文件夹” - -dst_path “刚创建的文件夹”
```
![](/assets/images/vocaloid-svs-tutorial/31.gif)  

创建完毕后，将文件夹移动至`VoiceDB`中，并以管理员身份运行安装脚本。  

对于Vocaloid 5和Vocaloid 6，运行Vocal Register / Vocareg。

**出于某种原因，某些mixin不适用于CVVC。或许还有我们未知的其他方法。**

### 添加咆哮

**该操作需要已打包的DDB**  

你需要一个包含咆哮声的声库。例如V4 Flower、VY1等等。  

在终端中打开`DDB_Packer`所在的文件夹，运行如下命令：
```
python mixins_ddb.py - -src_path “您声库.ddi的路径” - -mixins_path “咆哮声.ddi的路径. - -dst_path “新打包声库导出路径”
```
![](/assets/images/vocaloid-svs-tutorial/32.gif)  

这将创建一个新的声库。将其移动到`VoiceDB`所在的位置，确保它同VVD和CompID文件夹中其他文件的名称相匹配。

### 交叉合成

**您需要Vocaloid 4 FE Plus完成这一部分**

![](/assets/images/vocaloid-svs-tutorial/33.png)  
![](/assets/images/vocaloid-svs-tutorial/34.png)  

**这只会使您的声库出现在Vocaloid 4 FE Plus中。如果您想在Vocaloid 5或者6中使用，您需要运行Vocareg。**  

**不同语言的声库无法交叉合成。**  
**不同格式的声库无法交叉合成。**  
**仅包含CVVC的声库无法交叉合成。**  

### 添加Vocaloid 5/6的图像

前往：
C:\Program Files\Common Files\VOCALOID5\Resource\Voice  
C:\Program Files\Common Files\VOCALOID6\Resource\Voice  
您将看到多个CompID文件夹。**在这里新建以您CompID为名的文件夹**，并将图片放入该文件夹中。可参考其他声库的尺寸（600x324）。将其保存为`Setup.bmp`，便可在编辑器中显示。

![]()

## 常见问题

**问：这很难吗？**  
答：毋庸置疑，这不如制作UTAU声库那般流程化，它涉及频繁的窗口切换、测试以及程序切换。您无法自定义音域，也无法在不为编辑器定制的情况下，直接添加自己的字典。即使您设法做到了这些，也很难找到真正合适的方法来设置它。因此，您仍然需要处理音素。此外，Vocaloid的灵活性方面也不如UTAU中那么高。如果您没有足够的耐心，请不要尝试。  


**问：怎样能预览Vocaloid声库的音域？**  
答：DeepVocal在这方面比较准确，您可以在DeepVocal中快速测试音域。  

**问：应该在标记之前处理采样吗？**
答：在采样添加到声库之前处理即可。您甚至可以先标记它们，然后再编辑音频。

**问：所有的采样都是必要的吗？**
答：是的，如果您希望拥有一个包含所有可能组合的完整声库，那么所有采样都是必要的。有些组合可能完全用不到，但保险起见还是应该加上它们。例如，如果您没有收集到所有必要的“n”音采样，那么您将不得不手动编辑音素。  

**问：DBTool崩溃了怎么办？**  
答：重启就行。  

**问：为什么无法删除所有我选中的采样？**  
答：在声库制作完成前不要估算EpR，当你确定声库制作完毕的时候再估算。否则您的采样无法导出，不得不重新制作声库。  

**问：可以移植UTAU声库吗？**  
答：可以，但如果声库没有覆盖整个语言内的所有衔接，您可能需要补录采样，但这是可行的。实话实说，最好还是专门为Vocaloid新录制一个声库，因为这个程序相当繁琐。  

**问：应该在外置存储中操作吗？**  
答：强烈推荐，有些声库可能会达到1~20GB左右。  

**问：没有自制字典怎么办？**  
答：新建歌手并在DBTool中创建它，或者参考其他示例构建一个。  

**问：参数和`C/V_0`之类的东西会起作用吗？**  
答：会起作用。  

**问：为什么`-`不起作用？**  
答：不清楚为什么会这样，试试重新导出一下声库。  

**问：声库可以在Piapro v4x中工作吗？**
答：能。您可以用和Vocaloid 4 FE Plus完全相同的方式加载它们。

## 免责声明

我们不对您自行决定采取的行动承担任何责任。请勿试图通过DBTool或Vocaloid谋取利益。  
请勿盗用他人声音制作声库。  

## 资源

- [VocaloidDBTool3](https://archive.org/details/vocaloid3-developer-kit)*译注：此资源可在bilibili中找到*
- [SMSTools2](https://archive.org/details/smstools-2-application)*译注：此资源可在bilibili中找到*
- [ViVi + VocaDev](https://archive.org/details/vivi-jpn-final)（无需保留Vivi）*译注：此资源可在vocakey中找到*
- [Vocaloid 4 FE Plus](https://elrincondelkitsuneneo2-0.blogspot.com/2021/11/vocaloid-451-editor-version-alpha.html)（包含一个无需安装即可注册声库的软件，但声库仅在Vocaloid 4 FE Plus中显示）*译注：此资源可在vocakey中找到*
- [Piapro V4X](https://elrincondelkitsune.blogspot.com/2016/12/piapro-sfe.html)（包含一个无需安装即可注册声库的软件，但声库仅在Piapro中显示）*译注：此资源可在vocakey中找到*
- [Canned Bread's Swiss Army Knife](https://github.com/bread-in-a-can/Canned-Bread-s-VOCALOIDDBTOOL-Swiss-Army-Knife)（创建空白的`.trans`文件，以及将`.oto`文件转换为`.seq`文件）
- [VVD Editor Plus](/VVD/)（生成VVD文件、安装和卸载脚本。将声库打包以供其他编辑器使用时非常有用）*译注：文内链接均为译者fork版本，更新部分V4英语CompID。*
- [DDB Tools](https://github.com/yuukawahiroshi/ddb-tools)（将声库打包成V3~V6都可以使用的格式。需自备含有咆哮声ddb和ddi文件，可用VY1或Flower的,CYBER SONGMAN是最原始的咆哮声源。）
- [Colab版](https://colab.research.google.com/drive/1AMVBC5ex2QWffivwJm1qeavjBGpsnUQq?usp=sharing)（已更新为使用Github存储库）*译注：[搬运链接](/assets/files/DDB_Packer_Colab.ipynb)，请自行在本地Jupyter或国内Colab平替中使用*
- [DDB Tools GUI](https://github.com/ayatinene/ddb-tools)（更简单的打包工具，需要Python。在cmd中执行`python -m pip install -r requirements.txt`以安装。安装后，执行`python GUI.py`即可启动。）
- [oto2seg](https://github.com/yuukawahiroshi/oto2seg-for-VOCALOIDDBTOOL)（将oto转换为Vocaloid文件。它会切割您的样本，确保已安装ffmpeg和pydub，将其放在同一文件夹中。该工具并不完美，请确保您的样本清晰。仍需自备`Stationary`和`C/V Sil`。`m` `m'` `N` `N'`和`J`也不会自动生成。它会跳过不常见的日语组合，如Hu(ほぅ)、Fu(ふぅ)、Wu(うぅ)和Yi(いぃ)。）
- [自定义字典模板](https://www.mediafire.com/file/fejtjae5h984e3c/Dictionary_base.zip/file)（不像其他字典那样正常工作。使用时，需替换Vocaloid目录中的一个字典文件。确保文件名称相同。不要删除被替换的字典，以便正常使用。）
- [GUMI英语录音表(非模板)](https://docs.google.com/spreadsheets/d/15eBYYlkggMVbqEL1AvLlmLTVvVrNpaqJs9TIl16Y9mE/edit?usp=sharing)（若能自行转换，您将获得模板）*译注：[搬运链接](/assets/files/V3_list.xlsx)*
- [日语CVVC/VCV录音表+转录文件](https://www.mediafire.com/file/4bk3z9uh4or47ii/Vocaloidbase_CVVC_VCV_CC.zip/file)
- [Takeo V2(示例CVVC声库+开发文件)](https://www.mediafire.com/file/fgsm4nrncw1av9a/TAKEO_V2.zip/file) （支持咆哮声，已更新为更响亮、更清晰测采样） 

若您对制作其他语言的模板感兴趣，请通过Twitter或Discord联系@Enlilgen！

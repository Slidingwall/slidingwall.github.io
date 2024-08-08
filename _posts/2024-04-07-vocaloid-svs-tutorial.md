---
layout: post
title: 【中译】Vocaloid声库制作教程
date: 2024-04-07 04:05
category: 歌声合成
author: Zelliel & EnlilGen
tags: [Vocaloid, 歌声合成, 翻译]
summary: 
excerpt_image: /assets/images/vocaloid-svs-tutorial/18.png
top: 1
---

> 译注：本文为该文档中文精翻，仅供学习参考使用，内容及立场不代表译者观点。  
> 文章内容相关问题请咨询原作者。复现文章内容造成一切后果，均与译者无关。  
> [原文地址](https://docs.google.com/document/u/0/d/1vTHLPRp65ejcq5-bA7n_FP6CCgzG8_w0hgoYTCsAxq8)

### 前言

**警告：有史以来最大的工作量**  
如果您**没有**耐心制作Vocaloid声库，请不要尝试！  
如果您的硬盘没有至少1\~20GB的空间，**也不要尝试！**（仅一个音阶的采样就可能占用1\~5GB的空间）  
**这将需要大量的时间、大量的精力、大量的空间。**  
**阅读时不要忽略任何细节。**

## Vocaloid声库制作教程

作者：[Zelliel](https://twitter.com/Zelliell) 与 [EnlilGen](https://twitter.com/EnlilGen)  

如果您有任何值得添加进教程中的信息，请联系原作者。  
本文将带您了解创建Vocaloid声库的过程。

### 准备数据

##### 术语解释

- **Stationary**(持续)：合成长音符时循环的采样。  
  > *译注：多数为韵腹或能独立持续发音的辅音，类似UTAU中的长采样。*  
- **Articulation**(衔接)：连接元音与辅音的衔接采样。  
  > *译注：类似UTAU中的CV及VC。*  
- **Concatenated**(拼接)：将音素拼接在一起。  
- **Trans file**(转录文件)：纯文本，Vocaloid将据此从采样中提取音素。  
- **DBTool**(制作工具)：类似Deepvocal tookit的Vocaloid开发工具。

#### 步骤0：准备工作（可选）

首先像创建其他拼接语音库一样，提前新建若干文件夹，并选择适合您的录制音域。  

![](/assets/images/vocaloid-svs-tutorial/1.png)

在每个文件夹中创建`Stationary`和`Articulation`两个子文件夹。  
`Stationary`中存放长采样，包括元音（如`a`）和部分辅音（如`s` `l`，注意不是`l0`）。短发音（如爆破音`b` `p` `t`）不在此列。  
`Articulation`可采用VCV或CVVC的格式，后文详细介绍。  
* **注意：虽然Stationary不作为拼接使用，但它最好与Articulation选择同一批采样，以保持声库一致性。**  

![](/assets/images/vocaloid-svs-tutorial/2.png)
  
**现在让我们了解Vocaloid中CVVC与VCV的区别。**

#### 步骤1：采样

这一步的选择会大大影响后续进展，最好提前规划好。我们先从简单的开始。  
  
**V/Stationary 合成长音符时循环的短采样。** 没有它们，Vocaloid会在音符中间逐渐无声！为了确保歌声的连贯性，需要录制足够长的样本，以让重采样器不会重复的太生硬。您可以从任何采样中提取，但最好还是和开头结尾样本用同一个采样。有些`Stationary`是辅音，比如`N`或者英语中的`L`。这与UTAU不同，UTAU默认拉伸重采样而不是循环。  
**CVVC/Articulation 实际上就是CVVC。** Vocaloid中可以有`Sil k/a (- k/a)` `k a` `a a` `a k` `k k`以及`k/a Sil (k/a -)`的组合。只要拥有所有的组合（其中`C C`不是必须的），就能得到一个可用的声库。  
**每个音素只有同时拥有`Sil C/V`和`C/V Sil`才能正常播放，不管是哪种类型的声库，都需要音素的开头和结尾**这个方案虽然更容易，但做起来也更繁琐。对于测试声库而言是一个好的选择。这个规则同样适用于英语。  
> *译注：可参考Arpasing理解其原理。中文Vocaloid采用的是CVVC的方案。由于Vocaloid对每个复韵母都赋予单独的发音记号，致使其`V V`部分冗余过多，易被误认为采用了VCV方案。包括CVVChinese、Synthesizer V在内的其他方案都优化了复韵母的音素表记，以减少声库大小。*

**VCV/Triphone(三音素) 是制作声库的精髓。** 但工作量会大大增加。这时组合的格式就像`Sil k a` `a k a`等等，任何能组成三音素的组合都是可行的。如果需要的话，您可以遍历每种可能的组合。VCV可以与CVVC混合使用，以提升声库性能。如果不想做那么多，就偷点懒吧~  
对于英语则略有不同。例如，`star`是一个`C C V`，`s t @r`，而`string`中的`str`则是一个`C C C`，`s t r`。`Sil V V` `V V V`和`V V Sil`也可行，但它会与`Stationary`产生冲突，元音会在`Stationary`和三元音之间循环，使元音发音不完美。  
> *译注：可参考VCCV English理解此部分。英语辅音连缀较为发达，元音前可出现2~3个辅音，元音后最多可出现4个。值得注意的是，VCCV English将辅音连缀视为整体，而Vocaloid限于引擎机能，单条采样只能处理最多3个音素。*

DBTool读取44100Hz 16位的`.wav`音频，只要转录(trans)文件与其同名即可。您也可以像制作UTAU声库一样处理采样。  
**可选操作：**将所有采样导入Audacity去除底噪。应用`Filter Curve EQ(滤波曲线均衡器)> Preset(预设)> Low rolloff for Speech(语音低滚降)`，并进行标准化。处理好后的采样应另存在新文件夹中，避免覆盖源文件。这将为Vocaloid提供最佳音质。使用批量导出功能，按轨道名称一次性导出所有采样。若有去除齿音工具，效果更佳。（像IA一样对采样修音也是可取的！）完成预处理后，即可开始转录工作了。  

#### 步骤2：转录

顾名思义，转录是DBTool识别采样中音素的方式。先用对应语言的发音记号记录音频内容，再在下方用 **`[`方括号`]`** 括出要提取的片段（类似UTAU的别名）。`Stationary`的括号中仅包含一个音素（`[V]/[a]`），但可以用多个括号在一条采样内提取出多个`Stationary`。您最好统筹各个音素提取的位置，除非它们来自是不同的音高，否则应避免音素重复。  

需要明确，**`[`方括号`]`只关注出现的首个音素** 。例如：`Baby -> b eI b eI -> [b eI] [eI b] [b eI]`问题出在：**程序会认为两个`b eI`的内容相同，导致后者无效。** 为了这两个部分区分，需要这么修改：`Baby -> bh eI b eI -> [bh eI] [eI b] [b eI]`。三音素同理：`ba ba bu ba -> b a b a b M b a -> [a b a] [M b a]`，通过开头的音素以区分不同的采样。  

您可以直接将`.txt`重命名为`.trans`来创建转录文件，确保它与采样名称相同。Canned-Bread的Swiss army knife工具能根据采样名称自动生成`.trans`文件以便编辑。如果只做CVVC的话，可以使用auto_transcript功能。但据笔者个人经验，该功能并不完美。生成好的文件需要进行清理与校对，确保音素完全正确。生成后可在DBTool或文本编辑器中编辑，最好先在文本编辑器中处理。批量编辑以避免后续的麻烦，加快工作流程。（[Notepad++](https://notepad-plus-plus.org/)是个救星，但您也可以在记事本中打开，毕竟它们只是文本文件。）

**转录文件示例：**

- Stationary：  

![](/assets/images/vocaloid-svs-tutorial/3.png)

- Articulation：

![](/assets/images/vocaloid-svs-tutorial/4.png)
![](/assets/images/vocaloid-svs-tutorial/5.png)  
![](/assets/images/vocaloid-svs-tutorial/6.png)
![](/assets/images/vocaloid-svs-tutorial/7.png)  

##### 简化转录的基本规则

1. **`Sil`中的`S`必须是大写的！**否则程序不会读取，而您需要重新对转录进行分割。
2. 无需转录整个采样，或一直添加`Sil`。**比如`n ka`，可以只转录`N k`并括出`[N k]`，然后进行下一步。**任何采样都可以只转录关键部分。这样做虽然很浪费，但可以加快进度。
3. **日语专用** N的对应表 **（您需要所有有这些，它们都有`Starionary`）**

    - mm / **m** = `b` `p` `m`
    - mmy / **m'** = `b'` `p'` `m'`
    - **N\\** = `a` `i` `M` `o` `n` `N'` `J` `m` `m'`
    - nng / **N** = `k` `g`
    - nngy / **N'** = `k'` `g'`
    - nn / **N\\** = `h` `C` `p\` `p\'` `w` `v` `v'` `j`
    - nny / **J** = `J`
    - **n** = 所有发音

4. 唯一需要`Stationary`的辅音是鼻音。英语的流音(L)也需要。一些鼻音和流音可能在所有语言都需要`Starionary`。**如果没有`C C`衔接的话，两个辅音之间的过渡会不顺畅。基本上，没有衔接就没有过渡。**  
   > *译注：Vocaloid将中文前后鼻音归纳为复韵母，因此中文是Vocaloid中唯一一个没有`C C`衔接，也没有辅音持续的语言。*
5. 不要在音阶上过于苛刻，这可能会损坏Vocaloid。**音阶一般在3-10个即可。** XSY完全可用，因此不用担心！您可以只为`Articulation`录制3个音阶，但为`Stationary`录制五个以上。**不同语言或不同格式的声库无法交叉合成，仅含有CVVC的声库与XSY不兼容。（规避这个问题，只需要在声库中添加一个VCV样本即可，语言不限。）**
6. `Sil C`**应是无声的，而**`Sil C V`**应是有声的**。处理不当可能会有奇怪的拉长音。流音、鼻音、呼吸音都是如此。**程序不接受**`Sil Sil`**的标记。**
7. **切记，只有Vocaloid支持的语言才有能正常运行的字典。**所以要么在支持语言的范围内操作，要么研究语音学。（可以制作自定义字典，但非常困难）
8. 需要注意的是，即使`bi bi`被读作`b' i` `i b'` ` b' i`，您仍需录制`i b`和`b i`发音。这对所有音素都适用，例如，需要`i h`来衔接`i ha`。即使它的发音是`i C`或`C i`，`i h`和`h i`也应该没区别。
9. 直接复制和粘贴采样是没有问题的。

#### 步骤3：新建声库

一切准备就绪后，以您的歌手名字或代号创建一个空的`.txt`文件。您还需要准备DBTool的字典，DBTool的文件夹内有一些示例，它们是文本格式的，因此可以编辑。您也可以使用DBTool的字典功能来添加内容（后文详解）。

打开DBTool后，**选择**`File(文件) -> New Singer Database(新建歌手数据库)`，加载您选择的字典与您歌手名字命名的空`.txt`。点击`ViewDB -> stationary`检查是否成功。您应该会看到所有的音素和它们下边的`X`，因为还没有加载采样。  

![](/assets/images/vocaloid-svs-tutorial/8.png)

添加采样后，`X`会变成数字，适用于所有部分。采样频率会显示为**一个红点**，**从左到右代表频率从低到高**。点击红点以查看采样并编辑标记，与分割的方式相同。确保通过`nameDB > update markers`来保存更改（如果您得到的声音很怪，多半是标记放错了）。**检查时，请确保每次更换采样都重新点击红点，否则会显示错误的采样。**  

**重复的采样对声库有害。** 如果在同一个声库中添加两个相同音高、相同音素的采样，Vocaloid会在两个采样之间以奇怪的方式切换，使声音听起来笨拙且不均匀，甚至完全破坏Vocaloid。请务必注意获取采样的位置及内容！

创建歌手后，将会自动生成与`.txt`同名的一个文件夹、**一个`.dat`和一个`.tree`文件。** 不要删除这些重要文件。关闭DBTool后，再次打开时可从`singer.inf`所在的文件夹重新加载歌手。只需打开DBtool并加载歌手，就可以继续操作了。

![](/assets/images/vocaloid-svs-tutorial/9.png)
![](/assets/images/vocaloid-svs-tutorial/10.png)

接下来进行标注。

### 创建声库

#### 步骤0：自动分割

点击`File(文件)->Automatic Segmentation(自动分割)`开始分割。采样与转录文件必须在同一文件夹中，DBTool支持识别子文件夹，因此您可以放心加载整个声库。将DBTool设置为分割工具。如果您的操作正确，您将会看到这个界面：

![](/assets/images/vocaloid-svs-tutorial/11.png)

报错是正常的。全选并分割音素，将生成基础标记。之后在查看模式下打开它们并进行修正。注意：编辑转录文件后需要重新进行分割。**误操作会使您重复这些步骤，并强制删除所有刚刚添加的采样。**  

如果在`Stationary`或`Articulation`下显示`Error/0`，则表示转录有误，纠正音素即可。如果显示发音比实际要少，那么转录也有问题。若显示`BAD`字样，标记很可能重叠或者音素不在字典中，需要重做分割。如果持续时间(duration)旁边仅有`0`而没有其他内容，则表示样本不存在。双击转录、`Stationary`和`Articulation`将会打开它们各自的查看器。双击文件名将会打开外部音频查看器。以上操作也可在右键菜单中找到。外部音频编辑器（如`Audacity`）可在`文件`中设置。 

别急，我们先通过下一小节来学习正确配置语音库。

#### 从UTAU到Vocaloid（声库制作指南）

歌声合成开发的学习曲线的陡峭人尽皆知，但通过下面这些可视化指南，它将看起来将会超级简单。  

UTAU中的原音设定都是从零开始的。首先看到的是**采样名称**，通过**别名**来标注想要分割的部分，并用**左/右边界**定位。接着用**固定值**来标记我们始终想要播放的部分。**先行发声**是元音开始的地方，而**重叠**则是淡入淡出开始的地方。  
> *译注：无论音符长短，**固定值**都会参与拼接。当音符短于采样时长时，UTAU会直接让**固定值**与下一音符的**重叠**进行淡入淡出，不再延长韵腹。*  

像前文提到的转录一样，这是在告诉开发工具想要截取哪段采样，并放入语音库中进行淡入淡出以拼接更长的声音。唯一主要的区别时，**您需要定位每个部分的位置。** 例如`babi`，每条线必须和每个音素对齐。比如有一个音素`b`，那么`b`的起止点在哪里。对于后边的`a` `b`等音素同理。  

CVVC示例：

![](/assets/images/vocaloid-svs-tutorial/11-1.png)
![](/assets/images/vocaloid-svs-tutorial/11-2.png)
![](/assets/images/vocaloid-svs-tutorial/11-3.png)
![](/assets/images/vocaloid-svs-tutorial/11-4.png)

界面是英语的，但大同小异。在Vocaloid中则是这样：

![](/assets/images/vocaloid-svs-tutorial/11-5.png)

VC连接音几乎不包含`C`本身，而是其前置音素到此发音的过渡。  

不难看出，**重叠**一般是第一条线，**先行发声**是第二条。而第零条（**重叠**之前，如果不在标记中就不显示）是**左边界**。**固定值**是第三条线，同样也是**右边界**。**标注时，将Vocaloid声库当成Arpasing来对待。** 它们的原理相同，因为都没有`Stationary`音素。对于每个音阶而言，拥有1套开头结尾音素即可，不需要多个。对于`Sil C`/`Sil k` `C Sil`/`K Sil`而言，整个声库只需要1组即可，因为它们本质上就是静音。

换句话说，片段末尾连接的`C`是辅音发音前的过渡区。我们在`Articulation`中想要的不是这个辅音本身，而是它与前置音素的末尾的过渡。

**接下来看VCV**

VCV示例：

![](/assets/images/vocaloid-svs-tutorial/11-6.png)
![](/assets/images/vocaloid-svs-tutorial/11-7.png)

这在Vocaloid中也有所不同。

![](/assets/images/vocaloid-svs-tutorial/11-8.png)

这里有**左右边界**，一个更精确的**重叠**和第二个元音（暨**重叠**之后的元音）开始处的**先行发声**。由于二Vocaloid和UTAU对音素的分割不同，UTAU中的**固定值**并不独立存在。现在可以看出其整体思路。先分割采样，再来隔离每个独立的音素。首先切出来连接元音（第一个元音）或者静音部分，紧接着切出辅音前的过渡区，再来是辅音本身，最后是第二个元音。这个例子并不适用于所有音素，但它是一个大致思路。**可以将其视作`VC` `CV`。**  

现在让我们深入细节。  

#### 步骤1：编辑分段

您可以通过 **`左Ctrl`或者`左Shift+单击`选中多个条目编辑** 。最多同时支持编辑6条。  

点击`View/Edit Segmentation(查看/编辑分段)`  
示例：`ja_ja_ji_ja_ju_ja_je`  

![](/assets/images/vocaloid-svs-tutorial/12.png)

单击**顶部灰栏**以选择音素，同时允许您**选中红条**以编辑音素。  

![](/assets/images/vocaloid-svs-tutorial/13.gif)

接着，您便能按照您的意愿**移动红线**了。  

![](/assets/images/vocaloid-svs-tutorial/14.gif)

**正确的红线位置会减少您稍后在发音菜单中的编辑次数。**  
`Sil C V`：将标记放在音素开始的位置。  
![](/assets/images/vocaloid-svs-tutorial/14-1.png)  
`C V`：将辅音放在前一个音符的末尾，将元音放在辅音之后。  
![](/assets/images/vocaloid-svs-tutorial/14-2.png)  
`Sil C`：标记内什么也没有。  
![](/assets/images/vocaloid-svs-tutorial/14-3.png)  
`Sil V`：标记内可以有声音（不包括鼻音或流音）。  
![](/assets/images/vocaloid-svs-tutorial/14-4.png)  
（晕了吗？可以看看**资源**中的示例声库）

![](/assets/images/vocaloid-svs-tutorial/15.png)

- `空格`：播放采样  
- `Shift+拖动`：选中部分采样并播放  
- `Shift+单击`：取消选中采样  
- `Shift+单击标记`:选择标记中的采样  
- 滚动条旁**绿色箭头**：缩放波形（所有菜单均有这些滚动条）  
- 关闭界面`x`后采样旁出现`YES`：标记已被编辑  
- 如果编辑标记时底部看不到音素，则音素不在字典中。   
（以上适用于自动分割(autoseg)内外的所有菜单）

#### 步骤2：持续采样

选择想分割的采样，点击`View/Edit Segmentation(查看/编辑分段)`。  
这可能需要几秒的时间加载。完成后，选中想要编辑的分段，再次点击`View/Edit Segmentation(查看/编辑分段)`。  

选择或长或短的一段C/V采样，**确保标记不在采样头尾处**，而是采样中间或波形稳定清晰处。越长越好。

![](/assets/images/vocaloid-svs-tutorial/16.png)

将其添加进声库。

![](/assets/images/vocaloid-svs-tutorial/17.gif)

* 遗憾的是，这对于一个测试声库来说远远不够。测试采样还需要添加相同音素的`Sil C/V`或`C/V Sil`。  

这步仅适用于`Stationary`，首先用`Base segmation`分割`Articulation`。然后再分割`Articulation`。**第一步不能跳过！只有在`Stationary`添加完之后才能跳过这一步。** 对于`Stationary`，先执行第1步，然后执行第2步。对于`Articulation`，先执行第1步，然后执行第4步（分割`Articulation`后再校正）

#### 步骤3：衔接采样

选择想要分割的采样并点击`Segment Articulations(分割衔接)`。  
这可能需要几秒的时间加载。完成后，选中想要编辑的分段并点击`View/Edit Segmentation(查看/编辑分段)`。一次只能编辑1个分段。  
**方括号的数量决定了您制作发音的数量。**

例：`- a` `a a` `a -`  
![](/assets/images/vocaloid-svs-tutorial/17-1.png)  
例：`a i` `i a` `a M` `M e` `e a`  
![](/assets/images/vocaloid-svs-tutorial/17-2.png)  
例：`Sil b` `b Sil`  
![](/assets/images/vocaloid-svs-tutorial/17-3.png)  
例：_ba_m_ba_ba_bi_ba_bu_ba (VCV/CVVC)  
![](/assets/images/vocaloid-svs-tutorial/17-4.png)  
例：`Sil n` `Sil J`  
![](/assets/images/vocaloid-svs-tutorial/17-5.png)  


过程与**编辑分段**相同，但这次需要确保所有内容都正确对齐。  

点击`Add Articulations To Database(将衔接加入声库)`，根据您选择采样的数量，可能需要几秒钟到几分钟的时间。

![](/assets/images/vocaloid-svs-tutorial/19.gif)

<details>  <summary><h4><s>步骤4：频率映射(EpR)</s></h4></summary> 

> *译注：新版文档中此章已删除，此处保留备查。*

* 注意：如果您想移除采样，不要估算EpR。  
* 
* **这部分不一定对，但也大差不差。**  
**如果声库没有做完，不要做这一步！**

这一步为添加到声库的采样创建EpR模型。  
所需时间取决于声库大小。简单来说，它是采样的频率映射。

![](/assets/images/vocaloid-svs-tutorial/20.gif)

**可能会使声库大小增加数百MB。**  
**创建时可能出现中断，需重新导出数据库。**

</details>

### 编辑音素

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
**笔者建议您将呼吸音(br)采样添加为爆破音（不光是`br`，还有`br1` `br2`等！它们还需要有一个开头音和结尾音！开头音应该是无声的，而结尾音`br1 Sil`则是呼气的地方。），也可以添加气泡音采样，但不保证其有效。**  
**这是创建E.V.E.C的一种方法。**

### 打包声库

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

~~**不再需要生成DDI文件，因此移除此部分。**~~  

另一种生成CompID的方法是使用资源的Keygen。  
![](/assets/images/vocaloid-svs-tutorial/30-1.png)  
以下是Daigasso提供的一个快速指南！  

* 使用资源中的GUI可跳过此步骤。  

找到解压的`DDB_Packer`，右键选择`在终端中打开`。  
将打开一个终端供您打包声库。  

现在开始打包声库。新建以声库名称为名的文件夹，在该文件夹内再新建一个以CompID命名的文件夹。  
将VVD重命名为声库名称，将其同安装和卸载脚本移动到新建的文件夹中。  

返回终端并输入以下命令：

```shell
python pack_ddb.py - -src_path “singer.inf所在的文件夹” - -dst_path “刚创建的文件夹”
```

![](/assets/images/vocaloid-svs-tutorial/31.gif)  

创建完毕后，将文件夹移动至`VoiceDB`中，并以管理员身份运行安装脚本。  

对于Vocaloid 5和Vocaloid 6，运行Vocal Register / Vocareg。

* 出于某种原因，某些交叉合成不适用于CVVC。或许还有我们未知的其他方法。**（规避这个问题，只需要在声库中添加一个VCV样本即可，语言不限。）**  

#### 添加咆哮

**该操作需要已打包的DDB**  

您需要一个包含咆哮声的声库。例如V4 Flower、VY1等等。  
（Cyber Songman是最原始的咆哮声，其它声库都移植于此）

在终端中打开`DDB_Packer`所在的文件夹，运行如下命令：

```shell
python mixins_ddb.py - -src_path “您声库.ddi的路径” - -mixins_path “咆哮声.ddi的路径. - -dst_path “新打包声库导出路径”
```

![](/assets/images/vocaloid-svs-tutorial/32.gif)  

这将创建一个新的声库。将其移动到`VoiceDB`所在的位置，确保它同VVD和CompID文件夹中其他文件的名称相匹配。

* 如果这太难了，试试GUI。注意，**如果声库只有CVVC，添加咆哮声会破坏DDB和DDI。**
* **若想添加自己的咆哮声，可以使用QuickBMS拆包Vocaloid声库，替换咆哮声，然后再用QuickBMS重新编译。**任何V4声库都可以，选择一个不介意的声库进行操作。
* 您也可以使用GUI**为V3声库添加咆哮声。**

### 导入Vocaloid4
<details>  <summary><h4><s>在开发版编辑器中调试</s></h4></summary>  

> *译注：新版文档已删除，此处保留备查*

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
</details>

**因为开发版编辑器在30天后就会过期，所以最好直接打包声库并在Vocaloid FE上进行测试。** 如有新的进展，可以直接替换DDB和DDI。无需生成全新的CompID，那没有意义。除非您正在制作一个完全不同的声库。

声库经附带了一个“损坏”的XSY，所以您可以在规则下尽情的交叉合成！

**您需要Vocaloid 4 FE Plus（或Piapro V4x）完成这一部分**  

![](/assets/images/vocaloid-svs-tutorial/33.png)  
![](/assets/images/vocaloid-svs-tutorial/34.png)  

**这只会使您的声库出现在Vocaloid 4 FE Plus中。如果您想在Vocaloid 5或者6中使用，您需要准备安装程序，安装后再运行Vocareg。**  

**不同语言的声库无法交叉合成。**  
**不同格式的声库无法交叉合成。**  
**仅包含CVVC的声库无法交叉合成。（规避这个问题，只需要在声库中添加一个VCV样本即可，语言不限。）**  

#### 添加Vocaloid 5/6的图像

前往：
C:\Program Files\Common Files\VOCALOID5\Resource\Voice  
C:\Program Files\Common Files\VOCALOID6\Resource\Voice  
您将看到多个CompID文件夹。**在这里新建以您CompID为名的文件夹**，并将图片放入该文件夹中。可参考其他声库的尺寸（600x324）。将其保存为`Setup.bmp`，便可在编辑器中显示。

![](/assets/images/vocaloid-svs-tutorial/35.png)

### 常见问题

**问：这很难吗？**  
答：这就像是制作一个增强版的UTAU声库。Vocaloid在标注方面一点也不宽容。一个音阶可能起到大作用，也可能毁掉整个声库。如果您不关心采样的位置和取样方法，或许可能会获得一个非常糟糕的声库。没人想看到这样，总的来说，您只能自己摸索。

**问：选CVVC还是VCV？**  
答：说真的吗？选择CVVC会更容易上手，声音也相似。所以只需要添加1个VCV采样即可。在一些必要的中间音和开头音再采用VCV。  

**问：空白音该如何录制？**  
答：转录文件可以解释一切，当您困惑的时候可以查看它们。  

**问：怎样能预览声库的音域？**  
答：Deepvocal！它在这方面比较准确，可以用来快速测试音域。只用`a`采样即可。  

**问：应该在标记之前对采样降噪吗？**  
答：个人认为需要，但只要在采样添加到声库之前降噪即可。您甚至可以先标记它们，然后再编辑音频，因为DevKit是实时保存的。  

**问：所有的采样都是必要的吗？**  
答：是的，这是无法避免的。您要么录制全部采样，要么就手动编辑音素。Vocaloid是专门设计过的！一点小差错都会弄得一团糟。  

**问：DBTool崩溃了怎么办？**  
答：重启就行，DevKit是实时保存的。  

~~**问：为什么无法删除所有我选中的采样？**~~  
~~答：在声库制作完成前不要估算EpR，当您确定声库制作完毕的时候再估算。否则您的采样无法导出，不得不重新制作声库~~。  

**问：可以移植UTAU声库吗？**  
答：当然可以！Vocaloid声音会稍微有点奇怪吗？是的，因为您没有每个样本。但是，您可以通过使用CVVC来处理所有的N音，并强制使用`Sil C`和`C Sil`来“作弊”。然后复制粘贴一些东西，我们就得到了一个声库！（别担心，Miku的声库经常重用样本！事实上，VY1V4 Natural是将其他三个声库合并到一个声库中的！）  

**问：应该在外置存储中操作吗？**  
答：强烈推荐，有些声库可能会达到1~20GB左右，而且这还是开发版本的大小，您应该在外部驱动器上工作。  

**问：没有自制字典怎么办？**  
答：从资源中下载一个，自己构建一个，或者直接“作弊”。Vocaloid只支持它支持的语言，但这并不妨碍您以任何您想要的方式添加音素。注意，不要为V4添加`C/V_0`，它们会自动正常工作。您所要做的就是按音素输入。    

**问：为什么`-`不起作用？**  
答：不清楚为什么会这样，您可能需要重新制作您的声库。也就是说，创建一个新的声库，然后重新添加所有样本。  

**问：声库能在Piapro v4x中使用吗？**  
答：能。您可以用和Vocaloid 4 FE Plus完全相同的方式加载它们。您甚至还可以添加自定义图标！  

**问：声库能在Tunelab中使用吗？**  
答：正确安装后就能尽情使用了。以管理员身份运行安装程序后，无需密钥自动注册。  

**问：我可以分享我的声库吗？**  
答：可以，随VVD、CompID一起分享，其他人就可以毫无问题地使用它。如果分享了安装程序，就可以在tunelab中使用它！把它当作UTAU声库看待即可。但请确保您谨慎行事，并不要称其为官方版本！  

**问：我可以使用人力声库或RVC吗？**  
答：把它当作UTAU看待，尽管不鼓励这么做。  

**问：打包器给我`-9`和`-1`的错误代码？**  
答：`-9`是分段错误，应该出现在配置不完整或者没有正确适当的完成时。`-1`我认为是音频格式错误（不确定，但我觉得是）。--*daigasso*  

**问：最难的部分是？**  
答：当你没有转录文件必须全部手动完成时、当你是独立开发者时！你必须独自完成所有标记并排除故障。最好是分组工作。没有哪部分是容易的，如果完全不了解语音合成，那么会有一个巨大的学习曲线！诚实地说，先学会如何正确配置UTAU、CVVC和VCV，然后再回来制作Vocaloid。  

**问：`N\`是怎么回事？**  
答：Vocaloid依赖前后的音素，所以`N\`是`N`的众多变体之一。所以您需要确保处理好所有音素。甚至，`kya`里的`k'`也是依赖前后音素的。  

**问：`?`起作用吗？**  
答：你可以用它来获得自然的停顿声，比如`Steppu`中，`?`就是`e`和`pu`中间的`p`，或者任何送气音。您也可以用`?`来表示气泡音，用`asp`表示送气音。  

**问：配置中显示`BAD`是什么意思？**  
答：采样标记有重复或者音素不在字典中。  

**问：音频出现故障怎么办？**  
答：检查格式，再重新导出。  

### 免责声明

我们不对您自行决定采取的行动承担任何责任。请勿试图通过DBTool或Vocaloid谋取利益。  
请勿盗用他人声音制作声库。  

### 资源

- [VocaloidDBTool3](https://archive.org/details/vocaloid3-developer-kit)
  > *译注：此资源可在bilibili中找到*
- [SMSTools2](https://archive.org/details/smstools-2-application)
  > *译注：此资源可在bilibili中找到*
- ~~[ViVi + VocaDev](https://archive.org/details/vivi-jpn-final)（无需保留Vivi）~~
  > *译注：此资源可在vocakey中找到 链接仍有效，但已不再需要*
- [Vocaloid 4 FE Plus](https://elrincondelkitsuneneo2-0.blogspot.com/2021/11/vocaloid-451-editor-version-alpha.html)（包含一个无需安装即可注册声库的软件，但声库仅在Vocaloid 4 FE Plus中显示）
  > *译注：此资源可在vocakey中找到*
- [Piapro V4X](https://elrincondelkitsune.blogspot.com/2016/12/piapro-sfe.html)（包含一个无需安装即可注册声库的软件，但声库仅在Piapro中显示）
  > *译注：此资源可在vocakey中找到*
- [Deepvocal](https://www.deep-vocal.com/#/Product) 测试一下音域吧！！
- [Canned Bread's Swiss Army Knife](https://github.com/bread-in-a-can/Canned-Bread-s-VOCALOIDDBTOOL-Swiss-Army-Knife)（创建空白的`.trans`文件，以及将`.oto`文件转换为`.seq`文件）
- [QuickBMS](https://aluigi.altervista.org/quickbms.htm)
- [VVD Editor Plus](/VVD/)（生成VVD文件、安装和卸载脚本。将声库打包以供其他编辑器使用时非常有用）
  > *译注：文内链接均为译者fork版本，更新部分V4英语CompID。*
- [DDB Tools](https://github.com/yuukawahiroshi/ddb-tools)（将声库打包成V3~V6都可以使用的格式。需自备含有咆哮声ddb和ddi文件，我们没法直接提供。可用VY1或Flower的,CYBER SONGMAN是最原始的咆哮声源。）
- [Colab版](https://colab.research.google.com/drive/1AMVBC5ex2QWffivwJm1qeavjBGpsnUQq?usp=sharing)（已更新为使用Github存储库）
  > *译注：[搬运链接](/assets/files/DDB_Packer_Colab.ipynb)，请自行在本地Jupyter或国内Colab平替中使用*
- [DDB Tools GUI](https://github.com/ayatinene/ddb-tools)*(From UselessBug)*（更简单的打包工具，需要Python。在cmd中执行`python -m pip install -r requirements.txt`以安装。安装后，执行`python GUI.py`即可启动。）
- [oto2seg](https://github.com/yuukawahiroshi/oto2seg-for-VOCALOIDDBTOOL)（将UTAU oto转换为Vocaloid文件。它会切割您的样本，确保已安装ffmpeg和pydub，将其放在同一文件夹中。该工具并不完美，请确保您的样本清晰。仍需自备`Stationary`和`C/V Sil`。`m` `m'` `N` `N'`和`J`也不会自动生成。它会跳过不常见的日语组合，如Hu(ほぅ)、Fu(ふぅ)、Wu(うぅ)和Yi(いぃ)。）
- [自定义字典模板](https://www.mediafire.com/file/fejtjae5h984e3c/Dictionary_base.zip/file)（不像其他字典那样正常工作。使用时，需替换Vocaloid目录中的一个字典文件。确保文件名称相同。不要删除被替换的字典，以便正常使用。）
- [GUMI英语录音表(非模板)](https://docs.google.com/spreadsheets/d/15eBYYlkggMVbqEL1AvLlmLTVvVrNpaqJs9TIl16Y9mE/edit?usp=sharing)（若能自行转换，您将获得模板）
  > *译注：[搬运链接](/assets/files/V3_list.xlsx)*
- [日语CVVC/VCV录音表+转录文件](https://www.mediafire.com/file/4bk3z9uh4or47ii/Vocaloidbase_CVVC_VCV_CC.zip/file)*(From Enlilgen)*
- [日语CVVC录音表+转录文件](https://github.com/InochiPM/Vocaloid-Reclist/releases/tag/Reclist-1.2)*(From Inochi-P)*
- [基于单词的日语录音表](https://www.mediafire.com/file/ury58kwe3len0s0/Word_Based_Japanese.zip/file)*(From Ko Ko)* 像UTAU那样录制。每个音节对应一个音拍。（注意`N`算独立的音拍。）虽不完美，但这是一个很好的基础。采样需要复制粘贴。  
- [基于单词的英语录音表](https://www.mediafire.com/file/9z0cch1acqcad1a/Word_Based_English.zip/file)*(From Canned Bread/luciozundiezz)* 像UTAU那样录制，每个音阶对应一个音拍。（参考GUMI的录音表决定要复制哪些样本）虽不完美，但这是一个很好的基础。采样需要复制粘贴。 
- [基于单词的西班牙语录音表PDF](https://www.mediafire.com/file/5pwt3cldp7baen1/Spanish+Reclist+-+Public+Research+Paper.pdf/file)*(From AnotherNN)* 虽不完美，但已精简。
- [Vocaloid2Keygen](https://www.mediafire.com/file/9fo8mlep70m44xz/keygen.rar/file)
- [字典](https://www.mediafire.com/file/37q20qdvhrncibo/Dictionary_Collection.zip/file)*(From daigasso)*
- [Melodyne](https://drive.google.com/file/d/1Ga566Es8hLinnDZxbxVMTOwuLzwzVdIT/view?usp=drivesdk)如果需要的话，编辑或校正样本的音高！
- [Takeo V2(示例CVVC声库+开发文件)](https://www.mediafire.com/file/fgsm4nrncw1av9a/TAKEO_V2.zip/file) （支持咆哮声，已更新为更响亮、更清晰的采样）提供以便于学习并解答关于应该做什么和不应该做什么的疑问。遵循`readme`文件即可尽情地分析它！进行各种实验，尽情发挥，把它作为开发你自己的录音列表或音源库的基础。
- Takeo V4 HARD(示例VCV/CVVC[声库](https://www.mediafire.com/file/1xshvtghv7u15he/TK_HARD_V4_VB.zip/file)+[开发文件](https://www.mediafire.com/file/id6fefspopincfq/TK_HARD_V4_DEV.zip/file))规则同V2声库，您可以交叉合成两个声库。  

如有疑问或寻求帮助，请通过Twitter联系@Enlilgen！

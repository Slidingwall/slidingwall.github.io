---
layout: article
titles:
  # @start locale config
  en      : &EN       Works
  en-GB   : *EN
  en-US   : *EN
  en-CA   : *EN
  en-AU   : *EN
  zh-Hans : &ZH_HANS  作品
  zh      : *ZH_HANS
  zh-CN   : *ZH_HANS
  zh-SG   : *ZH_HANS
  zh-Hant : &ZH_HANT  作品
  zh-TW   : *ZH_HANT
  zh-HK   : *ZH_HANT
  ko      : &KO       작품
  ko-KR   : *KO
  fr      : &FR       Œuvre
  fr-BE   : *FR
  fr-CA   : *FR
  fr-CH   : *FR
  fr-FR   : *FR
  fr-LU   : *FR
  # @end locale config
key: page-works
mode: immersive
header:
  theme: dark
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: linear-gradient(rgba(32, 48, 40, .45),rgba(32, 48, 40, .45))
    src: /assets/images/banners/home.webp
---
<style>
.article__header--overlay .overlay {
  min-height: 240px !important;
}
.page__header .header__brand path {
  fill: rgba(255, 255, 255, .95) !important;
}
</style>
# 作品

### 歌声合成相关

#### [Link of my project files](https://www.alipan.com/s/BW1aSuvRXJR)

Bilibili已投稿作品的各种工程文件。

#### [synthv-dictionaries](/synthv-dictionaries)

【已存档】用于Synthesizer V的用户字典，以使语音库蹩脚的唱出另一种语言。附赠[字典转换器](/synthv-dictionaries/converter.html)。  
介于Synthesizer V 2不提供免费版本，所有用户均能使用跨语种功能而遗憾停更。  

可以[在这里](/synthv-dictionaries/phoneme/Comparison/)比较一下Synthesizer V与Vocaloid之间的音素差异。

#### [vocaloid-dictionaries](/vocaloid-dictionaries)

用于vocaloid的工作插件，以使语音库蹩脚的唱出另一种语言。  
基于通用插件并新增拆音功能，附赠[字典转换器](/vocaloid-dictionaries/converter.html)和改进后的几个现有插件。  
正在无限期重构中。目前在向自动跨语种插件与第三方跨语种填词插件转型。

同时寄存[Vocaloid Sample Parts](/vocaloid-dictionaries/Vocaloid-Sample-Parts)与[发音记号表](/vocaloid-dictionaries/symbol-charts)

#### [mandarin-reclist](/mandarin-reclist)

用于录制中文普通话拼接式语音库的方案，用（最少）83条录音来完成一个中文CVVC声库、（最少）420条录音完成一个VCV声库。  
同时促进了OpenUTAU的中文音素器支持`[REPLACE]`项，以简化oto工作。附赠[oto模板生成器](/mandarin-reclist/generator.html)。  
DeepVocal和VocalSharp的支持还在制作中。*理论很丰满，但还没有付诸于实践 在考虑做韩日双语版，但感觉也没什么必要的样子

#### [hifisampler-rs](https://github.com/Slidingwall/hifisampler-rs)

半成品，一个妄图使用rust重写[hifisampler](https://github.com/openhachimi/hifisampler)后端的构思。

#### [ddb-toolbox-rs](https://github.com/Slidingwall/ddb-toolbox-rs)

带有[GUI](https://github.com/ayatinene/ddb-tools)的[ddb-tools](https://github.com/yuukawahiroshi/ddb-tools)的rust重写，尽可能与Python原版保持一致。  

#### [jsm.data covernter](/歌声合成/2024/04/10/jsm-data.html)

在文章末尾，将Synthesizer V的G2P模型`[语言]-[音素格式]-jsm.data`转为可视化文本的小工具。  

#### Chinese translation of [Arpasing website](https://arpasing.tubs.wtf/zs/)

Arpasing的中文教程翻译。


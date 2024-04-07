---
layout: post
title: 强推一个写Jekyll博客的VScode插件
date: 2024-04-07 03:13
category: 技巧
author: 滑墙
tags: [Jekyll, VScode, 插件]
summary: 
excerpt_image: /assets/images/vscode-jekyll-1.png
---

## 前言

从小到大一直的梦想就是能够拥有一个自己的网站。高三下半年开始逐渐接触到Github Pages，但是当时还是门外汉，苦于配置环境和调整配置，完全是一个盲人摸象的状态。中间也曾经接触过WordPress、Hexo等博客引擎，最终抱着**少折腾**的心态，还是决定使用Github Pages和它原生支持的Jekyll来搭建博客。借着这次更换博客主题的机会，打算捡起来这个想法。不过，Jekyll最折磨人的应该就是头信息和文件名了。这个扩展可以很方便的建立模板，无需在本地安装任何Jekyll环境。  

## 操作环境

 本地用到的软件：经历过Typora收费后，我的Markdown编辑器便转向了VScode。我通过Github Desktop来管理各个仓库。  
 因为是采用Github Pages进行Jekyll编译，所以本地**完全不需要安装**官网要求的Ruby、Python2.7等等东西。可以找一个合适的主题自己个性化一下，注意编辑`_config.yml`的时候要[验证其格式](https://codebeautify.org/yaml-validator)，否则Github Actions渲染时会一直报错。

## 步骤

 1. 首先，在扩展里搜索`jekyll-post`并安装。  
![](/assets/images/vscode-jekyll-1.png)
 2. 安装完成后，在VScode的资源管理器中打开博客的Github仓库。在`_posts`文件夹内右键，选择`New Post`。  
![](/assets/images/vscode-jekyll-2.png)
 3. 在弹出来的对话框中输入文件的标题名称，插件会自动读取当前的系统时间来创建自动命名好的文件。  
![](/assets/images/vscode-jekyll-3.png)
 4. 同时，头信息也自动包含在了新建的文件中。可以通过在博客根目录建立`.post-template`以自定义头信息模板。  
![](/assets/images/vscode-jekyll-4.png)

# Web3 Exchange YouTube 爬虫程序

## 简介
Web3 Exchange YouTube 爬虫程序是一款自动化工具，可以模拟用户在浏览器中操作，通过指定关键词搜索 YouTube 视频，提取相关信息（如标题、链接、播放量、发布时间）并保存到 CSV 文件。同时，程序会生成视频标题的词云图，帮助直观分析关键词的分布和重要性。

## 功能特色
模拟人为操作打开浏览器，避免部分反爬限制。
根据关键词自动匹配相关视频。
导出符合条件的视频数据到 CSV 文件。
生成基于视频标题的词云图，支持自定义形状。

## 系统要求
操作系统：Windows 10/11 或 macOS
Python版本：Python 3.8 或以上
浏览器：Google Chrome（推荐版本：131）
依赖库：
  * Selenium
  * WordCloud
  * Matplotlib
  * NumPy
  * Pillow

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

## 使用说明
### 用法一：Python 环境运行
#### 安装 Python
  确保系统中已正确安装 Python，并配置环境变量。

#### 安装依赖库
  使用以下命令安装必要的 Python 库：
  `pip install selenium wordcloud matplotlib numpy pillow`

#### 检查 Chrome 版本
  确认系统中安装的 Google Chrome 浏览器版本为 131，因为程序使用了适配该版本的 `ChromeDriver`。

#### 运行程序
  在命令行中执行以下命令：
  `python main.py`

  根据提示输入搜索关键词和数据量。
  搜索完成后，程序会生成 `youtube_videos_filtered.csv` 文件和词云图 `youtube_titles_wordcloud.png`。

#### 检查结果
  在程序目录下，查看生成的 CSV 文件和词云图。

### 用法二：运行打包的 .exe 文件

  打开 `dist` 文件夹，找到 `main.exe` 文件。

#### 运行程序
  双击 `main.exe` 文件，在弹出的窗口中：

#### 输入搜索关键词。
  程序会自动搜索，并生成 CSV 文件和词云图。
#### 查看结果
  程序运行完成后，结果将输出到同级目录下的 `youtube_videos_filtered.csv` 和 `youtube_titles_wordcloud.png` 文件中。

#### 监控运行状态
  运行过程中，可在终端中查看日志信息，了解程序状态或错误信息（如未加载资源或网络问题）。

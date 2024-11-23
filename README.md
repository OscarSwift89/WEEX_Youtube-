# Weex-Twitter

使用 Python 编写的爬虫，自动搜索 Weex 在 Twitter 上的相关内容并搜集数据。

## 目录结构

```plaintext
Weex-Twitter/
├── main.py               # 主程序入口
├── login.py              # 登录功能模块
├── search.py             # 搜索功能模块
├── requirements.txt      # 依赖库列表
├── README.md             # 项目说明文档
└── chromedriver.exe      # ChromeDriver 执行文件
```

## 环境依赖
运行此项目需要以下环境与依赖：

* 操作系统：Windows 10 或更高版本
* Python：Python 3.8 或更高版本
* 浏览器：Google Chrome (版本 131 或更高)
* ChromeDriver：与 Chrome 浏览器版本匹配的 ChromeDriver

安装依赖库
使用以下命令安装所需依赖
pip install -r requirements.txt
requirements.txt 包含以下主要依赖库：

selenium
webdriver-manager

## 使用说明
1. 配置环境
确保 chromedriver.exe 位于项目根目录。
将 chromedriver.exe 的路径配置到系统环境变量，或直接在代码中指定完整路径。
2. 运行项目
运行主程序入口：

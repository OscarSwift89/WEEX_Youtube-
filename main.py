import os
import re
import csv
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

####################################################################################
# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 设置默认爬取数量和输出文件
MAX_RESULTS = 100
OUTPUT_CSV = 'youtube_videos_filtered.csv'

def matches_keywords(text, patterns):
    """
    检查文本是否匹配任意一个关键词模式
    :param text: 要检查的文本
    :param patterns: 正则表达式模式列表
    :return: 布尔值，表示是否匹配
    """
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):  # 忽略大小写
            return True
    return False

###################################################################################################

def fetch_youtube_videos(query, max_results, patterns):
    """
    爬取 YouTube 视频信息
    """
    logging.info(f"启动浏览器，开始爬取关键词: {query}")
    driver = webdriver.Chrome()
    driver.get('https://www.youtube.com')

    search_box = driver.find_element(By.NAME, 'search_query')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    time.sleep(3)  # 等待页面加载

    videos = []
    scroll_count = 0
    while len(videos) < max_results:
        video_elements = driver.find_elements(By.CSS_SELECTOR, 'ytd-video-renderer')

        for video in video_elements[len(videos):]:
            try:
                title = video.find_element(By.ID, 'video-title').text
                link = video.find_element(By.ID, 'video-title').get_attribute('href')

                # 从搜索结果页面直接提取播放量和发布时间
                metadata_line = video.find_element(By.CSS_SELECTOR, '#metadata-line').text.split('\n')
                views = metadata_line[0] if len(metadata_line) > 0 else "N/A"
                publish_time = metadata_line[1] if len(metadata_line) > 1 else "N/A"

                description = video.find_element(By.ID, 'description-text').text if video.find_element(By.ID, 'description-text') else ""

                # 调试信息
                logging.debug(f"检测到视频: {title}, 描述: {description}")

                # 过滤只包含关键词的结果
                if matches_keywords(title, patterns) or matches_keywords(description, patterns):
                    videos.append({
                        'title': title, 'link': link, 'views': views,
                        'publish_time': publish_time
                    })
                else:
                    logging.debug(f"视频未匹配关键词: {title}")
            except Exception as e:
                logging.error(f"解析视频信息失败: {e}")
            if len(videos) >= max_results:
                break

        # 增加滚动次数和等待时间
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)
        scroll_count += 1
        if scroll_count > 20:
            logging.warning("已达到最大滚动次数，结束爬取")
            break

    driver.quit()
    return videos[:max_results]

########################################################################################################

def save_to_csv(videos, output_file):
    """
    将爬取到的视频信息保存到 CSV 文件
    """
    if not videos:
        print("没有数据可写入 CSV 文件！")
        return

    print(f"准备写入 {len(videos)} 条数据到 {output_file}")
    # 使用 utf-8-sig 编码，避免乱码问题
    with open(output_file, mode='w', encoding='utf-8-sig', newline='') as file:
        fieldnames = ['Title', 'Link', 'Views', 'Publish Time']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for video in videos:
            writer.writerow({
                'Title': video['title'],
                'Link': video['link'],
                'Views': video['views'],
                'Publish Time': video['publish_time']
            })

#########################################################################################################

def generate_wordcloud_with_shape(titles, shape_image='weex.png', output_file='wordcloud.png', font_path='C:/Windows/Fonts/msyh.ttc'):
    """
    根据视频标题生成特定形状的词云图片
    :param titles: 视频标题列表
    :param shape_image: 用于定义词云形状的图片路径
    :param output_file: 保存词云图片的文件路径
    :param font_path: 支持中文的字体文件路径
    """
    # 将所有标题合并成一个字符串
    text = ' '.join(titles)
    
    # 加载形状图片并转换为数组
    mask = np.array(Image.open(shape_image))
    
    # 初始化词云对象
    wordcloud = WordCloud(
        font_path=font_path,  # 指定支持中文的字体路径
        width=1920,           # 提高分辨率宽度
        height=1080,          # 提高分辨率高度
        background_color='white',
        mask=mask,
        contour_width=1,      # 轮廓线宽度
        contour_color='black',
        colormap='viridis',   # 配色方案
        max_words=500,        # 显示更多词语
        relative_scaling=0.6, # 增强重要词语权重
        min_font_size=10,     # 设置最小字体大小
    ).generate(text)
    
    # 显示词云
    plt.figure(figsize=(15, 10))  # 设置显示尺寸
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Video Titles Word Cloud (Enhanced)", fontsize=24)
    plt.show()
    
    # 保存词云到文件
    wordcloud.to_file(output_file)
    print(f"词云已保存到 {output_file}")


#####################################################################################################

def main():
    print("当前工作目录:", os.getcwd())
    search_query = input("请输入想要搜索的关键词：").strip()
    
    # 自动生成关键词匹配模式
    search_patterns = [
        rf'\b{search_query}\b',               # 完全匹配关键词
        rf'{search_query}',                   # 部分匹配关键词
        rf'\b{search_query}\s*\b交易所\b',    # 关键词+交易所
        rf'\b{search_query}\s*\bExchange\b'  # 关键词+Exchange
    ]
    logging.info(f"使用关键词模式: {search_patterns}")
    
    videos = fetch_youtube_videos(search_query, MAX_RESULTS, search_patterns)
    print(f"共获取到 {len(videos)} 条符合条件的视频信息")

    save_to_csv(videos, OUTPUT_CSV)
    print(f"数据已保存到 {OUTPUT_CSV}")

    return videos  # 返回视频信息列表

#####################################################################################################

if __name__ == '__main__':
    videos = main()  # 接收爬取到的视频信息
    if videos:
        titles = [video['title'] for video in videos]  # 提取标题
        # 生成特定形状的词云
        generate_wordcloud_with_shape(
            titles,
            shape_image='weex.png',  # 替换为你的形状图片路径
            output_file='youtube_titles_wordcloud.png'
        )
    else:
        print("未获取到视频信息，无法生成词云。")

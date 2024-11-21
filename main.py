import os
import re
import csv
import sys
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# 配置日志记录
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

####################################################################################
# 设置关键词和爬取数量
SEARCH_QUERY = 'weex'
SEARCH_PATTERNS = [
    r'\bweex\b',  # 匹配 "weex"
    r'\bwe\s+ex\b',  # 匹配 "we ex"
    r'\bweex\s+交易所\b',  # 匹配 "weex 交易所"
    r'\bweex\s+Exchange\b',  # 匹配 "weex Exchange"
    r'\bweex\b.*\b交易所\b',  # 匹配 "weex" 和后续的 "交易所"
    r'\bweex\b.*\bExchange\b',  # 匹配 "weex" 和后续的 "Exchange"
]
MAX_RESULTS = 100

# 动态路径设置
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
SHAPE_IMAGE_PATH = os.path.join(BASE_DIR, 'weex.png')  # 形状图片路径
OUTPUT_CSV = os.path.join(BASE_DIR, 'youtube_videos_filtered.csv')  # 输出 CSV 路径
WORDCLOUD_OUTPUT_PATH = os.path.join(BASE_DIR, 'youtube_titles_wordcloud.png')  # 输出词云图片路径

####################################################################################

def check_dependencies():
    """检查依赖库是否可用"""
    try:
        import selenium
        import numpy
        import PIL
        import wordcloud
        import matplotlib
        logging.info("所有依赖库加载成功")
    except ImportError as e:
        logging.error(f"依赖库加载失败: {e}")
        print(f"请安装依赖库后再运行程序: {e}")
        sys.exit(1)

def matches_keywords(text, patterns):
    """检查文本是否匹配关键词"""
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):  # 忽略大小写
            return True
    return False

####################################################################################

def fetch_youtube_videos(query, max_results, patterns):
    """爬取 YouTube 视频信息"""
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

                metadata_line = video.find_element(By.CSS_SELECTOR, '#metadata-line').text.split('\n')
                views = metadata_line[0] if len(metadata_line) > 0 else "N/A"
                publish_time = metadata_line[1] if len(metadata_line) > 1 else "N/A"

                description = video.find_element(By.ID, 'description-text').text if video.find_element(By.ID, 'description-text') else ""

                if matches_keywords(title, patterns) or matches_keywords(description, patterns):
                    videos.append({
                        'title': title, 'link': link, 'views': views, 'publish_time': publish_time
                    })
            except Exception as e:
                logging.error(f"解析视频信息失败: {e}")
                continue

            if len(videos) >= max_results:
                break

        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        scroll_count += 1
        if scroll_count > 20:
            logging.warning("已达到最大滚动次数，结束爬取")
            break

    driver.quit()
    return videos[:max_results]

####################################################################################

def save_to_csv(videos, output_file):
    """保存数据到 CSV 文件"""
    if not videos:
        logging.warning("没有数据可写入 CSV 文件！")
        return

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
    logging.info(f"数据已保存到 {output_file}")

####################################################################################

def generate_wordcloud_with_shape(titles, shape_image, output_file):
    """根据视频标题生成特定形状的词云图片"""
    if not os.path.exists(shape_image):
        logging.error(f"形状图片 {shape_image} 不存在，无法生成词云")
        print(f"形状图片 {shape_image} 不存在，无法生成词云")
        return

    text = ' '.join(titles)
    mask = np.array(Image.open(shape_image))

    wordcloud = WordCloud(
        width=800,
        height=800,
        background_color='black',
        mask=mask,
        contour_width=1,
        contour_color='yellow',
        max_words=200
    ).generate(text)

    wordcloud.to_file(output_file)
    logging.info(f"词云已保存到 {output_file}")
    print(f"词云已保存到 {output_file}")

####################################################################################

def main():
    """主程序入口"""
    check_dependencies()
    print("当前工作目录:", os.getcwd())
    logging.info("程序开始运行")

    try:
        videos = fetch_youtube_videos(SEARCH_QUERY, MAX_RESULTS, SEARCH_PATTERNS)
        logging.info(f"共获取到 {len(videos)} 条符合条件的视频信息")

        save_to_csv(videos, OUTPUT_CSV)

        if videos:
            titles = [video['title'] for video in videos]
            generate_wordcloud_with_shape(titles, SHAPE_IMAGE_PATH, WORDCLOUD_OUTPUT_PATH)
        else:
            print("未获取到符合条件的视频信息")
            logging.warning("未获取到符合条件的视频信息")
    except Exception as e:
        logging.error(f"程序运行失败: {e}")
        print(f"程序运行失败: {e}")
    logging.info("程序结束运行")

####################################################################################

if __name__ == '__main__':
    main()

import re
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

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

def fetch_youtube_videos(query, max_results, patterns):
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

                # 过滤只包含关键词的结果
                if matches_keywords(title, patterns) or matches_keywords(description, patterns):
                    videos.append({
                        'title': title, 'link': link, 'views': views,
                        'publish_time': publish_time
                    })
            except Exception as e:
                print(f"解析视频信息失败: {e}")
            if len(videos) >= max_results:
                break

        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        scroll_count += 1
        if scroll_count > 20:
            print("已达到最大滚动次数，结束爬取")
            break

    driver.quit()
    return videos[:max_results]

def save_to_csv(videos, output_file):
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

def main():
    print("当前工作目录:", os.getcwd())
    videos = fetch_youtube_videos(SEARCH_QUERY, MAX_RESULTS, SEARCH_PATTERNS)
    print(f"共获取到 {len(videos)} 条符合条件的视频信息")

    save_to_csv(videos, OUTPUT_CSV)
    print(f"数据已保存到 {OUTPUT_CSV}")

if __name__ == '__main__':
    main()

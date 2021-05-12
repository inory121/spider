import os
import re
import shutil
import requests
from bs4 import BeautifulSoup


def send_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/75.0.3770.100 Safari/537.36 "
    }
    return requests.get(url, headers=headers, timeout=10).content


# 图片的链接
img_link_list = []
# 最终保存在硬盘的绝对路径
img_name_list = []


def main(url, path_prefix, format_type, page_num):
    """
    :param url: 图片网站链接
    :param path_prefix: 保存路径前缀
    :param format_type: 保存的图片格式
    :param page_num: 最多爬取页数
    :return: None
    """
    if os.path.exists(path_prefix):
        shutil.rmtree(path_prefix)
    print("开始创建目录...")
    for i in range(1, page_num):
        os.makedirs((path_prefix + "第{0}页").format(i), exist_ok=True)

        url = (url + "{0}").format(i)
        content = send_request(url)
        soup = BeautifulSoup(content, "html.parser")

        for item in soup.find_all('a', class_={"directlink largeimg", "directlink smallimg"}):
            img_link = item.get('href')
            img_link_list.append(img_link)

        for item in soup.find_all('a', class_="thumb"):
            img_real_name = re.findall(re.compile(r'/post/show/[0-9]*/(.*)', re.S), item.get('href'))[0]
            img_path_name = (path_prefix + "第{0}页\\").format(i) + img_real_name + format_type
            img_name_list.append(img_path_name)
    print("目录创建完成!!!")

    print("开始下载图片")
    for i in range(0, len(img_name_list)):
        img_data = send_request(img_link_list[i])
        print(img_name_list[i])
        with open(img_name_list[i], "wb") as image:
            image.write(img_data)
    print("图片下载完成!!!")


if __name__ == "__main__":
    main("https://konachan.net/post?page=", "F:\\anime\\", ".jpg", 10)

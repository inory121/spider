import re
import sqlite3
import urllib.request

import xlwt
from bs4 import BeautifulSoup


# 主方法
def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    # savepath = "豆瓣电影Top250.xls"
    dbpath = "movie.db"
    # saveData(datalist, savepath)
    saveData2DB(datalist, dbpath)


# 保存数据到sqlite
def saveData2DB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movie (info_link,pic_link,cname,ename,score,rated,introduction,info)
            values (%s)''' % ",".join(data)
        c.execute(sql)
        conn.commit()
    c.close()
    conn.close()


# 建表
def init_db(dbpath):
    conn = sqlite3.connect(dbpath)
    print("打开数据库成功")
    c = conn.cursor()
    sql = '''
        create table movie(
            id integer primary key autoincrement,
            info_link text,
            pic_link text,
            cname varchar,
            ename varchar,
            score numeric ,
            rated numeric ,
            introduction text,
            info text
        )
    '''
    c.execute(sql)
    conn.commit()
    conn.close()


# 正则
findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 获取影片数据
def getData(baseUrl):
    datalist = []
    for i in range(0, 10):
        url = baseUrl + str(i * 25)
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            data = []
            item = str(item)
            # 影片超链接
            link = re.findall(findLink, item)[0]
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            title = re.findall(findTitle, item)
            if len(title) == 2:
                ctitle = title[0]
                data.append(ctitle)
                otitle = title[1].replace("\u00a0", "").replace("/", "")
                data.append(otitle)
            else:
                data.append(title[0])
                data.append("  ")
            rating = re.findall(findRating, item)[0]
            data.append(rating)
            judge = re.findall(findJudge, item)[0]
            data.append(judge)
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append("  ")
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)
            bd = re.sub('/', " ", bd)
            bd = re.sub("\u00a0", "", bd)
            data.append(bd.strip())
            datalist.append(data)
    return datalist


# 模拟浏览器发送请求
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存获取的影片数据
def saveData(datalist, savepath):
    print("saving......")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
    col = ("电影链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价人数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])

    book.save(savepath)


# 程序主入口
if __name__ == "__main__":
    main()
    print("爬取完毕")

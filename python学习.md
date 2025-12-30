# day1
学习了re正则匹配，先用re.compile(正则表达式)，再finditem（要寻找的内容），通过group分组获取
xpath需要etree库，from lxml import etree
```
import requests
import re
# url = "https://piaofang.maoyan.com/dashboard-ajax"
""" params = {
    "orderType": 0,
    "uuid": "9353abda-5f4b-4874-8fb5-f45af34c48b8",
    "timeStamp": 1766411972340,
    "User-Agent": "TW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDYuMDsgTmV4dXMgNSBCdWlsZC9NUkE1OE4pIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xNDMuMC4wLjAgTW9iaWxlIFNhZmFyaS81MzcuMzY=",
    "index": 570,
    "channelId": 40009,
    "sVersion": 2,
    "signKey": "e564f8e979aaa490d279c485f4d7b44e",
    "WuKongReady": "h5"
}
headers = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
}
response = requests.get(url, params=params, headers=headers)
print(response.status_code)
print(response.text) """

# re模块
""" import re
# 正则表达式匹配
text = "Hello, my name is John Doe and I am 25 years old.123 l like 888" """
# 预加载，就是提前写好正则表达式，不用每次使用时都写
""" obj = re.compile(r'\d+') """
# 通过finditer方法进行查找,返回一个迭代器
""" result = obj.finditer(text)
for i in result:
    print(i.group()) """

# 通过findall方法进行查找，返回一个列表
""" result = obj.findall(text)
print(result)  """ 

# 通过search方法进行查找，只返回第一个匹配到的值
""" result = obj.search(text)
print(result.group) """       

# 通过match方法进行查找，匹配第一个，没有则停止匹配
""" result = obj.match(text)
print(result) """

# 可以通过?P<name>（小括号中为匹配的内容）来命名组，从而在迭代器里的group方法中通过name来获取值


url = "https://movie.douban.com/top250"
headers = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
}
response = requests.get(url, headers=headers)
html = response.text
obj = re.compile(r'<div class="item">.*?<span class="title">(?P<name>.*?)</span>'
                 r'.*?<p>.*?导演: (?P<dao>.*?)&nbsp,*?主演: (?P<actor>.*?)<br>', re.S)
result = obj.finditer(html)
for i in result:
    print(i.group("name"), i.group("dao"), i.group("actor"))
```

# day2
## 电影天堂爬取链接
```
import requests
import re
url = "https://www.dy2018.com"
headers = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36"
}

resp = requests.get(url, headers=headers)
resp.encoding = 'gb2312'
# print(resp.text)

# 提取2025必看热片部分
obj1 = re.compile(r'2025必看热片.*?<ul>(?P<html>.*?)</ul>', re.S)
result = obj1.search(resp.text)
if result:
    html = result.group("html")

#提取电影的链接
obj2 = re.compile(r"<li><a href='(?P<link>.*?)' title", re.S)
result = obj2.finditer(html)

obj3 = re.compile(r'<div id="Zoom">.*?片　　名　(?P<movie>.*?)<br />.*?<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<download>.*?)">', re.S)
for i in result:
    link = i.group("link")
    child_url = url.strip('/') + link
    child_resp = requests.get(child_url, headers=headers)
    child_resp.encoding = 'gb2312'
    child_result = obj3.search(child_resp.text)
    if child_result:
        print(child_result.group("movie"))
        print(child_result.group("download"))
    # print(link)

```
### 模拟浏览器访问--cookie
使用session
request = requests.session()

# day3 爬去梨视频
防盗链中，Refer：就是溯源链接，需要补上
```
url = "https://www.pearvideo.com/video_1804335"
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
    "Referer": url
}
contId = url.split("_")[1]
videoStatusURL = f"https://www.pearvideo.com/videoStatus.jsp?contId={contId}&mrd=0.24300385243810207"
resp = requests.get(videoStatusURL, headers=headers)
resp_json = resp.json()
videoURL = resp_json["videoInfo"]["videos"]["srcUrl"]
systemTime = resp_json["systemTime"]
vURL = videoURL.replace(systemTime, f"cont-{contId}")
with open("video.mp4", "wb") as f:
    video_resp = requests.get(vURL, headers=headers)
    f.write(video_resp.content)
print("视频下载完成")# 下载地址举例
```
# day4
使用代理 proxy
```
proxy = {
    "http": "http://"
    "https: "https://"
}
```

```
import requests

def get_ip():
    urlip = "http://httpbin.org/ip"
    resp = requests.get(urlip)
    ips = resp.json()['data']['ip']
    for ip in ips:
        yield ip

def scrapt():
    url = "https://www.example.com"

    while True:
        try:
            proxys = {
                    "http": f"http://{next(get_ip())}",
                    "https": f"http://{next(get_ip())}"
                }
            resp = requests.get(url, proxies=proxys)
            resp.encoding = 'utf-8'
            return resp.text
        except :
            print("更换ip中")

if __name__ == "__main__":
    for i in range(10):
        scrapt()

```
# day4
### 多线程
进程是资源单位，至少有一个线程
线程是执行单位
```
from threading import Thread

class MyThread(Thread):
    def run(self):
        for i in range(100):
            print(f"线程 {self.name} 输出: {i}")

if __name__ == "__main__":
    t = MyThread()
    t.start()
    for i in range(100):
        print(f"主线程 输出: {i}")
```
##### 线程池就是一次性开辟多个线程，然后给线程池分配任务

##### 协程就是当程序遇到IO操作被堵塞的时候，可以选择性的切换到其他任务上
协程需要使用asyncio库来使用
await 挂起操作，只能在异步函数中进行使用，异步函数返回的是一个异步对象
创建异步对象需要asyncio.create_task(异步函数)
asyncio.wait(多任务列表)
最后需要asyncio.run(主函数)
```
import asyncio
import time

async def download(url):
    print("Downloading...")
    #time.sleep(2) 异步使用同步语句会停止异步
    await asyncio.sleep(2)
    print("Download complete.")

async def main():
    urls = {
        "https://example.com/file1",
        "https://example.com/file2",
        "https://example.com/file3"
    }
    tasks = []
    for u in urls:
        t = asyncio.create_task(download(u))
        tasks.append(t)
    await asyncio.wait(tasks)

if __name__ == "__main__":
    asyncio.run(main())
```
```
request.get()也是同步操作，需要使用aiohttp
async def aiodownload(url):
    name = url.split("/")[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            with open((f"name{i}.jpg" for i in range(3)), "wb") as f:
                f.write(await resp.read())
            await resp.text()
    print("Download complete.") 
async def main():
    urls = {
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEUKhGK8UYTUqpbUoVYT9vJOBFnUbhnEZG2L1SKj0oo_qb_dnIUBoQNNpSVA7oc_jAM2GNAO3QjDen1fgtLHegJ8XauC-vTxzytnsohyhI&s=10",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTf7dFGleObRtZDXuLY1ozgF2rZ-C7hTQzJwGYljiM_h1RvFgA669r73HgNDYpAdeNfaJdvt590gm5BDug3EHtTkQoJoG8BVGSdQszsORVs&s=10",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRllzh8jxm-JxUk3xTU1wIqGAEzPlMckvXHWaTpCmhuhHcczQrqSxp1JSpfXrKCz5tZFXvp5b0TNrZ6IjHTEsP3fMMXsE_O_OQoNyONPDR3Ag&s=10"
    }
    tasks = []
    for u in urls:
        t = asyncio.create_task(aiodownload(u))
        tasks.append(t)
    await asyncio.wait(tasks)
if __name__ == "__main__":
    asyncio.run(main())
```
# day7
### Scrapy框架
##### 框架原理
爬虫组件url--》引擎--〉调度器--》引擎--〉下载器（发送请求）--》引擎--〉爬虫程序解析--》引擎--〉管道（保存数据）

- 创建项目：scrapy startproject 根目录名
- 创建爬虫程序：scrapy genspider xiao 4399.com
- 启动爬虫程序：scrapy crawl 爬虫程序名（xiao）
- 数据返回到pipline管道进行处理，启动管道（settings里面打开）"game.pipelines.GamePipeline": 300,设置管道的优先级

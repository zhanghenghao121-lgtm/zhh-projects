# day1
学习了re正则匹配，先用re.compile(正则表达式)，再finditem（要寻找的内容），通过group分组获取
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

import requests
from time import sleep

headers = {
    'Host':"m.weibo.cn",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,pt;q=0.7",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}

def get_user_info(uid):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}'.format(uid)
    # proxies = {
    #     	#"http": "http://119.115.235.131",
    #     	"https": "https://113.222.81.108",
    #      }
    result = requests.get(url, headers = headers, timeout = 10) # timeout = 10
    #print(result.status_code)
    json_data = result.json()
    #print(json_data)
    json_data = json_data['data']
    #print(json_data)
    userinfo = {
        'name': json_data['userInfo']['screen_name'],  # 获取用户头像
        'description': json_data['userInfo']['description'],  # 获取用户描述
        'follow_count': json_data['userInfo']['follow_count'],  # 获取关注数
        'followers_count': json_data['userInfo']['followers_count'],  # 获取粉丝数
        'profile_image_url': json_data['userInfo']['profile_image_url'],  # 获取头像
        'verified_reason': json_data['userInfo']['verified_reason'],  # 认证信息
        'containerid': json_data['tabsInfo']['tabs'][1]['containerid']  # 此字段在获取博文中需要
    }
    if json_data['userInfo']['gender'] == 'm':
        gender = '男'
    elif json_data['userInfo']['gender'] == 'f':
        gender = '女'
    else:
        gender = '未知'
        userinfo['gender'] = gender
    return userinfo

userinfo1 = get_user_info('1350995007')
# print(userinfo1)

def get_all_post(uid, containerid):
    page = 0
    posts = []
    while page < 10:
        result = requests.get('https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid={}&page={}'.format(uid, containerid, page))
        json_data = result.json()
        json_data = json_data['data']
        #print(json_data['cards'])
        # if not json_data['cards']:
        #     break
        for i in json_data['cards']:
            #print(i.keys())
            if(i.get('mblog')):
                posts.append(i['mblog']['text'])
        sleep(0.5)
        page += 1
    return posts

posts = get_all_post('1350995007', '1076031350995007')
print(len(posts))

import jieba.analyse
from html2text import html2text
content = '\n'.join([html2text(i) for i in posts])
result = jieba.analyse.textrank(content, topK=1000, withWeight=True)
keywords = dict()
for i in result:
    keywords[i[0]] = i[1]
print(keywords)

from PIL import Image, ImageSequence
import numpy as np

import matplotlib.pyplot as plt

from wordcloud import WordCloud, ImageColorGenerator

image = Image.open('./images/personas.jpg')
graph = np.array(image)
wc = WordCloud(font_path='./fonts/msyh.ttf',background_color='white', max_words=300, mask=graph)
wc.generate_from_frequencies(keywords)
image_color = ImageColorGenerator(graph)
plt.imshow(wc)

plt.imshow(wc.recolor(color_func=image_color))

plt.axis('off') # 关闭图像坐标系

plt.show()
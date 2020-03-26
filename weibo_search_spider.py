import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import jieba
import wordcloud
from matplotlib import pyplot as plt
import random
import time
from playsound import playsound


class Weibo_Spider():
    def __init__(self):
        self.host = 'm.weibo.cn'
        self.base_url = 'https://m.weibo.cn/api/container/getIndex?'

        #构建一个列表
        self.agent_list = ['Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
                      'Mozilla/5.0 (Linux; Android 8.1; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools',
                      'Mozilla/5.0 (Linux; Android 8.1.0; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)',
                      'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN',
                      'Mozilla/5.0 (Linux; U; Android 8.0.0; zh-CN; MHA-AL00 Build/HUAWEIMHA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.1.4.994 Mobile Safari/537.36',
                      'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
                      'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN',
                      'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A421 wxwork/2.5.8 MicroMessenger/6.3.22 Language/zh']

        # 代理ip列表
        self.proxies_list = [{"HTTP": "139.196.140.179:8888"},{"HTTPS": "123.171.5.133:8118"},{"HTTP": "60.217.64.237:31923"},{"HTTP": "117.94.213.117:8118"},{"HTTPS": "222.95.144.38:3000"},{"HTTPS": "117.88.176.43:3000"},{"HTTPS": "125.73.220.18:31036"},{"HTTPS": "121.237.149.206:3000"},{"HTTPS": "117.88.176.126:3000"},{"HTTP": "222.95.144.71:3000"},{"HTTPS": "114.99.54.65:8118"},{"HTTP": "114.235.114.39:8118"},{"HTTP": "117.88.176.154:3000"},{"HTTP": "1.202.116.62:8118"},{"HTTPS": "222.95.144.70:3000"},{"HTTP": "121.237.148.63:3000"},{"HTTP": "121.237.148.85:3000"},{"HTTPS": "106.122.205.131:8118"},{"HTTP": "222.95.144.89:3000"},{"HTTP": "121.40.162.239:808"},{"HTTP": "183.163.207.197:8118"},{"HTTP": "118.78.196.142:8118"},{"HTTPS": "222.95.144.33:3000"},{"HTTPS": "121.237.149.200:3000"},{"HTTP": "222.95.144.87:3000"},{"HTTPS": "58.58.213.55:8888"},{"HTTPS": "121.237.149.243:3000"},{"HTTPS": "121.237.148.176:3000"},{"HTTP": "114.101.44.137:65309"},{"HTTP": "121.237.149.74:3000"},{"HTTP": "121.237.149.6:3000"},{"HTTPS": "121.237.148.212:3000"},{"HTTPS": "121.237.149.130:3000"},{"HTTPS": "175.8.108.109:8118"},{"HTTP": "120.78.168.189:8118"},{"HTTPS": "121.237.149.238:3000"},{"HTTP": "121.237.149.232:3000"},{"HTTP": "125.110.126.241:8118"},{"HTTPS": "222.95.144.170:3000"},{"HTTPS": "115.223.91.210:8010"},{"HTTP": "121.237.149.202:3000"},{"HTTP": "222.95.144.51:3000"},{"HTTP": "121.237.149.212:3000"},{"HTTP": "121.237.149.89:3000"},{"HTTP": "121.237.149.165:3000"},{"HTTPS": "121.237.149.28:3000"},{"HTTP": "124.200.36.118:40188"},{"HTTPS": "222.128.9.235:59593"},{"HTTP": "117.62.173.23:8118"},{"HTTPS": "110.73.4.196:8123"},{"HTTP": "118.181.226.166:44640"},{"HTTPS": "221.218.102.146:33323"},{"HTTPS": "218.249.45.162:35586"},{"HTTPS": "61.178.149.237:59042"},{"HTTP": "171.80.199.196:8118"},{"HTTP": "121.227.179.238:8118"},{"HTTP": "117.85.166.121:8118"},{"HTTPS": "58.254.220.116:52470"},{"HTTP": "140.143.53.70:8118"},{"HTTPS": "218.21.230.156:808"},{"HTTPS": "111.229.224.145:8118"},{"HTTP": "114.233.201.7:8118"},{"HTTPS": "222.94.148.166:808"},{"HTTP": "60.2.44.182:30963"},{"HTTPS": "119.254.94.93:46323"},{"HTTP": "118.114.165.98:8118"},{"HTTPS": "123.115.250.230:8118"},{"HTTP": "115.218.137.95:8118"},{"HTTP": "111.222.141.127:8118"},{"HTTP": "139.224.233.103:8118"},{"HTTP": "49.235.69.138:8118"},{"HTTP": "106.14.173.173:8080"},{"HTTP": "119.179.130.107:8060"},{"HTTPS": "221.206.100.133:34073"},{"HTTP": "220.173.143.242:808"},{"HTTPS": "121.237.149.75:3000"},{"HTTPS": "121.237.149.249:3000"},{"HTTP": "222.95.144.66:3000"},{"HTTP": "222.95.144.245:3000"},{"HTTPS": "175.148.68.177:1133"},{"HTTP": "117.88.176.213:3000"},{"HTTP": "117.88.176.111:3000"},{"HTTPS": "120.11.132.193:8118"},{"HTTPS": "218.21.96.128:58080"},{"HTTPS": "27.154.34.146:31527"},{"HTTP": "1.83.117.226:8118"},{"HTTP": "183.143.50.6:8118"},{"HTTPS": "171.221.66.26:8118"},{"HTTP": "27.42.168.46:48919"},{"HTTPS": "121.33.220.158:808"},{"HTTPS": "116.113.27.170:47849"},{"HTTPS": "59.172.27.6:53281"},{"HTTP": "121.237.149.188:3000"},{"HTTP": "115.223.77.240:8010"},{"HTTPS": "220.168.52.245:55255"},{"HTTP": "121.237.149.60:3000"},{"HTTP": "183.147.245.40:8118"},{"HTTP": "121.237.149.35:3000"},{"HTTPS": "115.219.168.249:8118"},{"HTTPS": "222.95.144.97:3000"}]


    # 按页数抓取数据
    def get_single_page(self,page,q):
        params = {
            'containerid': '100103type=61&q='+q+'&t=0',
            'sudaref':'m.weibo.cn',
            'display':0,
            'retcode':6102,
            'page_type':'searchall',
            'page':page
        }
        url = self.base_url + urlencode(params)
        try:
            proxies = random.choice(self.proxies_list)
            referer_params = {'type': '1&q=' + q}
            headers = {
                'Host': self.host,
                'Referer': 'https://m.weibo.cn/search?containerid=100103' + urlencode(referer_params),
                'User-Agent': random.choice(self.agent_list)
            }
            response = requests.get(url, headers=headers,proxies=proxies)
            print(proxies)
            print(headers)
            # exit()
            if response.status_code == 200:
                return response.json()
        except requests.ConnectionError as e:
            print('抓取错误', e.args)


    # 解析页面返回的json数据
    def parse_page(self,json):
        if json == None:
            # print('这条没有拿到数据，json为None')
            yield None
        else:
            items = json.get('data').get('cards')
            for item in items:
                item = item.get('mblog')

                if item:
                    data = {
                        'id': item.get('id'),
                        'text': pq(item.get("text")).text(),  # 仅提取内容中的文本
                        'attitudes': item.get('attitudes_count'),
                        'comments': item.get('comments_count'),
                        'reposts': item.get('reposts_count')
                    }
                    yield data


if __name__ == '__main__':
    weibo_spider = Weibo_Spider()
    q = '数据产品经理'

    ## start下面抓取微博关键词的实时数据内容
    # page = 1
    # while page < 1000:
    #     json = weibo_spider.get_single_page(page,q)
    #     results = weibo_spider.parse_page(json)
    #     for res in results:
    #         if res != None:
    #             file_path = q + '.txt'
    #             with open(file_path, 'a') as f:
    #                 for result in results:
    #                     # print(result)
    #                     # print(type(result))
    #
    #                     # print(result['text'])
    #                     f.write(result['text'])
    #                     f.write("\n")
    #
    #             print("第" + str(page) + "页保存成功")
    #             time.sleep(3)  # 休眠3秒
    #             page += 1
    #         else:
    #             print("第" + str(page) + "页没有拿到数据")
    #             playsound('/Users/mac/Music/music/2.mp3')
    #             time.sleep(3)  # 休眠3秒
    #
    # playsound('/Users/mac/Music/music/1.mp3')
    #
    # exit()

    ##end 抓取存储代码到这里结束

    # 下面设置词云分析
    with open(q + '.txt', "r") as f:  # 设置文件对象
        str = f.read()

    str = str.upper().replace(' ', '')
    # print(str)
    print(len(str))
    # exit()

    words = jieba.cut(str)
    # print(words)
    # exit()

    fnl_words = [word for word in words if len(word) > 1]  # 去掉单字
    # print(fnl_words)
    # exit()

    wc = wordcloud.WordCloud(width=1000, font_path='汉仪综艺体简.ttf', height=1000)  # 设定词云画的大小字体，一定要设定字体，否则中文显示不出来
    wc.generate(' '.join(fnl_words))

    plt.imshow(wc)  # 看图
    wc.to_file(q + ".jpg")  # 保存
    exit()



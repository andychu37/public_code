# -*- coding: utf-8 -*-
"""
    @Author Andy
    @Date 2020-03-27
    @Describe 根据关键词获取boos直聘的招聘信息
    @Version 1.0
"""
import requests
import json
import random
import time
from bs4 import BeautifulSoup
import xlwt
import pymysql
import jieba
import wordcloud
from matplotlib import pyplot as plt
from playsound import playsound


class job_detail():
    def __init__(self):
        self.base_url = "https://www.zhipin.com/job_detail/?query={}&city={}&industry={}&position={}&page={}"
        self.user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
]
        self.proxies_list = [{"HTTP": "139.196.140.179:8888"}, {"HTTPS": "123.171.5.133:8118"},
                         {"HTTP": "60.217.64.237:31923"}, {"HTTP": "117.94.213.117:8118"},
                         {"HTTPS": "222.95.144.38:3000"}, {"HTTPS": "117.88.176.43:3000"},
                         {"HTTPS": "125.73.220.18:31036"}, {"HTTPS": "121.237.149.206:3000"},
                         {"HTTPS": "117.88.176.126:3000"}, {"HTTP": "222.95.144.71:3000"},
                         {"HTTPS": "114.99.54.65:8118"}, {"HTTP": "114.235.114.39:8118"},
                         {"HTTP": "117.88.176.154:3000"}, {"HTTP": "1.202.116.62:8118"},
                         {"HTTPS": "222.95.144.70:3000"}, {"HTTP": "121.237.148.63:3000"},
                         {"HTTP": "121.237.148.85:3000"}, {"HTTPS": "106.122.205.131:8118"},
                         {"HTTP": "222.95.144.89:3000"}, {"HTTP": "121.40.162.239:808"},
                         {"HTTP": "183.163.207.197:8118"}, {"HTTP": "118.78.196.142:8118"},
                         {"HTTPS": "222.95.144.33:3000"}, {"HTTPS": "121.237.149.200:3000"},
                         {"HTTP": "222.95.144.87:3000"}, {"HTTPS": "58.58.213.55:8888"},
                         {"HTTPS": "121.237.149.243:3000"}, {"HTTPS": "121.237.148.176:3000"},
                         {"HTTP": "114.101.44.137:65309"}, {"HTTP": "121.237.149.74:3000"},
                         {"HTTP": "121.237.149.6:3000"}, {"HTTPS": "121.237.148.212:3000"},
                         {"HTTPS": "121.237.149.130:3000"}, {"HTTPS": "175.8.108.109:8118"},
                         {"HTTP": "120.78.168.189:8118"}, {"HTTPS": "121.237.149.238:3000"},
                         {"HTTP": "121.237.149.232:3000"}, {"HTTP": "125.110.126.241:8118"},
                         {"HTTPS": "222.95.144.170:3000"}, {"HTTPS": "115.223.91.210:8010"},
                         {"HTTP": "121.237.149.202:3000"}, {"HTTP": "222.95.144.51:3000"},
                         {"HTTP": "121.237.149.212:3000"}, {"HTTP": "121.237.149.89:3000"},
                         {"HTTP": "121.237.149.165:3000"}, {"HTTPS": "121.237.149.28:3000"},
                         {"HTTP": "124.200.36.118:40188"}, {"HTTPS": "222.128.9.235:59593"},
                         {"HTTP": "117.62.173.23:8118"}, {"HTTPS": "110.73.4.196:8123"},
                         {"HTTP": "118.181.226.166:44640"}, {"HTTPS": "221.218.102.146:33323"},
                         {"HTTPS": "218.249.45.162:35586"}, {"HTTPS": "61.178.149.237:59042"},
                         {"HTTP": "171.80.199.196:8118"}, {"HTTP": "121.227.179.238:8118"},
                         {"HTTP": "117.85.166.121:8118"}, {"HTTPS": "58.254.220.116:52470"},
                         {"HTTP": "140.143.53.70:8118"}, {"HTTPS": "218.21.230.156:808"},
                         {"HTTPS": "111.229.224.145:8118"}, {"HTTP": "114.233.201.7:8118"},
                         {"HTTPS": "222.94.148.166:808"}, {"HTTP": "60.2.44.182:30963"},
                         {"HTTPS": "119.254.94.93:46323"}, {"HTTP": "118.114.165.98:8118"},
                         {"HTTPS": "123.115.250.230:8118"}, {"HTTP": "115.218.137.95:8118"},
                         {"HTTP": "111.222.141.127:8118"}, {"HTTP": "139.224.233.103:8118"},
                         {"HTTP": "49.235.69.138:8118"}, {"HTTP": "106.14.173.173:8080"},
                         {"HTTP": "119.179.130.107:8060"}, {"HTTPS": "221.206.100.133:34073"},
                         {"HTTP": "220.173.143.242:808"}, {"HTTPS": "121.237.149.75:3000"},
                         {"HTTPS": "121.237.149.249:3000"}, {"HTTP": "222.95.144.66:3000"},
                         {"HTTP": "222.95.144.245:3000"}, {"HTTPS": "175.148.68.177:1133"},
                         {"HTTP": "117.88.176.213:3000"}, {"HTTP": "117.88.176.111:3000"},
                         {"HTTPS": "120.11.132.193:8118"}, {"HTTPS": "218.21.96.128:58080"},
                         {"HTTPS": "27.154.34.146:31527"}, {"HTTP": "1.83.117.226:8118"}, {"HTTP": "183.143.50.6:8118"},
                         {"HTTPS": "171.221.66.26:8118"}, {"HTTP": "27.42.168.46:48919"},
                         {"HTTPS": "121.33.220.158:808"}, {"HTTPS": "116.113.27.170:47849"},
                         {"HTTPS": "59.172.27.6:53281"}, {"HTTP": "121.237.149.188:3000"},
                         {"HTTP": "115.223.77.240:8010"}, {"HTTPS": "220.168.52.245:55255"},
                         {"HTTP": "121.237.149.60:3000"}, {"HTTP": "183.147.245.40:8118"},
                         {"HTTP": "121.237.149.35:3000"}, {"HTTPS": "115.219.168.249:8118"},
                         {"HTTPS": "222.95.144.97:3000"}]

    # 获取cookie,手动更新存在本地(因为访问boos直聘3页，cookie会变，需要需要js逆向破解，所以暂时下载页面到本地再匹配数据,)
    def get_cookie(self):
        cookie_res = open('./cookie.txt', 'r', encoding="utf-8")
        cookie = cookie_res.read()
        return cookie


    # 获取所有城市的编码
    def get_citysites(self):
        url = 'https://www.zhipin.com/wapi/zpCommon/data/city.json'
        res_json = requests.get(url)
        res = res_json.text
        res_dict = json.loads(res)
        with open('./citysites.json', 'w', encoding='utf-8') as f:
            json.dump(res_dict,f,ensure_ascii=False,indent=4)
        print('所有城市的编码成功获取并保存为citysites.json')

    # 获取指定城市的编码
    def get_city_code(self,city_name):
        # print(city_name)
        with open('./citysites.json','r') as f:
            contents = json.load(f)
        cityes = contents["zpData"]["cityList"]
        city_code = contents["zpData"]["locationCity"]["code"]
        # print(city_code)
        for city in cityes:
            for i in city['subLevelModelList']:
                if i['name'] == city_name:
                    city_code = i['code']
        # print(city_code)
        # exit()
        return city_code

    # 获取页面html,下载到本地（因为访问boos直聘3页，cookie会边，需要需要js逆向破解，所以暂时下载页面到本地再匹配数据）
    def get_html(self,city_name,query,page,url):

        print(url)

        headers = {
            'User-Agent': random.choice(self.user_agent_list),
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Host': 'www.zhipin.com',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': self.get_cookie()
        }
        proxies = random.choice(self.proxies_list)
        response = requests.get(url,headers = headers,proxies = proxies)
        res = response.text
        file_path = query+'/'+city_name + '_' + query + '_' + str(page)
        with open(file_path + '.html', "wb") as f:
            #   写文件用bytes而不是str，所以要转码
            f.write(res.encode())
        print('第'+str(page)+'页html保存成功')
        # return True


    # 获取html页面的数据内容

    def get_content(self,city_name, query, page,city_code):
        file_path = query + '/' + city_name + '_' + query + '_' + str(page)
        htmlf = open(file_path + '.html', 'r', encoding="utf-8")
        html = htmlf.read()
        bs = BeautifulSoup(html, 'lxml')
        # print(bs)
        # print(type(bs))
        # exit()

        contents = []
        i = 1
        for info in bs.find_all("div", "job-primary"):
            zhiwei_mingcheng = info.find("span","job-name").get_text()
            gongzuo_didian = info.find('span','job-area').get_text()
            company = info.find("div", "company-text").a.get_text()
            jid = info.find("div", "primary-box").get('data-jid')
            lid = info.find("div", "primary-box").get("data-lid")
            # 如果data-jid在a标签内，则用下面去获取
            # jid = info.find("div", "info-primary").a["data-jid"]
            # lid = info.find("div", "info-primary").a["data-lid"]

            tags1 = [text for text in info.find('div','tags').stripped_strings]
            tags = ' '.join(tags1)
            info_desc = info.find('div','info-desc').get_text()
            print(i)
            i += 1
            desc = self.get_job_desc(jid, lid)
            texts = [text for text in info.find("div", "info-primary").p.stripped_strings]
            salary = info.find("div", "job-limit").span.get_text()
            work_exp = texts[0] if len(texts) > 1 else None
            edu_bak = texts[1] if len(texts) > 1 else None
            companies = [text for text in info.find("div", "company-text").p.stripped_strings]
            industry = companies[0]
            if len(companies) > 2:
                finance = companies[1]
                staff_num = companies[2]
            else:
                finance = None
                staff_num = companies[1]
            search_name = query
            city_code = city_code
            contents.append(self.job_info(zhiwei_mingcheng,gongzuo_didian,company,jid,lid,salary,work_exp,edu_bak,industry,finance,staff_num,tags,info_desc,desc,search_name,city_code))
            # print(zhiwei_mingcheng)
            # print(gongzuo_didian)
            # print(company)
            # print(jid)
            # print(lid)
            # print(salary)
            # print(work_exp)
            # print(edu_bak)
            # print(industry)
            # print(finance)
            # print(staff_num)
            # print(tags)
            # print(info_desc)
            # exit()
            # print(contents)
            # exit()
            # time.sleep(3)
        # print(contents)
        # exit()
        return contents


    # 获取job详情内页的数据
    def get_job_desc(self,jid, lid):
        proxies = random.choice(self.proxies_list)
        headers = {
            'User-Agent': random.choice(self.user_agent_list),
        }

        url = "https://www.zhipin.com/wapi/zpgeek/view/job/card.json?jid={}&lid={}".format(jid, lid)
        print(url)
        print(headers)
        print(proxies)
        response = requests.get(url, headers=headers, proxies=proxies)
        html = json.loads(response.text)["zpData"]["html"]
        soup = BeautifulSoup(html, "lxml")
        desc = soup.find("div", "detail-bottom-text").get_text()
        return desc


    # 重新组合数据
    def job_info(self,zhiwei_mingcheng,gongzuo_didian,company,jid,lid,salary,work_exp,edu_bak,industry,finance,staff_num,tags,info_desc,desc,search_name,city_code):

        return {
            "zhiwei_mingcheng": zhiwei_mingcheng,
            "gongzuo_didian": gongzuo_didian,
            "company": company,
            "jid": jid,
            "lid": lid,
            "salary": salary,
            "work_exp": work_exp,
            "edu_bak": edu_bak,
            "industry": industry,
            "finance": finance,
            "staff_num": staff_num,
            "tags": tags,
            'info_desc':info_desc,
            'desc':desc,
            'search_name':search_name,
            'city_code':city_code
        }


    # 保存整合后的数据
    def save_data(self,page, content, city, query):
        file = xlwt.Workbook(encoding="utf-8", style_compression=0)
        sheet = file.add_sheet('数据分析', cell_overwrite_ok=True)
        sheet.write(0, 0, "职位名称")
        sheet.write(0, 1, "工作地点")
        sheet.write(0, 2, "公司名称")
        sheet.write(0, 3, "jid")
        sheet.write(0, 4, "lid")
        sheet.write(0, 5, "薪资")
        sheet.write(0, 6, "工作经验")
        sheet.write(0, 7, "学历要求")
        sheet.write(0, 8, "行业")
        sheet.write(0, 9, "融资情况")
        sheet.write(0, 10, "公司人数")
        sheet.write(0, 11, "职位吸引标签")
        sheet.write(0, 12, "福利")
        sheet.write(0, 13, "职位描述")
        sheet.write(0, 14, "search_name")
        sheet.write(0, 15, "city_code")
        for i in range(len(content)):
            sheet.write(i + 1, 0, content[i]["zhiwei_mingcheng"])
            sheet.write(i + 1, 1, content[i]["gongzuo_didian"])
            sheet.write(i + 1, 2, content[i]["company"])
            sheet.write(i + 1, 3, content[i]["jid"])
            sheet.write(i + 1, 4, content[i]["lid"])
            sheet.write(i + 1, 5, content[i]["salary"])
            sheet.write(i + 1, 6, content[i]["work_exp"])
            sheet.write(i + 1, 7, content[i]["edu_bak"])
            sheet.write(i + 1, 8, content[i]["industry"])
            sheet.write(i + 1, 9, content[i]["finance"])
            sheet.write(i + 1, 10, content[i]["staff_num"])
            sheet.write(i + 1, 11, content[i]["tags"])
            sheet.write(i + 1, 12, content[i]["info_desc"])
            sheet.write(i + 1, 13, content[i]["desc"])
            sheet.write(i + 1, 14, content[i]["search_name"])
            sheet.write(i + 1, 15, content[i]["city_code"])
        file.save(r'{}_{}_{}.xls'.format(city, query, page))



    # 读取mysql的job描述数据，存入到txtw文件
    def get_mysqldata(self,query,wordcloud_name):

        # 打开数据库连接
        db = pymysql.connect("localhost", "andy", "andychu37", "boos_zhipin", charset='utf8')

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # wordcloud_name = 'search_name'

        # SQL 查询语句
        sql = "SELECT "+wordcloud_name+" FROM 数据分析 where search_name ='"+query+"' "
        # print(sql)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            # print(results)
            # print(type(results))
            # exit()

            fp = open(query+'_'+wordcloud_name+'.txt', "w")
            loan_count = 0
            for loanNumber in results:
                # print(loanNumber)
                if loanNumber[0] != None:

                    # print(loanNumber[0])
                    loan_count += 1
                    fp.write(loanNumber[0] + "\n")
            fp.close()
            print(query+'_'+wordcloud_name+'.txt保存成功')


            exit()


        except:
            print
            "Error: unable to fecth data"

        # 关闭数据库连接
        db.close()


    # 生成词云
    def get_wordcloud(self,wordcloud_name):
        # 下面设置词云分析
        with open(wordcloud_name + '.txt', "r") as f:  # 设置文件对象
            str = f.read()

        str = str.upper().replace('\n', '')
        str = str.upper().replace(' ', '')
        # print(str)
        print(len(str))
        # exit()

        words = jieba.cut(str)
        # print(words)
        # exit()
        # fnl_words = [word for word in words if len(word) > 1]  # 去掉单字

        fnl_words = words
        # print(fnl_words)
        # exit()

        wc = wordcloud.WordCloud(width=1000, font_path='汉仪综艺体简.ttf', height=1000)  # 设定词云画的大小字体，一定要设定字体，否则中文显示不出来
        wc.generate(' '.join(fnl_words))

        plt.imshow(wc)  # 看图
        wc.to_file(wordcloud_name + ".jpg")  # 保存
        exit()


    def run(self):
        pass




if __name__ == '__main__':
    job_detail_spider = job_detail()
    # 输入城市名
    city_name = '杭州'
    # 获取城市code
    city_code = job_detail_spider.get_city_code(city_name)
    # 输入搜索的岗位关键词
    query = 'python'
    # 默认搜索为第一页
    page = 1
    industry = ''
    position = ''
    base_url = "https://www.zhipin.com/job_detail/?query={}&city={}&industry={}&position={}&page={}"
    # urls = []
    url = base_url.format(query, city_code, industry, position, page)
    while page < 16:
        # 下载html页面到本地
        url = base_url.format(query, city_code, industry, position, page)
        html_res = job_detail_spider.get_html(city_name, query, page, url)
        # exit()

        # 获取html页面的数据，重新整合
        content = job_detail_spider.get_content(city_name, query, page,city_code)
        content += content
        job_detail_spider.save_data(page,content, city_name, query)
        print('第' + str(page) + '页数据成功保存为xls文件')

        page += 1

    playsound('/Users/mac/Music/music/1.mp3')
    exit()

    wordcloud_name = '职位描述'
    job_detail_spider.get_mysqldata(query,wordcloud_name)
    # time.sleep(5)

    wordcloud_name = query+'_'+wordcloud_name
    job_detail_spider.get_wordcloud(wordcloud_name)

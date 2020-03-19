import requests
import rsa
import time
import random
import urllib3
import base64
import dao
from dao import table_exists
from dao import  create_table
import re
import dealHTML
from user_agents import agents
from urllib.parse import quote
from binascii import b2a_hex
urllib3.disable_warnings() # 取消警告


def get_timestamp():
    return int(time.time()*1000)  # 获取13位时间戳

class Spider():
    def __init__(self,username,password,topic):
        self.username = username
        self.password = password
        self.session = requests.session() #登录用session
        self.session.headers = {
            'User-Agent':  "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9"
        }
        self.session.verify = False  # 取消证书验证
        self.now_user = 0
        self.now_url = ''  # 记录当前访问的url
        self.now_topic = 0
        self.now_page = 1 #记录当前页面
        self.topic = topic

    def prelogin(self):
        '''预登录，获取一些必须的参数'''
        self.su = base64.b64encode(self.username.encode())  #阅读js得知用户名进行base64转码
        url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su={}&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_={}'.format(quote(self.su),get_timestamp()) #注意su要进行quote转码
        response = self.session.get(url).content.decode()
        # print(response)
        # 要想登录，就得获取nonce的值，而要获取nonce的值，就要先请求这个找到的请求
        self.nonce = re.findall(r'"nonce":"(.*?)"',response)[0]
        self.pubkey = re.findall(r'"pubkey":"(.*?)"',response)[0]
        self.rsakv = re.findall(r'"rsakv":"(.*?)"',response)[0]
        self.servertime = re.findall(r'"servertime":(.*?),',response)[0]
        return self.nonce,self.pubkey,self.rsakv,self.servertime

    def get_sp(self):
        '''用rsa对明文密码进行加密，加密规则通过阅读js代码得知'''
        publickey = rsa.PublicKey(int(self.pubkey,16),int('10001',16))
        message = str(self.servertime) + '\t' + str(self.nonce) + '\n' + str(self.password)
        self.sp = rsa.encrypt(message.encode(),publickey)
        return b2a_hex(self.sp)

    def login(self):
            '''
            登录
            :return:
            '''
            url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
            data = {
            'entry': 'weibo',
            'gateway': '1',
            'from':'',
            'savestate': '7',
            'qrcode_flag': 'false',
            'useticket': '1',
            'pagerefer': 'https://login.sina.com.cn/crossdomain2.php?action=login&r=https%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
            'vsnf': '1',
            'su': self.su,
            'service': 'miniblog',
            'servertime': str(int(self.servertime)+random.randint(1,20)),
            'nonce': self.nonce,
            'pwencode': 'rsa2',
            'rsakv': self.rsakv,
            'sp': self.get_sp(),
            'sr': '1536 * 864',
            'encoding': 'UTF - 8',
            'prelt': '35',
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META',
            }
            response = self.session.post(url,data=data,allow_redirects=False).text # 提交账号密码等参数
            redirect_url = re.findall(r'location.replace\("(.*?)"\);',response)[0] # 微博在提交数据后会跳转，此处获取跳转的url
            result = self.session.get(redirect_url,allow_redirects=False).text  # 请求跳转页面
            ticket,ssosavestate = re.findall(r'ticket=(.*?)&ssosavestate=(.*?)"',result)[0] #获取ticket和ssosavestate参数
            
            uid_url = 'https://passport.weibo.com/wbsso/login?ticket={}&ssosavestate={}&callback=sinaSSOController.doCrossDomainCallBack&scriptId=ssoscript0&client=ssologin.js(v1.4.19)&_={}'.format(ticket,ssosavestate,get_timestamp())
            data = self.session.get(uid_url).text #请求获取uid
            uid = re.findall(r'"uniqueid":"(.*?)"',data)[0]
            print(uid)
            home_url = 'https://weibo.com/u/{}/home?wvr=5&lf=reg'.format(uid) #请求首页
            html = self.session.get(home_url)
            # self.session.cookies.save()
            html.encoding = 'utf-8'
            # print(html.text)
            print('*******************************登录成功！********************************')
        
    def Myspider(self,keyword,page):
        '''
        负责爬取网页
        :param page: 爬取页面
        :return: 爬取网页
        '''
        try:
            self.now_url = f'https://s.weibo.com/weibo/{keyword}?topnav=1&wvr=6&b={page}'
            print("******************************当前页面为*********************************")
            print(self.now_url)
            print("************************************************************************"+'第'+str(self.now_page)+"页")
            time.sleep(1)
            nowhtml = self.session.get(self.now_url)
            nowhtml.encoding = 'utf-8'
            print(nowhtml.status_code)
            if nowhtml.status_code != 200:
                print('*******************************爬取失败！，休息休息********************************')
                time.sleep(60)
            # print(nowhtml.text)
            # with open('html.txt', 'w', encoding='utf-8') as f:
            #     f.write(myhtml.text)
            return nowhtml.text
        except:
            print('出错！休息休息，重新登录！')
            time.sleep(30)
            self.main()

    def ctrl_spider(self):
        '''
        控制爬虫
        :return:
        '''
        #爬虫关键词和页面
        # for kw in range(0,len(keyword)):
        my_page = 0

        # if (table_exists(keywordDb[self.topic]) != 1):
        #     print("表不存在，建表")
        #     create_table(keywordDb[self.topic])
        while( 1 ):
            # 如果数据库内容没有20000，继续爬取，要频繁访问数据库，需要优化
            if dao.total(keywordDb[self.topic]) < 20000:

                # html = self.Myspider(keyword[kw], p+1)
                html = self.Myspider(keyword[self.topic], self.now_page)
                print("******************************爬取成功！*********************************")
                content = dealHTML.deal_html(html)
                self.preserve(content)
                time.sleep(random.random()*3)
                time.sleep(3)
                self.now_page += 1
                if self.now_page  == 200:
                    time.sleep(3)
                    self.now_page = 1
                # if self.now_page == 51:
                #     self.now_page = 1
                #     my_page += 1
                # #每20个50页循环换一次帐号和请求头
                # if (my_page != 0)and (my_page % 20) == 0:
                #     self.now_user += 1
                #     self.password = passwords[(self.now_user)%2]
                #     self.username = usernames[(self.now_user)%2]
                #     self.session.headers = {
                #         'User-Agent': agents[random.randint(0, 50)]
                #     }
                #     self.prelogin()
                #     self.get_sp()
                #     self.login()
                #     print("****************************切换账号和请求头*************************"+'\n'+"当前帐号：    "+self.username)

                #一百页换一次请求头和帐号
                # if page%100==0:
                #     headers = {
                #         'User-Agent': agents[random.randint(0,60)]
                #     }
                #     self.session.headers = headers
                #     self.now_user+= 1
                #     self.username = usernames[self.now_user]
                #     self.password = passwords[self.now_user]
                #     print("更换帐号和密码，当前帐号和密码：")
                #     print(self.username,self.password)
                #     self.prelogin()
                #     self.get_sp()
                #     self.login()
            # kw+=1
            # self.now_topic = kw
            else:
                break
        #关闭数据库
        dao.closeDB()

    def preserve(self,content):
        '''
        保存数据到mysql数据库
        :param content: 要保存的内容
        :return:
        '''
        # dao.create_table(keyword[self.now_topic])
        # if self.now_page == 1:
        #     dao.create_table(keywordDb[self.topic])
        for cont in range(0,len(content)):
            user = eval(content[cont][0])
            dao.insert(keywordDb[self.topic],user,content[cont][1])
            cont += 1

    def main(self):

        #登录
        self.prelogin()
        self.get_sp()
        self.login()
        #控制爬虫爬取页面
        self.ctrl_spider()

if __name__ == '__main__':
    usernames = ['1272769209@qq.com',
                 '349155081@qq.com',
                 '434355330@qq.com',
                 '1156903009@qq.com',
                 '1757224427@qq.com',
                 '1757286043@qq.com',
                 '1273340877@qq.com',
                 '1244171637@qq.com',
                 '1173856486@qq.com',
                 '1272817710@qq.com']
    
    passwords = ['1272769209',
                 '349155081',
                 'qq434355330',
                 'qq1156903009',
                 '1757224427',
                 '1757286043',
                 '1273340877',
                 'qq1244171637',
                 'qq1173856486',
                 '1272817710']
    # 关键词 可自定义
    keyword = ('健康', '湖北科技学院', '5G', '中美贸易战', '垃圾分类', '教育', '医疗', '大学生', '人工智能')
    # 对应的数据库表名 可自定义
    keywordDb = ('healthy', 'hbust', 'fiveG', 'CHINA_USA', 'Classification', 'education', 'medical', 'CollegeStudents', 'AI')
    #启动爬虫
    spider = Spider(usernames[0], passwords[0], 0)
    spider.main()





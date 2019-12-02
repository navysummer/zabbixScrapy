# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from lxml import etree

class Zabbix(object):
    """docstring for Zabbix"""
    def __init__(self, url,user,password):
        super(Zabbix, self).__init__()
        self.url = url
        self.user = user
        self.password = password
        self.zbx_sessionid = None
        self.PHPSESSID = None
        self.sid = None
        __login_status = self.___login()
        if not __login_status:
            raise Exception("login fail")
    def ___login(self):
        login_headers = {
            "Referer":self.url,
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }
        login_data = {
            "name": self.user,
            "password": self.password,
            "autologin":"1",
            "enter": "Sign in"
        }
        login_url = self.url + "/index.php"
        r = requests.post(login_url,data=login_data,headers=login_headers)
        cookies = r.cookies.get_dict()
        if not cookies:
            raise Exception('login fail')
        self.PHPSESSID = cookies['PHPSESSID']
        self.zbx_sessionid = cookies['zbx_sessionid']
        html_doc = r.text.encode("gbk", 'ignore').decode("gbk", "ignore")
        soup = BeautifulSoup(html_doc, 'html.parser')
        title = soup.find('title').get_text()
        if "Content-Length" in r.headers or title == 'Zabbix':
            return False
        else:
            self.sid = soup.find('a',class_='top-nav-signout').attrs['onclick'].split("'")[1].split('&')[1].split('=')[1]
            return True

    def getSession(self):
        session = {
            'PHPSESSID':self.PHPSESSID,
            'zbx_sessionid':self.zbx_sessionid
        }
        return session

    def ___logout(self):
        if self.zbx_sessionid is None:
            raise Exception('logout fail')
        if self.sid is None:
            raise Exception('logout fail')
        logout_url = self.url + "/index.php?reconnect=1"
        logout_data = {
            "sid":self.sid
        }
        requests.post(logout_url,logout_data)
        
    def getData(self,url,xpath_str):
        if not self.PHPSESSID or not self.zbx_sessionid:
            raise Exception('login fail')
        headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Sec-Fetch-Mode":"navigate",
            "Sec-Fetch-Site":"none",
            "Sec-Fetch-User":"?1",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Cookie":"PHPSESSID="+self.PHPSESSID+"; zbx_sessionid="+self.zbx_sessionid
        }
        r = requests.get(url,headers=headers)
        html_doc = r.text
        #print(html_doc)
        tree = etree.HTML(html_doc)
        data = tree.xpath(xpath_str)
        self.___logout()
        return data




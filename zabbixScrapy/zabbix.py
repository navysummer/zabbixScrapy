# -*- coding: UTF-8 -*-
import requests
from lxml import etree

class Zabbix(object):
    """docstring for Zabbix"""
    def __init__(self, url,user,password):
        super(Zabbix, self).__init__()
        self.url = url
        self.user = user
        self.password = password
        self.cookies = None
        self.zbx_sessionid = None
        self.PHPSESSID = None
        self.sid = None
        self.___login()
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
        if 'PHPSESSID' not in cookies:
            raise Exception('login fail')
        if 'zbx_sessionid' not in cookies:
            raise Exception('login fail')
        self.cookies = cookies
        self.PHPSESSID = cookies['PHPSESSID']
        self.zbx_sessionid = cookies['zbx_sessionid']
        html_doc = r.text.encode("gbk", 'ignore').decode("gbk", "ignore")
        tree = etree.HTML(html_doc)
        xpath_str = "(//input[@id='sid'])[1]/@value"
        sid = tree.xpath(xpath_str)
        if not sid:
            raise Exception('login fail')
        self.sid = sid[0]

    def getSession(self):
        session = {
            'PHPSESSID':self.PHPSESSID,
            'zbx_sessionid':self.zbx_sessionid,
            'sid':self.sid
        }
        return session

    def ___logout(self):
        if self.sid is None:
            raise Exception('login fail')
        logout_url = self.url + "/index.php?reconnect=1"
        logout_data = {
            "sid":self.sid
        }
        requests.post(logout_url,logout_data)
        
    def getData(self,url,xpath_str):
        if not self.cookies:
            raise Exception('login fail')
        r = requests.get(url,cookies=self.cookies)
        html_doc = r.text
        tree = etree.HTML(html_doc)
        data = tree.xpath(xpath_str)
        self.___logout()
        return data




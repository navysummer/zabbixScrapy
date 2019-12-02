# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from lxml import etree
from urllib.parse import urlparse,parse_qs

class Zabbix(object):
    """docstring for Zabbix"""
    def __init__(self, url,user,password):
        super(Zabbix, self).__init__()
        self.url = url
        self.user = user
        self.password = password
        self.cookies = None
        self.sid = None
        self.zbx_sessionid = None
        self.PHPSESSID = None
        self.apikey = None
        self.___login()

    def ___login(self):
        self.urlinfo = urlparse(self.url)
        Host = self.urlinfo.netloc
        scheme = self.urlinfo.scheme
        path = self.urlinfo.path
        params = self.urlinfo.params
        querys = self.urlinfo.query
        queryDict = parse_qs(querys)
        self.apikey = queryDict['apikey'][0]
        fragment = self.urlinfo.fragment
        login_headers = {
            "Host":Host,
            "Referer":self.url,
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }
        login_data = {
            "name": self.user,
            "password": self.password,
            "autologin":"1",
            "enter": "Sign in"
        }
        login_url = scheme + "://" + Host + path + "index.php"
        r = requests.post(login_url,data=login_data,headers=login_headers,allow_redirects=False)
        cookies = r.cookies.get_dict()
        if not cookies:
            raise Exception('login fail')
        cookies.update({'apikey':self.apikey})
        if 'zbx_sessionid' not in cookies:
            raise Exception('login fail')
        self.zbx_sessionid = cookies['zbx_sessionid']
        self.cookies = cookies
        res = requests.get(login_url,cookies=cookies)
        new_cookies = res.cookies.get_dict()
        if 'PHPSESSID' not in new_cookies:
            raise Exception('login fail')
        self.PHPSESSID = new_cookies['PHPSESSID']
        html_doc = res.text.encode("gbk", 'ignore').decode("gbk", "ignore")
        soup = BeautifulSoup(html_doc, 'html.parser')
        sid = soup.find('input',id='sid')
        if not sid:
            raise Exception('login fail')
        self.sid = sid.attrs['value']

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
        Host = self.urlinfo.netloc
        scheme = self.urlinfo.scheme
        path = self.urlinfo.path
        logout_url = scheme + "://" + Host + path + "index.php?reconnect=1"
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


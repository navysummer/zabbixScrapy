from zabbixScrapy import Zabbix


login_url = 'http://localhost:204/zabbix'
user = 'Admin'
pwd = 'TWrFlMnJFraqY3gG'
zabbix = Zabbix(login_url,user,pwd)
session = zabbix.getSession()
print(session)
url = 'http://localhost:204/zabbix/zabbix.php?action=dashboard.view'
xpath = '//title/text()'
data = zabbix.getData(url,xpath)
print(data)




from zabbixScrapy import ZabbixKey
login_url = 'http://localhost:204/system/06e3c7b31e3f4a5da36ad31f56a5ab54/?apikey=key_1c7a25dc606542ba9a7adce4c9ca5ec2'
user = 'Admin'
pwd = 'TWrFlMnJFraqY3gG'
zabbix = ZabbixKey(login_url,user,pwd)
session = zabbix.getSession()
print(session)
url = 'http://localhost:204/system/06e3c7b31e3f4a5da36ad31f56a5ab54/zabbix.php?action=dashboard.view'
xpath = '//title/text()'
data = zabbix.getData(url,xpath)
print(data)




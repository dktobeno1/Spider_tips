from selenium import webdriver
import re,time
from bs4 import BeautifulSoup
import json

def get_gd(name_company):
    my_driver = webdriver.PhantomJS()
    url_first = r'http://www.tianyancha.com/search?key=%s&checkFrom=searchBox'%name_company
    my_driver.get(url_first)
    time.sleep(15)
    content_first = my_driver.page_source
    pattern = re.compile(r'href="http://www.tianyancha.com/company/(.+?)"')
    list_id = re.findall(pattern,content_first)
    url_info = r'http://www.tianyancha.com/company/%s'%list_id[0]
    url_gd = r'http://www.tianyancha.com/expanse/changeinfo.json?id=%s&ps=5&pn=2'%list_id[0]
    my_driver.get(url_info)
    time.sleep(10)
    content_info = my_driver.page_source
    #print(content_info)
    my_driver.close()
    soup = BeautifulSoup(content_info,'lxml')
    print('公司股东：')
    for a in soup.findAll('a',{"event-name":"company-detail-investment"}):
        #print(a)
        print(a.string)
    
    


if __name__ == '__main__':
    name = input('请输入需要查询的公司名：')
    name = str(name.encode('utf-8')).replace(r'\x',r'%').upper()
    name = name.split(r"'")[1]
    #print(name)
    get_gd(name)

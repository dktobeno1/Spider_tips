from selenium import webdriver
import re,time
name_company = input('请输入需要查询的公司名：')
my_driver = webdriver.PhantomJS()
url_first = r'http://www.tianyancha.com/search?key=%s&checkFrom=searchBox'%name_company
url_second = r'http://www.tianyancha.com/company/9519792'
url_third = r'http://www.tianyancha.com/v2/search/%s.json?'%name_company
url_forth = r'http://www.tianyancha.com/expanse/changeinfo.json?id=9519792&ps=5&pn=2'
url_fifth = r'http://www.tianyancha.com/newest/56.json'
my_driver.get(url_first)
time.sleep(15)
content_gd = my_driver.page_source
print(content_gd)
my_driver.close()

pattern = re.compile(r'href="(http://www.tianyancha.com/company/.+?)"')
#pattern_test = re.compile(r'9519792')

list_id = re.findall(pattern,content_gd)
print(list_id)
#my_driver.page_source是字符串类型

import re,requests,time,mysql.connector
from bs4 import BeautifulSoup

def worker():
    conn = mysql.connector.connect(user = 'root',password = '',database = 'poetry')
    cursor = conn.cursor()
    url_info = 'http://www.zgshige.com/mrhs/index_4.shtml'
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
               'Connection': 'keep-alive',
               'Host': 'www.zgshige.com'
            }
    results_info = requests.get(url_info, headers = headers, timeout = 60)
    results_info.encoding = 'utf-8'
    soup = BeautifulSoup(results_info.text, 'lxml')
    #print(soup.prettify())
    #list_name = soup.findAll(href = re.compile(r'^/c/.+?\.shtml'))
    list_f = list(soup.select('h4 > a'))
    list_tag = list_f[:-1]
    #print(list_tag)
    for a in list_tag:
        url = 'http://www.zgshige.com'+a['href']
        result_content = requests.get(url, headers = headers, timeout = 30)
        result_content.encoding = 'utf-8'
        soup_content = BeautifulSoup(result_content.text, 'lxml')
        name = str(soup_content.h3.string)
        #print(name)
        #author = list(soup_content.findAll('p',{'id':'ArticleUserName'}))[0].string
        #print(author)
        
        span_date = list(soup_content.findAll('span',{'class':'p-l-sm p-r-sm'}))[0]
        date = str(span_date.string)
        author = str(span_date.previous_sibling.string)
        #print(date,author)
        
        list_content = list(soup_content.findAll('section',{'style':re.compile('text-align: .+?; font-size: .+? box-sizing: border-box;')}))
        print(len(list_content))
        if len(list_content) >= 2:
            content = str(list_content[0])
            recommend = str(list_content[1])
            cursor.execute('insert into dailypoetry (name,date,author,content,recommend,url) values (%s,%s,%s,%s,%s,%s)',[name,date,author,content,recommend,url])
        else:
            cursor.execute('insert into dailypoetry (name,date,author,url) values (%s,%s,%s,%s)',[name,date,author,url])
        print('%s导入数据库'% name)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    worker()

# -*- coding: utf-8 -*-

import gzip,re,requests,time,random
from multiprocessing import Pool
import mysql.connector

#def ungzip(data):
   # try:        # 尝试解压
       # print('正在解压.....')
       # data = gzip.decompress(data)
        #print('解压完毕!')
   # except:
      #  print('未经压缩, 无需解压')
  #  return data
	
#@asyncio.coroutine
#def test(name,types,num,court,dates,url,docid,proced,cause,area,yiju,content):
#    p=panjueshu(name=name,cause=cause,docid=docid,area=area,proced=proced,types=types,num=num,court=court,dates=dates,yiju=yiju,content=content,url=url)
#    yield from p.save()
def randHeader():  # 随机获取headers头
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    header = [
        {
            'Host': 'wenshu.court.gov.cn',
            'User-Agent': random.choice(head_user_agent),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive'},
        {
            'Host': 'wenshu.court.gov.cn',
            'User-Agent': random.choice(head_user_agent),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'}
    ]
    return header

def get_ips():
    list_ip = ['125.88.74.122:81',
               '183.95.80.165:8080',
               '59.37.160.57:8081',
               '124.133.230.254:80',
               '183.78.183.156:82',
               '124.88.67.83:843',
               '42.81.58.199:80',
               '124.88.67.9:80',
               '180.167.34.187:80',
               '183.78.183.156:82',
               '125.88.74.122:85',
               '124.88.67.22:83',
               '14.152.93.79:8080',
               '120.9.13.2:8888',
               '182.38.36.42:8998',
               '122.96.59.98:82',
               '117.95.19.112:8998',
               '14.127.200.59:8081',
               '221.3.6.2:8081',
               '182.112.128.115:80',
               '124.88.67.9:843',
               '171.8.79.143:8080',
               '183.57.249.97:8081',
               '180.136.83.16:8998',
               '220.174.236.211:80',
               '124.88.67.17:83',
               '124.88.67.54:82',
               '42.81.58.199:80',
               '183.165.150.216:8998'
               ]
    return list_ip
def worker(que):
    qishi = (que.get()-1)*20+1
    jieshu = qishi+19
    proxy_ip = {}
    ip_time = 0
    s = Queue.Queue(10)  # 案件数目请求未成功队列
    conn = mysql.connector.connect(user="root", password="password", database="caipan")
    cursor = conn.cursor()
    the_url = 'http://wenshu.court.gov.cn/List/ListContent'
    index = qishi-1
    try_j = 0
    while True:
        if not s.empty():
            index = s.get()
            try_j += 1
            if 2 <= try_j <= 3:
                time.sleep(3)
            elif 4 <= try_j <=5:
                time.sleep(6)
            elif try_j == 6:
                time.sleep(10)
            elif try_j == 7:
                time.sleep(20)
            elif try_j >=8:
                try_j = 0
        else:
            index += 1
            if index > jieshu:
                print('>>>>>>>>>>>>> %s -- %s 页文书已抓取完成  <<<<<<<<<<<<<<'% (qishi,jieshu))
                break
                
        try:
            data={'Param':'裁判年份:2016',
            'Page':'20',
            'Order':'法院层级',
            'Index':str(index),
            'Direction':'asc'

            }
            headers = randHeader()
            
            if (int(time.time())-ip_time) > 60 or not proxy_ip:
                proxy_ip={'http':'http://%s'%random.choice(get_ips)}
                ip_time=int(time.time())
            print(index)
            resp=requests.post(the_url,data = data,headers = headers[0],proxies=proxy_ip,timeout=60)
            respons=resp.text
            pattern=re.compile(r'{\\"裁判要旨段原文\\":\\"(.*?)\\",\\"案件类型\\":\\"(.*?)\\",\\"裁判日期\\":\\"(.*?)\\",\\"案件名称\\":\\"(.*?)\\",\\"文书ID\\":\\"(.*?)\\",\\"审判程序\\":\\"(.*?)\\",\\"案号\\":\\"(.*?)\\",\\"法院名称\\":\\"(.*?)\\"}')
            list_info = re.findall(pattern,respons)
            for info in list_info:
                yiju = info[0]
                type = info[1]
                date = info[2]
                name = info[3]
                docid = info[4]
                produce = info[5]
                num = info[6]
                court = info[7]
                url='http://wenshu.court.gov.cn/content/content?DocID=%s'%info[4]
                #url_content = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=%s'%info
                #resp_content=requests.get(url_content).text
                #loop.run_until_complete(test(name,types,num,court,dates,url,docid,proced))
                cursor.execute('insert into panjueshu (name,docid,proced,types,url,num,court,dates,cause) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', [name,docid,proced,types,url,num,court,dates,cause])
                conn.commit()
        #print(self.count)

if __name__=='__main__':
    #loop = asyncio.get_event_loop()
    p=Pool(4)
    #print(1)
    for i in range(1,7):
        p.apply_async(duoye_1,args=(i*10+1,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')


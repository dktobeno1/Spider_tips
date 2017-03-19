from urllib import request
import re,random
def hebing(t):
        b=':'.join(t)
        return b
def get_ip():
    
    url_top=r'http://www.xicidaili.com/nt/1'
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
    req=request.Request(url_top,headers=headers)
    resp=request.urlopen(req).read().decode('utf-8')
    #print(resp)
    pattern=re.compile(r'<td>(\d+?\.\d+?\.\d+?\.\d+?)</td>\s+?<td>(\d+?)</td>')
    list_ip=re.findall(pattern,resp)
    #print(list_ip)
    list_ip_final=list(map(hebing,list_ip))
    #print(list_ip_final)
    return list_ip_final


if __name__=='__main__':
    print(get_ip())
#dailiip=random.choice(get_ip())
#proxy_support=request.ProxyHandler({'http':dailiip})
#opener = request.build_opener(proxy_support)
#request.install_opener(opener)
#a = request.urlopen('http://www.111cn.net').read().decode("utf8") 
#print(a)

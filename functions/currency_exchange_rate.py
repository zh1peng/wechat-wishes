# install BeautifulSoup4
from bs4 import BeautifulSoup
import re, requests, sys, os

def get_exchange_rate(currency):
    url = 'http://www.boc.cn/sourcedb/whpj/index.html'  # 网址
    html = requests.get(url).content.decode('utf8')  # 获取网页源码（中间涉及到编码问题,这是个大坑，你得自己摸索）
    try:
    # 方式一：正则匹配
        a = html.index('<td>%s</td>' %currency)  # 
        s = html[a:a + 300]  # 截取新西兰元汇率那部分内容（从a到a+300位置）
        result = re.findall('<td>(.*?)</td>', s)  # 正则获取
        
        result_msg='现汇买入价：' + result[1] + '\n'
        result_msg=result_msg+'现钞买入价：' + result[2] + '\n'
        result_msg=result_msg+'现汇卖出价：' + result[3] + '\n'
        result_msg=result_msg+'现钞卖出价：' + result[4] + '\n'
        result_msg=result_msg+'中行折算价：' + result[5] + '\n'
    except:
        result_msg='你是说火星币？'
        print(result_msg)
    return result_msg

from BeautifulSoup import BeautifulSoup
import re, urllib, sys, os
def getweb(url):
    f = urllib.urlopen(url)
    data =f.read()
    f.close()
    return data
url = 'http://www.boc.cn/sourcedb/whpj/'
content = getweb(url)
soup = BeautifulSoup(''.join(content))
table_p   = soup.findAll('td', width="86")
name    = []
price   = []
date    = []
title   = []
pattern = re.compile('<[^<]*>',re.UNICODE)
for i in range(len(table_p)):
  if (i % 8) == 0:
    s1 = re.sub(pattern,'',unicode(str(table_p[i]),'utf-8'))
    if i == 0:
      title.append(s1)
    else:
      name.append(s1) 
  if (i % 8) == 1:
    s2 = re.sub(pattern ,'',unicode(str(table_p[i]),'utf-8'))
    if i == 1:
      title.append(s2)
    else:
      price.append(s2)
  if (i % 8) == 6:
    s3 = re.sub(pattern,'',unicode(str(table_p[i]),'utf-8'))    
    if i == 6:
      title.append(s3)
    else:
      date.append(s3)

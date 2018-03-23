
import datetime
import time
s = input('Enter learning date (YYYY/MM/DD) or Hit enter for "'"today"'": ')
if s=='':
    s=time.strftime("%Y/%m/%d")
print('Dates to review are: ')
for n in [1, 2, 4, 7, 15]:
    d = datetime.datetime.strptime(s, '%Y/%m/%d') + datetime.timedelta(days=n)
    print(d.strftime('%Y/%m/%d'))
time.sleep(60)

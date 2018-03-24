
# print review time
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


# thread1
import datetime
import time
def attach_review_time(msg):
    now = datetime.datetime.now()
    #20min, 1hour, 8~9hour 1days 2days 6days 15days
    review_times=[]
    review_dic={}
    for review_time in [20, 60, 480,1440,2880,8640,21600]:
        tmp = now + datetime.timedelta(minutes = review_time)
        review_times.append(tmp.strftime("%Y%m%d%H%M%S"))
        review_dic[tmp.strftime("%Y%m%d%H%M%S")]=msg
    return review_dic
time.sleep()
review_dic=attach_review_time(msg)  
all2review={}
all2review.update(a)

# Thread 2
def thread2(send2review)
while True: 
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if now in all2review:
        print(all2review[now])

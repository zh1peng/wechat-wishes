import requests
import itchat
from urllib import request, parse
import json
import time

KEY = '143da4e9713c42bca81b079cc0ff4d2f'

def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:       
        return

def get_realtime(stop_id):
    if isinstance(stop_id,int):
        stop_id=str(stop_id)
    base_url='https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?'
    url2use=base_url+'stopid='+stop_id
    req = request.Request(url2use)
    response = request.urlopen(req)
    result = response.read().decode('utf-8')
    result_json = json.loads(result)
    result_list=result_json['results']
    bus_list=[i['route'] for i in result_list]
    due_time=[i['duetime'] for i in result_list]
    msg=time.strftime('%H:%M:%S',time.gmtime())
    for routi,timei in zip(bus_list,due_time):
        msg=msg+'\nRoute:%s---Duetime: %s' %(routi,timei)
    return msg
# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    defaultReply = 'I received: ' + msg['Text']
    if msg.startswith('bus'):
        stop_id=msg[3:]
        reply=get_realtime(stop_id)
    else:
        reply = get_response(msg['Text'])
    return reply or defaultReply

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login(enableCmdQR=2)
itchat.run()

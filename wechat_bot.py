import requests
import itchat
from urllib import request, parse
import json
import time

KEY = '143da4e9713c42bca81b079cc0ff4d2f'

def tuling_response(msg):
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
    bus_info=time.strftime('%H:%M:%S',time.gmtime())
    for routi,timei in zip(bus_list,due_time):
        bus_info=bus_info+'\nRoute:%s---Duetime: %s' %(routi,timei)
    return bus_info

def get_response(received_msg):
    if received_msg.startswith('bus'):
        stop_id=received_msg[3:]
        reply=get_realtime(stop_id)
    else:
        reply = tuling_response(received_msg)
    return reply
        
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    received_msg=msg['Text']
    try:
        reply=get_response(received_msg)
    except:
        reply = '机器蛇好像挂了'
    return reply


itchat.auto_login(enableCmdQR=2)
itchat.run()

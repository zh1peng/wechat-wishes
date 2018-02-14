# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 13:44:09 2018

@author: 懒麻蛇
"""

def gen_poetry(key='这是测试',p_len='7',p_type='1',p_rythm='2'):
    """
输入皆为str

p_len=5 五言
p_len=7 七言

p_type=1 藏头
p_type=2 藏尾
p_type=3 藏中
p_type=4 递增
p_type=5 递减

p_rythm=1 双句一压
p_rythm=2 双句押韵
p_rythm=3 一三四押
"""
    from urllib import request, parse
    import json
    showapi_appid="55435"  
    showapi_sign="62fe27fa408342fda92bfcd68bad4894"  
    url="http://route.showapi.com/950-1"
    send_data = parse.urlencode([('showapi_appid', showapi_appid),('showapi_sign', showapi_sign)
    	,('num', p_len)
    	,('type',p_type)
    	,('yayuntype', p_rythm)
    	,('key', key)
    
    ])
    req = request.Request(url)
    try:
        response = request.urlopen(req, data=send_data.encode('utf-8'), timeout = 10) # 10秒超时反馈
    except Exception as e:
        print(e)
    result = response.read().decode('utf-8')
    result_json = json.loads(result)
    res_body=result_json['showapi_res_body']
    poetry_txt=res_body['list']
    return poetry_txt

import itchat
import time
itchat.auto_login()
friends = itchat.get_friends(update=True)[0:]
for i in friends:
    name=i['RemarkName']
    uname=i['UserName']
    msg1='智剑霜凝斩新雾\n鹏翼张风期万里\n祝辞回谢递丹霄\n'
    msg3='新歌一曲送祝福\n年年有余五谷丰\n快意人生精神爽\n乐享华年正从容\n万家千户贺新岁\n事随人愿展宏图\n如虎添翼雄风振\n意气奋发英姿酷\n恭祝狗年吉星照\n喜笑颜开沐春风\n发奋图强前锦阔\n财源广进福满屋\n'
    if len(name)==2:
        name_input=name
        msg0='hey %s,因考虑到明天会有铺天盖地的祝福短信堵塞网络,有理想有远见且智慧过人未卜先知的举世无双宇宙超级无敌天才提前恭祝新年快乐!万事如意!阖家幸福!\n\n'%name_input
        try:
            msg2=gen_poetry(name_input)[3]
        except:
            msg2='\n'
        msg2=msg2.replace('，','\n')
        msg2=msg2.replace('。','\n')
        if len(msg2)!=16:
            msg2='\n'
        my_msg=msg0+msg1+msg2+msg3
        print(my_msg)
        #itchat.send(my_msg, toUserName='filehelper')
        itchat.send(my_msg, toUserName=uname)
    elif len(name)==3:
        name_input=name[1:]
        msg0='hey %s,因考虑到明天会有铺天盖地的祝福短信堵塞网络,有理想有远见且智慧过人未卜先知的举世无双宇宙超级无敌天才提前恭祝新年快乐!万事如意!阖家幸福!\n\n'%name_input
        try:
            msg2=gen_poetry(name_input)[3]
        except:
            msg2='\n'
        msg2=msg2.replace('，','\n')
        msg2=msg2.replace('。','\n')
        if len(msg2)!=16:
            msg2='\n'
        my_msg=msg0+msg1+msg2+msg3
        print(my_msg)
        #itchat.send(my_msg, toUserName='filehelper')
        itchat.send(my_msg, toUserName=uname)
    else:
        continue
    msg2='\n'
    time.sleep(10)
        
#itchat.send('回复：\n帮我写一首+文字\n获得为你炮制的藏头诗\n例如：\n帮我写一首+新年快乐', toUserName=uname)

import requests
import itchat

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
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return

# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = 'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg['Text'])
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    return reply or defaultReply

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login()
itchat.run()


    

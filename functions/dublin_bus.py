
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

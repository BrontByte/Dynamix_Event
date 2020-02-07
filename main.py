#!/usr/bin/python

import requests
import json
import time

autoBuy = False
autoRetry = False
myCookie = ''
myUA = ''
myConfig = 'credittype=PAID&mapid=_map_soularmy_M&eventid=1423&assist=&avator=_char_SoulArmy'

headers = {'Expect': '100-continue',
           'X-Unity-Version': '2018.3.14f1',
           'Content-Type': 'application/x-www-form-urlencoded',
           'User-Agent': myUA,
           'Host': 'dynamix-server.c4-cat.com',
           'Connection': 'Keep-Alive',
           'Accept-Encoding': 'gzip',
           'Cookie': myCookie}


def enterGame(Config):
    url = 'http://dynamix-server.c4-cat.com//event/enter'
    data = Config
    response = requests.post(url=url, data=data, headers=headers, verify=False)
    if ('{"err":"Credit Not Enough"}' == response.text):
        buyCredit()
    else:
        print("你有这么多盘子：", json.loads(response.text)['userdata']['frag'])
        print("这么多蓝体力：", json.loads(response.text)['userdata']['freecredit'])
        print("和这么多金体力：", json.loads(response.text)['userdata']['paidcredit'])
        print("code:", json.loads(response.text)['eventcreditrecord']['code'])
        time.sleep(1)
        resultGame(json.loads(response.text)['eventcreditrecord']['code'])
        


def resultGame(gameCode):
    url = 'http://dynamix-server.c4-cat.com//event/result'
    data = 'code='+gameCode+'&clear=T&score=1000000'
    response = requests.post(url=url, data=data, headers=headers, verify=False)
    while('{"err":"TypeError: Cannot read property \'split\' of null"}' == response.text):
        #未知错误
        print("等一下")
        time.sleep(2)
        response = requests.post(url=url, data=data, headers=headers, verify=False)
    print("碎盘子", json.loads(response.text)['eventresult']['frag'])
    print("你抽到了:", json.loads(response.text)['eventresult']['itemid'])
    print("\t\t\t\t\t\t\t\t\t出货",json.loads(response.text)['eventresult']['itemRarity'])
    return (json.loads(response.text)['eventresult']['itemRarity'] == 1)

def buyCredit():
    if autoBuy:
        print("没体力了，自动购买")
    else:
        input("你没体力了，买点？")
    url = 'http://dynamix-server.c4-cat.com//event/refillcredit'
    data = '1=1'
    #response =
    requests.post(url=url, data=data, headers=headers, verify=False)
    return 0       #懒得做判断

if myCookie == '' or myUA == '' or myConfig == '':
    print("请先抓包获取Cookie,User-Agent,enter数据包的data")
    exit()
while True:
    enterGame(myConfig)
    if autoRetry:
        pass
    else:
        input("再来一遍?")

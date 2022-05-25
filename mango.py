# -*- coding: utf-8 -*-

import re
import time
import json
import base64
import random
import requests

def getName(videoid, videotitle, timestamp, cookies):
    mango_getname_api = 'https://pcweb.api.mgtv.com/video/info?vid=' + videoid + '&cid=' + videotitle + '&_support=10000000&callback=jsonp_' + str(timestamp)
    mango_getname_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4128.3 Safari/537.36'}
    mango_getname_cookies = cookies
    mango_getname_response = requests.get(url=mango_getname_api, headers=mango_getname_headers, cookies=mango_getname_cookies)
    mango_getname_result = mango_getname_response.content.decode("utf-8")
    mango_getname_result_dict = json.loads(mango_getname_result[17:-1])

    mango_videoname = mango_getname_result_dict['data']['info']['videoName']
    mango_videotitle = mango_getname_result_dict['data']['info']['title']
    mango_videolen = mango_getname_result_dict['data']['info']['time']

    return mango_videoname, mango_videotitle, mango_videolen

def genTK2(did, timestamp):
    tk2_base = "did=" + did + "|pno=1030|ver=0.3.0301|clit=" + str(int(timestamp / 1000))
    tk2_base64 = base64.b64encode(tk2_base.encode("utf-8")).decode("utf-8")
    tk2_mod = tk2_base64.replace("+", "_").replace("/", "~").replace("=", "-")
    tk2_arr = list(tk2_mod)
    tk2_arr.reverse()
    tk2_out = ''.join(tk2_arr)
    return tk2_out

def getTK2PM2(tk2_out, videoid, timestamp, cookies):
    mango_tk2pm2_api = "https://pcweb.api.mgtv.com/player/video?did=af0af9f3-35db-48fc-902e-e04e5e3bfb9b&suuid=&cxid=&tk2=" + tk2_out + "&video_id=" + videoid + "&type=pch5&_support=10000000&auth_mode=1&callback=jsonp_" + str(timestamp)
    mango_tk2pm2_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4128.3 Safari/537.36'}
    mango_tk2pm2_cookies = cookies
    mango_tk2pm2_response = requests.get(url=mango_tk2pm2_api, headers=mango_tk2pm2_headers, cookies=mango_tk2pm2_cookies)
    mango_tk2pm2_result = mango_tk2pm2_response.content.decode("utf-8")
    mango_tk2pm2_result_dict = json.loads(mango_tk2pm2_result[17:-1])
    mango_pm2 = mango_tk2pm2_result_dict['data']['atc']['pm2']
    mango_tk2 = mango_tk2pm2_result_dict['data']['atc']['tk2']
    return mango_pm2, mango_tk2

def getSource(mango_tk2, mango_pm2, videoid, timestamp, cookies):
    mango_getsouce_api = 'https://pcweb.api.mgtv.com/player/getSource?_support=10000000&tk2=' + mango_tk2 + '&pm2=' + mango_pm2 + '&video_id=' + videoid + '&type=pch5&callback=jsonp_' + str(timestamp)
    mango_getsouce_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4128.3 Safari/537.36'}
    mango_getsouce_cookies = cookies
    mango_getsouce_response = requests.get(url=mango_getsouce_api, headers=mango_getsouce_headers, cookies=mango_getsouce_cookies)
    mango_getsouce_result = mango_getsouce_response.content.decode("utf-8")
    mango_getsouce_result_dict = json.loads(mango_getsouce_result[17:-1])
    '''
    jumpurl = ['', '', '', '']
    jumpurllen = len(mango_getsouce_result_dict['data']['stream'])
    for index in range(jumpurllen):
        jumpurl[index] = mango_getsouce_result_dict['data']['stream'][index]['url']
    '''
    return  mango_getsouce_result_dict['data']['stream']

def outJSON(qua, jumpurl, cookies, mango_videolen, mango_videotitle, mango_videoname):
    quarr = qua.split(",")
    json_outstr = {
        "VideoName": "",
        "VideoTitle": "",
        "VideoLength": "",
    }
    json_outstr['VideoLength'] = mango_videolen
    json_outstr['VideoTitle'] = mango_videotitle
    json_outstr['VideoName'] = mango_videoname
    jumpbaseurl = 'https://web-disp.titan.mgtv.com'
    for index in range(len(quarr)):
        getm3u8url = jumpbaseurl + jumpurl[int(quarr[index])]['url']
        mango_getm3u8_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4128.3 Safari/537.36'}
        mango_getm3u8_cookies = cookies
        mango_getm3u8_response = requests.get(url=getm3u8url, headers=mango_getm3u8_headers, cookies=mango_getm3u8_cookies)
        mango_getm3u8_result = mango_getm3u8_response.content.decode("utf-8")
        mango_getm3u8_result_dict = json.loads(mango_getm3u8_result)
        m3u8 = mango_getm3u8_result_dict['info']
        json_outstr[jumpurl[int(quarr[index])]['name']] = m3u8
    return  json_outstr

def getDID():
    r = ""
    for i in range(19):
        r += str(random.randint(0,9))
    return r

def querydata2json(data):
    MUST = ["id", "title"]
    rj = {}
    da = data.split('&')
    for i in range(len(da)):
        daa = da[i].split("=")
        rj[daa[0]] = daa[1]
    for key in MUST:
        if key not in rj:
            return "ERR"
    return rj


def handler(environ, start_response):
    
    query_data = querydata2json(environ['QUERY_STRING'])
    if query_data == "ERR":
        ERR_INFO = {"ERR": "PARAMS ERROR!"}
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return str(ERR_INFO)
    videoid = query_data["id"]
    videotitle = query_data["title"]

    cookies = {'HDCN': '',}
    did = getDID()
    if "hdcn" in query_data:
        cookies['HDCN'] = query_data["hdcn"]

    timestamp = int(time.time())

    infoarr = getName(videoid, videotitle, timestamp, cookies)
    mango_videoname = infoarr[0]
    mango_videotitle = infoarr[1]
    mango_videolen = infoarr[2]

    tk2_out = genTK2(did, timestamp)

    infoarr = getTK2PM2(tk2_out, videoid, timestamp, cookies)
    mango_pm2 = infoarr[0]
    mango_tk2 = infoarr[1]

    jumpurl = getSource(mango_tk2, mango_pm2, videoid, timestamp, cookies)
    if "qua" in query_data:
        qua = query_data["qua"]
    else:
        qua = "0,1,2,3"
    outjson = outJSON(qua, jumpurl, cookies, mango_videolen, mango_videotitle, mango_videoname)
    start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
    return str(outjson)


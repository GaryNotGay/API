# -*- coding: utf8 -*-
import json
import time
import math
import base64
import urllib
import random
import requests

def getTM():
    return str(int(time.time()))

def getGUID():
    s = ""
    for i in range(32):
        s += random.choice('abcdef1234567890')
    return s

def getRFID(tm):
    id = getGUID()
    return f"{id}_{tm}"

def createPID():
    a = 32
    b = ''
    for index in range(32):
        d = hex(math.floor(16 * random.random()))
        b += d[2:]
    return b

def getFlowid(pid, plat):
    return f"{pid}_{plat}"

def getCkey(plat, vid, guid, tm, url):
    url = f'https://api.telecom.ac.cn/ckey81?platform={plat}&vid={vid}&guid={guid}&time={tm}&url={url}'
    r = requests.get(url)
    ckey = json.loads(r.content)["KEY"].upper()
    return ckey

def logincookie(guid, cookie):
    #print(cookie)
    login = {"guid":guid,
             "main_login": "qq",
             "openid": cookie["vqq_openid"],
             "appid": cookie["vqq_appid"],
             "access_token": cookie["vqq_access_token"],
             "vuserid": cookie["vqq_vuserid"],
             "vusession": cookie["vqq_vusession"]}
    logindata = json.dumps(login)
    return str(logindata)
    # return str(login)

def getVideoInfo(vid):
    u = f"http://vv.video.qq.com/getinfo?vids={vid}&otype=ojson"
    r = requests.get(url=u)
    rj = json.loads(r.content.decode("utf-8"))
    title = rj["vl"]["vi"][0]["ti"]
    duration = rj["vl"]["vi"][0]["td"]
    return title, duration

def getM3U8(adparam, vinfoparam):
    data = {"buid": "vinfoad", "adparam": None, "vinfoparam": None}
    data["adparam"] = urllib.parse.urlencode(adparam)
    data["vinfoparam"] = urllib.parse.urlencode(vinfoparam)
    datas = json.dumps(data)
    print(datas)
    result = requests.post(url='https://vd.l.qq.com/proxyhttp', data=datas).text
    result_json = json.loads(result)
    video_info = json.loads(result_json["vinfo"])
    print(video_info)
    #name = video_info["vl"]["vi"][0]["ti"]
    return video_info["vl"]["vi"][0]["ul"]["ui"][0]["url"]

def querydata2json(data):
    MUST = ["vid", "coverid"]
    rj = {}
    da = data.split('&')
    for i in range(len(da)):
        daa = da[i].split("=")
        rj[daa[0]] = daa[1]+(len(daa)-2)*"="
    for key in MUST:
        if key not in rj:
            return "ERR"
    return rj
    
def handler(environ, start_response):
    qua_list = ['270P', '480P', '720P', '1080P']
    defn_list = ['sd', 'hd', 'shd', 'fhd']

    vinfoparam = {
        "charge":"0",
        "otype":"ojson",
        "defnpayver":"1",
        "spau":"1",
        "spaudio":"0",
        "spwm":"1",
        "sphls":"2",
        "host":"v.qq.com",
        "refer":"v.qq.com",
        "ehost":"", #
        "sphttps":"1",
        "encryptVer":"8.1",
        "cKey":"", #
        "platform":"", #
        "sdtfrom":"v1010",
        "appVer":"3.5.57",
        "unid":"",
        "auth_from":"",
        "auth_ext":"",
        "vid":"", #
        "defn":"", #
        "fhdswitch":"0",
        "dtype":"3",
        "drm":"40",
        "spsrt":"2",
        "tm":"", #
        "lang_code":"0",
        "logintoken":"",
        "spvvpay":"1",
        "spadseg":"3",
        "hevclv":"0",
        "spsfrhdr":"0",
        "spvideo":"0"
    }

    adparam = {
        "pf":"in",
        "pf_ex":"pc",
        "pu":"1",
        "pt":"0",
        "platform":"", #
        "from":"0",
        "flowid":"", #
        "guid":"", #
        "coverid":"", #
        "vid":"", #
        "chid":"0",
        "tpid":"106",
        "refer":"",
        "url":"", #
        "lt":"qq",
        "opid":"",#
        "atkn":"",#
        "appid":"",#
        "uid":"",#
        "tkn":"",#
        "rfid":"", #
        "v":"1.4.94",
        "vptag":"",
        "ad_type":"LD|KB|PVL",
        "live":"0",
        "appversion":"1.5.4",
        "ty":"web",
        "adaptor":"1",
        "dtype":"1",
        "resp_type":"json"
    }

    request_id = environ['fc.context'].request_id
    try:
        query_data = querydata2json(environ['QUERY_STRING'])
        if query_data == "ERR":
            ERR_INFO = {"Status":"False", "Message": "缺少必要参数，请参考接口文档，确认必要参数", "Info": "https://doc.api.telecom.ac.cn/", "UUID": request_id}
            start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
            return json.dumps(ERR_INFO, ensure_ascii=False)
        vid = query_data["vid"]
        coverid = query_data["coverid"]
        if "qua" in query_data:
            qua = query_data["qua"].split(',')
        else:
            qua = ["0", "1", "2", "3"]
        if "token" in query_data:
            #print(query_data["token"])
            cookie = json.loads(str(base64.b64decode(query_data["token"]))[2:-1])
            print(cookie)
        else:
            cookie = {
                        "main_login": "qq",
                        "vqq_openid": "",
                        "vqq_appid": "",
                        "vqq_access_token": "",
                        "vqq_vuserid": "",
                        "vqq_vusession": "",
                    }

        platform = "10201"
        url = f"https://v.qq.com/x/cover/{coverid}/{vid}.html"

        videoinfo = getVideoInfo(vid)
        json_outstr = {
            "Status": "True",
            "UUID": request_id,
            "VideoName": videoinfo[0],
            "VideoLength": videoinfo[1],
            }

        for i in range(len(qua)):
            defn = defn_list[int(qua[i])]
            guid = getGUID()
            tm = getTM()
            pid = createPID()
            ckey = getCkey(platform, vid, guid, tm, url)
            flowid = getFlowid(pid, platform)
            rfid = getRFID(tm)

            vinfoparam["ehost"] = url
            vinfoparam["defn"] = defn
            vinfoparam["cKey"] = ckey
            vinfoparam["platform"] = platform
            vinfoparam["vid"] = vid
            vinfoparam["tm"] = tm
            vinfoparam["logintoken"] = logincookie(guid, cookie)
            #vinfoparam["logintoken"] = ""

            adparam["coverid"] = coverid
            adparam["vid"] = vid
            adparam["flowid"] = flowid
            adparam["guid"] = guid
            adparam["rfid"] = rfid
            adparam["platform"] = platform
            adparam["url"] = url
            adparam["refer"] = url
            adparam["opid"] = cookie["vqq_openid"],
            adparam["atkn"] = cookie["vqq_access_token"]
            adparam["appid"] = cookie["vqq_appid"]
            adparam["uid"] = cookie["vqq_vuserid"]
            adparam["tkn"] = cookie["vqq_vusession"]

            m3u8 = getM3U8(adparam, vinfoparam)
            json_outstr[qua_list[int(qua[i])]] = m3u8

        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return json.dumps(json_outstr, ensure_ascii=False)
    except Exception as e:
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        outjson = {"Status": "False", "Message": "未知错误，请参考错误信息，定位原因，或联系作者", "Info": str(e), "UUID": request_id}
        return json.dumps(outjson, ensure_ascii=False)
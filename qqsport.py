# -*- coding: utf8 -*-
import time
import json
import random
import requests
from urllib import parse
from urllib import request

header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46",
          "referer": "https://sports.qq.com/"
        }

login = {"vqq_openid": "",
         "vqq_appid": "",
         "vqq_access_token": "",}

def getLiveID(mid):
    url = "https://matchweb.sports.qq.com/kbs/matchDetail?mid=" + str(mid)
    #print(url)
    req = requests.get(url)
    res = json.loads(req.content.decode('utf-8'))
    #print(res)
    teaminfo = res['data']['matchInfo']['leftName'] + ' vs ' + res['data']['matchInfo']['rightName']
    commentator = res['data']['matchInfo']['commentator']
    return res['data']['liveId'], res['data']['programId'], teaminfo, commentator

def getGUID():
    s = ""
    for i in  range(32):
        s += random.choice('abcdefghijklmnopqrstuvwxyz1234567890')
    return s

def getTM():
    return str(int(time.time()))

def getEnVer():
    ver = "7."
    today = int(time.strftime("%w"))
    if today == 0:
        today = 7
    ver += str(today)
    return ver

# todo
def getCkey(platform, liveid, sdt, tm, ver):
    url = f"https://api.telecom.ac.cn/ckey7x?platform={platform}&vid={liveid}&sdt={sdt}&tm={tm}&ver={ver}"
    response = requests.get(url)
    ckey = response.text
    return ckey

def jsonDataToUrlParams(params_data):
    url_str = '?'
    nums = 0
    max_nums = len(params_data)
    for key in params_data:
        nums = nums + 1
        # 如果是最后一位就不要带上&
        # 拼为url字符串
        if nums == max_nums:
            url_str += str(key) + '=' + str(params_data[key])
        else:
            url_str += str(key) + '=' + str(params_data[key]) + '&'
    return url_str


def getM3U8(defn, liveId, programId):
    url = "https://infozb6.video.qq.com/"
    params = {
        "cmd": "2",
        "cnlid": "",
        "pla": "0",
        "stream": "2",
        "system": "0",
        "appVer": "3.0.0.157",
        "encryptVer": "",
        "qq": "0",
        "device": "PC",
        "guid": "",
        "defn": "fhd",
        "host": "qq.com",
        "livepid": "",
        "logintype": "1",
        "vip_status": "1",
        "livequeue": "1",
        "fntick": "",
        "tm": "",
        "sdtfrom": "1107",
        "platform": "40201",
        "cKey": "",
        "queueStatus": "0",
        "sphttps": "1",
        "authext": "",
        "auth_ext": "",
        "auth_from": "40001",
        "logintoken": "",
        }

    params["defn"] = defn
    params["cnlid"] = str(liveId)
    params["livepid"] = str(programId)
    ver = getEnVer()
    params["encryptVer"] = ver
    params["guid"] = getGUID()
    tm = getTM()
    params["fntick"] = params["tm"] = tm
    params["cKey"] = getCkey(params["platform"], liveId, params["sdtfrom"], tm, ver)
    params["authext"] = params["auth_ext"] = params["logintoken"] = login

    url_json = json.dumps(params)
    url_data = jsonDataToUrlParams(params)
    url += url_data.replace("'", "\"").replace(" ", "")
    req = requests.get(url, cookies=login, headers=header)

    res = json.loads(req.content.decode("utf-8"))
    m3u8url = res["playurl"]
    return m3u8url

def querydata2json(data):
    MUST = ["mid"]
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
    try:
        query_data = querydata2json(environ['QUERY_STRING'])
        if query_data == "ERR":
            ERR_INFO = {"Status":"False", "Message": "缺少必要参数，请参考接口文档，确认必要参数", "Info": "https://doc.api.telecom.ac.cn/"}
            start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
            return json.dumps(ERR_INFO, ensure_ascii=False)
        mid = query_data["mid"]
        if "qua" in query_data:
            qua = query_data["qua"]
        else:
            qua = "3"
        
        if "openid" in query_data:
            login["openid"] = query_data["openid"]
        if "appid" in query_data:
            login["appid"] = query_data["appid"]
        if "token" in query_data:
            login["token"] = query_data["token"]


        defnarr = ["sd", "hd", "shd", "fhd"]
        defn = defnarr[int(qua)]
        #mid = "208:2288013"
        info = getLiveID(mid)
        liveId = info[0]
        programId = info[1]
        teaminfo = info[2]
        commentator = info[3]
        m3u8 = getM3U8(defn, liveId, programId)

        json_outstr = {
            "LiveName": "",
            "LiveCommentator": "",
            "Url":"",
        }
        json_outstr['LiveName'] = teaminfo
        json_outstr['LiveCommentator'] = commentator
        json_outstr['Url'] = m3u8
        print(json_outstr)
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return json.dumps(json_outstr, ensure_ascii=False)
    except Exception as e:
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        outjson = {"Status": "False", "Message": "未知错误，请参考错误信息，定位原因，或联系作者", "Info": str(e)}
        return json.dumps(outjson, ensure_ascii=False)

import json
import uuid
import requests

def getUUID():
    return str(uuid.uuid1())

def getAPI(cid, qua, userId, userToken, code):
    if code == "h265":
        u = f"https://webapi.miguvideo.com/xxxxxxx"
    else:
        u = f"https://webapi.miguvideo.com/xxxxxxx"
    #出于接口保密性及安全性考虑，暂不公开接口信息
    h = {
        "SDKCEId": "",
        "terminalId": "pc",
        "userId": "",
        "userToken": "",
    }

    h["SDKCEId"] = getUUID()
    h["userId"] = userId
    h["userToken"] = userToken

    r = requests.get(url=u, headers=h)
    rj = json.loads(r.content.decode("utf-8"))
    return rj

def querydata2json(data):
    MUST = ["cid"]
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
    cid = query_data["cid"]

    if "qua" in query_data:
        qua = query_data["qua"]
    else:
        qua = "2,3,4"
    
    if "userId" in query_data:
        userId = query_data["userId"]
    else:
        userId = ""

    if "userToken" in query_data:
        userToken = query_data["userToken"]
    else:
        userToken = ""
    
    json_outstr = {
        "VideoName": "",
        "VideoLength": "",
        "VideoUrl":"",
    }
    urlarr = []

    lqua = ""
    hqua = ""
    quaarr = qua.split(",")
    for i in range(len(quaarr)):
        if int(quaarr[i]) > 4:
            hqua += quaarr[i]
            hqua += ","
        else:
            lqua += quaarr[i]
            lqua += ","

    data = getAPI(cid, hqua, userId, userToken, "h265")
    if data["code"] == "200":
        json_outstr['VideoName'] = data["body"]["content"]["contName"]
        json_outstr['VideoLength'] = data["body"]["content"]["duration"]
        for i in range(len(data["body"]["urlInfos"])):
            urlt = {"rateDesc": "", "videoCoding": "", "TrySee": "", "url": ""}
            urlt["rateDesc"] = data["body"]["urlInfos"][i]["rateDesc"]
            urlt["videoCoding"] = data["body"]["urlInfos"][i]["videoCoding"]
            urlt["url"] = data["body"]["urlInfos"][i]["url"]
            if data["body"]["urlInfos"][i]["trySeeDuration"] == "0":
                urlt["TrySee"] = "False"
            else:
                urlt["TrySee"] = "True"
            if int(data["body"]["urlInfos"][i]["rateType"]) > 4:
                urlarr.append(urlt)
        data = getAPI(cid, lqua, userId, userToken, "h264")
        for i in range(len(data["body"]["urlInfos"])):
            urlt = {"rateDesc": "", "videoCoding": "", "TrySee": "", "url": ""}
            urlt["rateDesc"] = data["body"]["urlInfos"][i]["rateDesc"]
            urlt["videoCoding"] = data["body"]["urlInfos"][i]["videoCoding"]
            urlt["url"] = data["body"]["urlInfos"][i]["url"]
            if data["body"]["urlInfos"][i]["trySeeDuration"] == "0":
                urlt["TrySee"] = "False"
            else:
                urlt["TrySee"] = "True"
            if int(data["body"]["urlInfos"][i]["rateType"]) < 5:
                urlarr.append(urlt)
        json_outstr['VideoUrl'] = urlarr

        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return str(json_outstr)
    else:
        err = {"Message": "", "Desc": "接口只支持网页端可播放的视频"}
        err["Message"] = data["message"]
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return str(err)
import json
import requests

def getVid(mid):
    u = f"https://matchweb.sports.qq.com/kbs/matchVideoAll?mid={mid}&callback=matchVideoAllReplay"
    r = requests.get(u)
    print(r.content)
    rj = json.loads(r.content)

    vid = ""
    matchIndex = 0
    for i in range(len(rj["data"]["playbackList"])):
        if int(rj["data"]["playbackList"][i]["matchIndex"]) > matchIndex:
            matchIndex = int(rj["data"]["playbackList"][i]["matchIndex"])
            vid = rj["data"]["playbackList"][i]["vid"]
    return vid

def querydata2json(data):
    MUST = ["mid"]
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
    request_id = environ['fc.context'].request_id
    try:
        query_data = querydata2json(environ['QUERY_STRING'])
        if query_data == "ERR":
                ERR_INFO = {"Status":"False", "Message": "缺少必要参数，请参考接口文档，确认必要参数", "Info": "https://doc.api.telecom.ac.cn/", "UUID": request_id}
                start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
                return json.dumps(ERR_INFO, ensure_ascii=False)
        mid = query_data["mid"]

        vid = getVid(mid)
        url = f"https://v.qq.com/x/page/{vid}.html"
        start_response('302 Moved Temporarily', [('Location', url), ('Access-Control-Allow-Origin', '*')])
        return ""

    except Exception as e:
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        outjson = {"Status": "False", "Message": "未知错误，请参考错误信息，定位原因，或联系作者", "Info": str(e), "UUID": request_id}
        return json.dumps(outjson, ensure_ascii=False)
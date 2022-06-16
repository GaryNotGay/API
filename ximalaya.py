# -*- coding: utf8 -*-
import json
import base64
import requests

def getTime():
    url = 'https://www.ximalaya.com/revision/time'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4181.9 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    result = response.content.decode('utf-8')
    return result

def getAlbum(albumId):
    url = f'https://www.ximalaya.com/revision/album/v1/getTracksList?pageSize=100&albumId={albumId}'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4181.9 Safari/537.36',}
    response = requests.get(url=url, headers=headers)
    result = response.content.decode('utf-8')
    resultJson = json.loads(result)
    rj = {
        "AlbumName": resultJson['data']['tracks'][0]['albumTitle'],
        "TrackTotalNum": resultJson['data']['trackTotalCount'],
        "tracksID": "",
    }
    tracksID = []
    for index in range(len(resultJson['data']['tracks'])):
        tracksID.append({"index": resultJson['data']['tracks'][index]['index'], "trackId":resultJson['data']['tracks'][index]['trackId']})
    if rj["TrackTotalNum"] > 100:
        pageTotalNum = int(rj["TrackTotalNum"]/100)+1
        pageNum = 2
        while pageNum <= pageTotalNum:
            url = f'https://www.ximalaya.com/revision/album/v1/getTracksList?pageSize=100&albumId={albumId}&pageNum={pageNum}'
            response = requests.get(url=url, headers=headers)
            result = response.content.decode('utf-8')
            resultJson = json.loads(result)
            for i in range(len(resultJson['data']['tracks'])):
                tracksID.append({"index": resultJson['data']['tracks'][i]['index'], "trackId":resultJson['data']['tracks'][i]['trackId']})
            pageNum += 1
    rj["tracksID"] = tracksID
    return json.loads(json.dumps(rj, ensure_ascii=False))

def getTrack(trackId, qua, token):
    qua_list = ["M4A_64", "MP3_64", "M4A_24", "MP3_32", "AAC_24"]
    time = getTime()
    url = f"https://mobile.ximalaya.com/mobile-playpage/track/v3/baseInfo/{time}?device=web&trackId={trackId}"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4181.9 Safari/537.36', }
    cookies = {'1&_token': token,
               'login_type': 'password_mobile',}
    response = requests.get(url=url, cookies=cookies, headers=headers)
    result = response.content.decode('utf-8')
    resultJson = json.loads(result)
    track = {
        "AudioName": resultJson['trackInfo']['title'],
        "AudioLen": resultJson['trackInfo']['duration'],
        "AudioUrls": "",
    }
    urls = []
    for i in  range(len(resultJson['trackInfo']['playUrlList'])):
        url = {"type": "", "url": ""}
        for q in range(len(qua)):
            if resultJson['trackInfo']['playUrlList'][i]["type"] == qua_list[int(qua[q])]:
                url["type"] = resultJson['trackInfo']['playUrlList'][i]["type"]
                url["url"] = decryprUrl(resultJson['trackInfo']['playUrlList'][i]["url"])
                urls.append(url)
    track["AudioUrls"] = urls
    return track

def decryprUrl(u):
    u = f"https://api.telecom.ac.cn/xmlyde?t={u}"
    r = requests.get(url=u)
    rj = json.loads(r.content.decode("utf-8"))
    return rj["Url"]

def querydata2json(data):
    MUST = ["all"]
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
    request_id = environ['fc.context'].request_id
    try:
        query_data = querydata2json(environ['QUERY_STRING'])
        if query_data == "ERR":
            ERR_INFO = {"Status":"False", "Message": "缺少必要参数，请参考接口文档，确认必要参数", "Info": "https://doc.api.telecom.ac.cn/", "UUID": request_id}
            start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
            return json.dumps(ERR_INFO, ensure_ascii=False)
        isall = query_data["all"]
        if int(isall) == 1:
            isAll = True
        else:
            isAll = False
        if "token" in query_data:
            token = str(base64.b64decode(query_data["token"]))[2:-1]
            print(token)
        else:
            token = ""
        if "qua" in query_data:
            qua = query_data["qua"].split(',')
        else:
            qua = ["0", "1", "2", "3", "4"]
        if isAll:
            if "albumid" in query_data:
                albumId = query_data["albumid"]
            else:
                outjson = {"Status": "False", "Message": "缺少必要参数，请参考接口文档，确认必要参数", "Info": "all=1时，请搭配albumid参数", "UUID": request_id}
                start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
                return json.dumps(outjson, ensure_ascii=False)
            #albumId = "30510905"
            AlbumInfo = getAlbum(albumId)
            json_outstr = {"Status": "True",
                        "UUID": request_id,
                        "AlbumName": AlbumInfo["AlbumName"],
                        "TrackTotalNum": AlbumInfo["TrackTotalNum"],
                        "AlbumUrls": ""}
            urls = []
            for i in range(len(AlbumInfo["tracksID"])):
                trackID = AlbumInfo["tracksID"][i]["trackId"]
                index = AlbumInfo["tracksID"][i]["index"]
                trackInfo = getTrack(trackID, qua, token)
                trackInfo["index"] = index
                urls.append(trackInfo)
            json_outstr["AlbumUrls"] = urls
            #print(json_outstr)
            start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
            return json.dumps(json_outstr, ensure_ascii=False)
        else:
            if "trackid" in query_data:
                trackID = query_data["trackid"]
            else:
                outjson = {"Status": "False", "Message": "缺少必要参数，请参考接口文档，确认必要参数", "Info": "all!=1时，请搭配trackid参数", "UUID": request_id}
                start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
                return json.dumps(outjson, ensure_ascii=False)
            #trackID = "314550869"
            trackInfo = getTrack(trackID, qua, token)
            trackInfo["Status"] = "True"
            trackInfo["UUID"] = request_id
            print(trackInfo)
            start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
            return json.dumps(trackInfo, ensure_ascii=False)

    except Exception as e:
        outjson = {"Status": "False", "Message": "未知错误，请参考错误信息，定位原因，或联系作者", "Info": str(e), "UUID": request_id}
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return json.dumps(outjson, ensure_ascii=False)
    
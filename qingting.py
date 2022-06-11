# 蜻蜓网页端付费音频已下线，该接口暂停使用，仅用作代码保存

# -*- coding: utf8 -*-
import json
import time
import hmac
import base64
import requests

def getDetail(userID, channel):
    url = 'https://i.qingting.fm/capi/v3/channel/' + str(channel) + '?user_id=' + str(userID)
    response = requests.get(url)
    result = response.content.decode('utf-8')
    resultJson = json.loads(result)
    v = resultJson['data']['v']
    name = resultJson['data']['title']
    total = resultJson['data']['program_count']
    return v, name, total

def getList(userID, v, channel, total):
    if total <= 100:
        url = 'https://i.qingting.fm/capi/channel/' + str(channel) + '/programs/' + str(v) + '?curpage=1&pagesize=' + str(total) + '&order=asc'
        response = requests.get(url)
        result = response.content.decode('utf-8')
        resultJson = json.loads(result)
        detail = resultJson['data']['programs']
        return detail
    else:
        detail = []
        for index in range(int(total/100) + 1):
            url = 'https://i.qingting.fm/capi/channel/' + str(channel) + '/programs/' + str(v) + '?curpage=' + str(index+1) + '&pagesize=100&order=asc'
            print(url)
            response = requests.get(url)
            result = response.content.decode('utf-8')
            resultJson = json.loads(result)
            detail += resultJson['data']['programs']
        return detail

def getUserInfo():
    user_id = ''
    password = ''
    data = {'account_type': '5', 'device_id': 'web', 'user_id': user_id, 'password': password}
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4181.9 Safari/537.36'}
    url = 'https://u2.qingting.fm/u2/api/v4/user/login'
    response = requests.post(url = url, json = data, headers = headers)
    result = response.content.decode('utf-8')
    resultJson = json.loads(result)
    qingting_id = resultJson['data']['qingting_id']
    access_token = resultJson['data']['access_token']
    return qingting_id, access_token

def getLen(length):
    i = ''
    h = int(length / 3600)
    if not h == 0:
        i += str(h)
        i += 'h'
    length %= 3600
    m = int(length / 60)
    if not m == 0:
        i += str(m)
        i += 'm'
    length %= 60
    if not length == 0:
        i += str(length)
        i += 's'
    return i

def CreatSign(url):
    message = bytes(url, 'utf-8')
    key = bytes('fpMn12&38f_2e', 'utf-8')
    sign = hmac.new(key, message, digestmod='MD5').hexdigest()
    return sign

def getDownUrl(channel, audioID, userID, AccessToken):
    cookies = {'qingting_id': ''}
    cookies['qingting_id'] = userID
    timestamp = int(time.time() * 1000)
    domain = 'https://audio.qingting.fm'
    url =  '/audiostream/redirect/' + str(channel) + '/' + str(audioID) + '?access_token=' + str(AccessToken) + '&device_id=MOBILESITE&qingting_id=' + str(userID) + '&t=' + str(timestamp)
    sign = CreatSign(url)
    url += '&sign=' + str(sign)
    return domain + url

def querydata2json(data):
    MUST = ["channel", "audioID"]
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
    JsonEncode = {'Warnning':'Standard Format is \'channelsID+programsID / channelsID+0\' (https://www.qingting.fm/channels/channelsID/programs/programsID/)',
              'Encode':'Base64',
              'Key':'Null',
              'ParseResult':''}
    try:
        query_data = querydata2json(environ['QUERY_STRING'])
        if query_data == "ERR":
            ERR_INFO = {"Status":"False", "Message": "缺少必要参数，请参考接口文档，确认必要参数", "Info": "https://doc.api.telecom.ac.cn/"}
            start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
            return json.dumps(ERR_INFO, ensure_ascii=False)
        channel = query_data["channel"]
        audioID = query_data["audioID"]

        isFull = False
        if audioID == '0':
            isFull = True

        UserInfo = getUserInfo()
        print(UserInfo)
        userID = UserInfo[0]
        AccessToken = UserInfo[1]
        AudioDetail = getDetail(userID, channel)
        v = AudioDetail[0]
        name = AudioDetail[1]
        total = AudioDetail[2]
        AudioList = getList(userID, v, channel, total)

        if not isFull:
            res = {}
            for index in range(len(AudioList)):
                if str(AudioList[index]['id']) == audioID:
                    audioName = AudioList[index]['title']
                    duration = AudioList[index]['duration']
                    break
            length = getLen(duration)
            downUrl = getDownUrl(channel, audioID, userID, AccessToken)
            res[name + '-' + audioName + '-' + length] = downUrl
            outstr = base64.b64encode(str(res).encode('utf-8')).decode('utf-8')
            JsonEncode['ParseResult'] = outstr
            start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
            return json.dumps(JsonEncode, ensure_ascii=False)
        else:
            res = {}
            for index in range(len(AudioList)):
                audioName = AudioList[index]['title']
                duration = AudioList[index]['duration']
                length = getLen(duration)
                downUrl = getDownUrl(channel, audioID, userID, AccessToken)
                res[audioName + '-' + length] = downUrl
            out = {'name': name, 'res': res}
            outstr = base64.b64encode(str(out).encode('utf-8')).decode('utf-8')
            JsonEncode['ParseResult'] = outstr
            start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
            return json.dumps(JsonEncode, ensure_ascii=False)
    except Exception as e:
        outjson = {"Status": "False", "Message": "未知错误，请参考错误信息，定位原因，或联系作者", "Info": str(e)}
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return json.dumps(outjson, ensure_ascii=False)
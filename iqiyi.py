# -*- coding: utf8 -*-
import oss2
import json
import time
import random
import hashlib
import base64
import requests
import urllib.parse

def md5(s):
    return hashlib.md5(s.encode('utf8')).hexdigest()

def getTM():
    return str(int(time.time() * 1000))

def get_kuid():
    '''获取macid,此值是通过mac地址经过算法变换而来,对同一设备不变'''
    macid = ''
    chars = 'abcdefghijklnmopqrstuvwxyz0123456789'
    size = len(chars)
    for i in range(32):
        macid += list(chars)[random.randint(0, size - 1)]
    return macid

def getVF(param):
    param64 = str(base64.b64encode(param.encode("utf-8")))[2:-1]
    url = f'https://api.telecom.ac.cn/cmd5x?param={param64}'
    response = requests.get(url)
    result = response.content.decode('utf-8')
    rj = json.loads(result)
    return rj["KEY"]

def getVideoInfo(url):
    response = requests.get(url)
    result = response.content.decode('utf-8')
    videojson_index_start = result.find('window.QiyiPlayerProphetData=')+len('window.QiyiPlayerProphetData=')
    videojson_index_end = result.find('</script>', videojson_index_start)
    resultJson = json.loads(result[videojson_index_start: videojson_index_end])
    tvid = str(resultJson['v']['tvid'])
    vid = str(resultJson['v']['vid'])
    return tvid, vid

def getUrl(tvid, vid, bid, P1, P3):
    baseurl = 'https://cache.video.iqiyi.com/dash?'
    #tvid = '2922791537225900'
    #bid = '600' 200--360P 300--540P 500--720P 600--1080P
    #vid = '0d753a6b6ee8b6d8b96505a5fec60d1e'
    src = '01010031010000000000' # static
    '''
    salt h2l6suw16pbtikmotf0j79cej4n8uw13
        01010031010000000000
        01010031010010000000
        01080031010000000000
        01080031010010000000
        03020031010000000000
        03020031010010000000
        03030031010000000000
        03030031010010000000
        02020031010000000000
        02020031010010000000
    '''
    vt = '0' # static
    rs = '1' # static
    uid = P3
    ori = 'pcw' # static
    ps = '0' # static or 0
    tm = getTM()
    qd_v = '2' # static or 2
    k_uid = '06620b78f2d7f96b516c5b55a20d853b'
    pt = '0'  # static
    d = '0'  # static
    authKey = md5("d41d8cd98f00b204e9800998ecf8427e"+tm+tvid)
    k_tag = '1'  # static
    ost = '0' # static
    ppt = '0'  # static
    dfp = 'a0bc5541cebb2a45fba3d2a345595bcb9a5fd9ba71ff9606fd5a13bd92de5d3ace' # Cookie
    #dfp = ''
    bop = '{"version":"10.0","dfp":"' + dfp + '"}'
    locale = 'zh_cn' # static
    prio = '%7B%22ff%22%3A%22f4v%22%2C%22code%22%3A2%7D' # {"ff":"f4v","code":2}
    k_ft1 = '706436220846084'
    k_ft4 = '1162183859249156'
    k_ft5 = '1' # static
    pck = P1
    k_err_retries = '0' # static or 0
    ut = '1' # static or 0
    up = ''
    qdy = 'a'
    qds = '0'

    url = 'tvid='+tvid+'&bid='+bid+'&vid='+vid+'&src='+src+'&vt='+vt+'&rs='+rs+'&uid='+uid+'&ori='+ori+'&ps='+ps+'&k_uid='+k_uid+'&pt='+pt+'&d='+d+'&s=&lid=&cf=&ct=&authKey='+authKey+'&k_tag='+k_tag+'&ost='+ost+'&ppt='+ppt+'&dfp='+dfp+'&locale='+locale+'&prio='+prio+'&pck='+pck+'&k_err_retries='+k_err_retries+'&up=&qd_v='+qd_v+'&tm='+tm+'&qdy='+qdy+'&qds='+qds+'&k_ft1='+k_ft1+'&k_ft4='+k_ft4+'&k_ft5='+k_ft5+'&bop='+urllib.parse.quote(bop)+'&ut='+ut
    vf = getVF("/dash?"+url)
    finalurl = baseurl + url + '&vf=' + vf
    return finalurl

def getM3U8(url, bid):
    response = requests.get(url)
    resultJson = json.loads(response.content.decode('utf-8'))
    for index in range(len(resultJson['data']['program']['video'])):
        if resultJson['data']['program']['video'][index]['bid'] == int(bid) and 'scrsz' in resultJson['data']['program']['video'][index]:
            m3u8 = resultJson['data']['program']['video'][index]['m3u8']
            with open('/tmp/tmp.m3u8', "w") as f:
                f.write(m3u8)
            f.close()
    return m3u8

def getVideoDetail(tvid):
    url = 'https://pcw-api.iqiyi.com/video/video/baseinfo/' + str(tvid)
    response = requests.get(url)
    result = response.content.decode('utf-8')
    resultJson = json.loads(result)
    name = resultJson['data']['subtitle']
    duration = resultJson['data']['durationSec']
    return name, duration

def getAuth(name, tm, rand, uid):
    key = ""
    m = hashlib.md5()
    #print(f"/{name}-{tm}-{rand}-{uid}-{key}")
    m.update(f"/{name}-{tm}-{rand}-{uid}-{key}".encode("utf-8"))
    return m.hexdigest()

def getRandom():
    s = ""
    for i in  range(32):
        s += random.choice('abcdef1234567890')
    return s

def getURL(name, ip):
    url = ""
    tm = str(int(time.time()) + 3600)
    rand = getRandom()
    uid = hashlib.md5((ip+tm).encode("utf-8")).hexdigest()
    auth = getAuth(name, tm, rand, uid)
    finalurl = f"{url}{name}?auth_key={tm}-{rand}-{uid}-{auth}"
    #print(finalurl)
    return finalurl

def up2OSS(name):
    auth = oss2.Auth('', '')
    bucket = oss2.Bucket(auth, '', '')
    bucket.put_object_from_file(name, f'/tmp/tmp.m3u8')
    return bucket.object_exists(name)

def querydata2json(data):
    MUST = ["id"]
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
            ERR_INFO = {"Status":"False", "Message": "缺少必要参数，请参考接口文档，确认必要参数", "Info": "https://doc.api.telecom.ac.cn/"}
            start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
            return json.dumps(ERR_INFO, ensure_ascii=False)
        id = str(query_data["id"])

        if "p1" in query_data:
            P1 = query_data["p1"]
        else:
            P1 = ""

        if "p3" in query_data:
            P3 = query_data["p3"]
        else:
            P3 = ""

        if "qua" in query_data:
            qua = query_data["qua"].split(',')
        else:
            qua = ["0", "1", "2", "3"]

        videourl = f"https://www.iqiyi.com/v_{id}.html"
        info = getVideoInfo(videourl)
        tvid = info[0]
        vid = info[1]

        bidarr = ["200", "300", "500", "600"]
        quaarr = ['360P', '480P', '720P', '1080P']
        urlarr = {"Status": "True", "UUID": request_id, 'VideoName':'', 'VideoLen':'', }
        detail = getVideoDetail(tvid)
        urlarr['VideoName'] = detail[0]
        urlarr['VideoLen'] = str(detail[1])
        for index in range(len(qua)):
            bid = bidarr[int(qua[index])]
            downurl = getUrl(tvid, vid, bid, P1, P3)
            getM3U8(downurl, bid)
            name = getRandom().upper()+".m3u8"
            up2OSS(name)
            url = getURL(name, environ['REMOTE_ADDR'])
            urlarr[quaarr[int(qua[index])]] = url
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return json.dumps(urlarr, ensure_ascii=False)
    except Exception as r:
        outjson = {"Status": "False", "Message": "未知错误，请参考错误信息，定位原因，或联系作者", "Info": r}
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return json.dumps(outjson, ensure_ascii=False)
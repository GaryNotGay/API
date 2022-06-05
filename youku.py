import time
import json
import requests
import urllib.parse

def getTM():
    return str(int(time.time() * 1000))

def getSign(data):
    url = 'https://api.telecom.ac.cn/youkusign'
    sign = requests.get(url=url, data=data)
    #print(sign.content.decode('utf-8'))
    return str(sign.content.decode('utf-8'))

def getM3U8(vid, _m_h5_tk, _m_h5_tk_enc, cna, ckey):
    cookie = {'_m_h5_tk': _m_h5_tk,
              '_m_h5_tk_enc': _m_h5_tk_enc}

    jsv='2.6.1'
    appKey='24679788'
    api='mtop.youku.play.ups.appinfo.get'
    v = "1.1"
    timeout='15000'
    AntiFlood='true'
    AntiCreep='true'
    type='jsonp'
    dataType='jsonp'
    callback='mtopjsonp1'

    t = getTM()
    steal_params = {"ccode":"0502","client_ip":"192.168.1.1","utid":cna,"client_ts":t[0:10],"version":"4.0.76","ckey":ckey}
    biz_params = {"vid": vid, "current_showid":"461677", "preferClarity":5, "media_type": "standard,subtitle", "app_ver": "4.0.76", "extag": "EXT-X-PRIVINF", "play_ability":16782592, "master_m3u8":1, "drm_type":19, "key_index": "web01", "encryptR_client": "yBj8F8UD1reCWzQ44qVuLg==","local_vid": vid, "skh":1}
    ad_params = {"vs":"1.0","pver":"4.0.76","sver":"2.0","site":1,"aw":"w","fu":0,"d":"0","bt":"pc","os":"win","osv":"10","dq":"auto","atm":"","partnerid":"null","wintype":"interior","isvert":0,"vip":0,"emb":"","p":1,"rst":"mp4","needbf":2,"avs":"1.0"}
    data = {"steal_params":str(steal_params).replace('\'', r'\"'), "biz_params":str(biz_params).replace('\'', r'\"'), "ad_params":str(ad_params).replace('\'', r'\"')}
    data = str(data).replace('\'', r'"').replace('\\\\', '\\').replace(" ","")
    sign = getSign(cookie["_m_h5_tk"].split('_')[0]+"&"+t+"&"+appKey+"&"+data)
    url = f'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/?jsv={jsv}&appKey={appKey}&t={t}&sign={sign}&api={api}&v={v}&timeout={timeout}&AntiFlood={AntiFlood}&AntiCreep={AntiCreep}&type={type}&dataType={dataType}&callback={callback}&data='+urllib.parse.quote(data)
    #print(url)
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'
    header = {'User-Agent': UA, 'Referer': 'https://v.youku.com/'}
    response = requests.get(url=url, headers=header, cookies=cookie)
    rj = json.loads(response.content.decode('utf-8')[12:-1])
    return rj

def quacheck(quacur, quarr):
    for i in range(len(quarr)):
        if quacur.find("mp4"+quarr[i]) != -1:
            return True
    return False

def querydata2json(data):
    MUST = ["vid", "_m_h5_tk", "_m_h5_tk_enc", "cna"]
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
    vid = query_data["vid"]
    cna = query_data["cna"]
    _m_h5_tk = query_data["_m_h5_tk"]
    _m_h5_tk_enc = query_data["_m_h5_tk_enc"]
    ckey = ''

    if "qua" in query_data:
        qua = query_data["qua"]
    else:
        qua = "sd,hd,hd2,hd3"

    data = getM3U8(vid, _m_h5_tk, _m_h5_tk_enc, cna, ckey)
    if data["ret"][0] == "SUCCESS::调用成功":
        json_outstr = {
                "VideoName": "",
                "VideoLength": "",
                "VideoUrl":""
            }
        json_outstr['VideoLength'] = data["data"]["data"]["video"]["seconds"]
        json_outstr['VideoName'] = data["data"]["data"]["video"]["title"]
        quaarr = qua.split(",")
        videoarr = []
        for i in range(len(data["data"]["data"]["stream"])):
            videot = {
                "url": "",
                "qua": "",
                "drm": "",
            }
            if data["data"]["data"]["stream"][i]["media_type"] == "standard":
                videot["url"] = data["data"]["data"]["stream"][i]["m3u8_url"]
                videot["qua"] = str(data["data"]["data"]["stream"][i]["width"])+"*"+str(data["data"]["data"]["stream"][i]["height"])+"_"+data["data"]["data"]["stream"][i]["stream_type"]
                videot["drm"] = data["data"]["data"]["stream"][i]["drm_type"]
            if data["data"]["data"]["stream"][i]["stream_type"] != "auto" and quacheck(data["data"]["data"]["stream"][i]["stream_type"], quaarr):
                videoarr.append(videot)
        json_outstr['VideoUrl'] = videoarr

        #print(json_outstr)
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return str(json_outstr)
        
    else:
        err = {"Message": "", "Desc": "非法令牌=Cookie错误，其他错误信息请联系作者"}
        err["Message"] = data["ret"][0]

        #print(err)
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return str(err)

import json
import requests
requests.packages.urllib3.disable_warnings()

def api_get(id_):
    api_url = f"https://web-play.pptv.com/webplay3-0-{id_}.xml?o=0&version=6&type=mhpptv&appid=pptv.web.h5&appplt=web&appver=4.0.7&cb=a"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    s = requests.get(api_url, verify=False, headers=headers)
    data = json.loads(s.text[2:-4])
    return data


def outJSON(qua, data):
    try:
        name = data['childNodes'][2]['nm']
        dur = data['childNodes'][2]['dur']
    except Exception:
        name = data['childNodes'][0]['nm']
        dur = data['childNodes'][0]['dur']

    json_outstr = {
        "VideoName": "",
        "VideoLength": "",
    }
    json_outstr['VideoLength'] =dur
    json_outstr['VideoName'] = name

    quarr = qua.split(",")
    for index in range(len(quarr)):
        try:
            q = int(quarr[index])
            vh = data['childNodes'][q*2+4]['vh']
            vw = data['childNodes'][q*2+4]['vw']
            hw = str(vw)+"*"+str(vh)
            rid = data['childNodes'][q*2+4]['rid'][:-4]
            kk = data['childNodes'][q*2+3]['childNodes'][-1]['childNodes'][0].split('%26')[0]
            m3u8url = f"https://ksyun.vod.pptv.com/{rid}.m3u8?fpp.ver=1.0.0&k={kk}&type=mhpptv&o=0&sv=4.1.18"
            if hw in json_outstr.keys():
                hw += "_high"
            json_outstr[hw]=m3u8url
        except:
            return  json_outstr
    return  json_outstr

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
        qua = "0,1,2,3,4"

    data = api_get(cid)
    outjson = outJSON(qua, data)
    start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
    return str(outjson)
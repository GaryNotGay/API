import os
import re
import oss2
import json
import time
import glob
import m3u8
import random
import base64
import hashlib
import requests
from urllib import parse
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from concurrent.futures import ThreadPoolExecutor

def AESDecrypt(cipher_text, key, iv):
    cipher_text = pad(data_to_pad=cipher_text, block_size=AES.block_size)
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    cipher_text = aes.decrypt(cipher_text)

    return cipher_text

def getMP3(path, url):
     playlist = m3u8.load(uri=url)
     
     key = requests.get(playlist.keys[-1].uri).content
     iv = binascii.a2b_hex(playlist.keys[-1].iv[2:])

     with ThreadPoolExecutor(max_workers=100) as pool:
          for seg in playlist.segments:
               u = seg.uri
               n = "{:0>5}".format(u.split("/")[-1][3:])
               pool.submit(getTS, path+"/"+n, u, key, iv)

     
     files = glob.glob(os.path.join(path, '*.ts'))
     filea = []
     for file in files:
         filea.append(file)
     filea.sort()
     with open(path+"/tmp.ts", 'wb+') as fw:
            for i in range(len(filea)):
               file = filea[i]
               with open(file, 'rb') as fr:
                    fw.write(fr.read())
               fr.close()
     fw.close()
     os.system("ffmpeg -i "+path+"/tmp.ts"+" -c copy "+path+"/out.m4a")

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
    bucket.put_object_from_file(name, f'/tmp/out.m4a')
    return bucket.object_exists(name)

def getTS(path, url, key, iv):
     with open(path, 'wb') as f:
          ts = requests.get(url).content
          dets = AESDecrypt(ts, key=key, iv=iv)
          f.write(dets)
     f.close()

def querydata2json(data):
    MUST = ["date"]
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
        date = query_data["date"]

        tm1 = int(time.mktime(time.strptime(date, "%Y%m%d")))-28800
        tm2 = int(time.mktime(time.strptime(str(int(date)+1), "%Y%m%d")))-28800

        u = "https://www.dedao.cn/pc/bauhinia/pc/class/purchase/article_list"
        d = {"chapter_id":"",
            "count":30,
            "detail_id":"5L9DznlwYyOVdwasGdKmbWABv0Zk4a",
            "include_edge":"false",
            "is_unlearn":"false",
            "max_id":0,
            "max_order_num":0,
            "reverse":"true",
            "since_id":0,
            "since_order_num":0,
            "unlearn_switch":"false"
            }
        r = requests.post(url=u, data=d)
        rj = json.loads(r.content.decode("utf-8"))
        title = ""
        dura = ""
        url = ""
        for i in range(len(rj["c"]["article_list"])):
            if rj["c"]["article_list"][i]["publish_time"] >= tm1 and rj["c"]["article_list"][i]["publish_time"] < tm2 :
                title = date + "_" + rj["c"]["article_list"][i]["recommend_title"]
                dura = rj["c"]["article_list"][i]["audio"]["duration"]
                url = rj["c"]["article_list"][i]["audio"]["mp3_play_url"]
        if url != "":
            getMP3("/tmp", url)
            name = getRandom().upper()+".m4a"
            up2OSS(name)
            m4aurl = getURL(name, environ['REMOTE_ADDR'])
        else:
            m4aurl = ""

        outjson = {"Status": "True", "UUID": request_id, 'AudioName':title, 'AudioLen':dura, 'AudioUrl':url, 'M4AUrl':m4aurl}
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return json.dumps(outjson, ensure_ascii=False)

    except Exception as e:
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        outjson = {"Status": "False", "Message": "未知错误，请参考错误信息，定位原因，或联系作者", "Info": str(e), "UUID": request_id}
        return json.dumps(outjson, ensure_ascii=False)
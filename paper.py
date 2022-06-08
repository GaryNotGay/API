import os
import oss2
import time
import fitz
import json
import pyDes
import base64
import PyPDF2
import random
import hashlib
import pikepdf
import binascii
import requests
import urllib.parse
from pyDes import *

class RMRB:

    def getYMD(self):
        return time.strftime("%Y-%m/%d", time.localtime())

    def getLen(self, YMD):
        u = "http://paper.people.com.cn/rmrb/html/{}/nbs.D110000renmrb_01.htm".format(YMD)
        req = requests.get(u)
        req_str = str(req.content.decode('utf-8'))
        return req_str.count('版：')

    def rmrb(self, path, mode):
        if int(mode) == 0:
            date = getDate()
            YMD = self.getYMD()
        else:
            date = str(mode)
            YMD = time.strftime("%Y-%m/%d", time.strptime(date, "%Y%m%d"))

        print("Input Params: Path={path}, Date={date}".format(path=path, date=date))
        length = self.getLen(YMD)
        for index in range(length):
            if int(date) <= 20200630:
                u = "http://paper.people.com.cn/rmrb/page/{YMD}/{index:0>2d}/rmrb{date}{index:0>2d}.pdf".format(YMD=YMD, date=date, index=index+1)
            else:
                u = "http://paper.people.com.cn/rmrb/images/{YMD}/{index:0>2d}/rmrb{date}{index:0>2d}.pdf".format(YMD=YMD, date=date, index=index+1)
            downFile(u, path+"rmrb_"+str(date)+"_"+str(index+1)+".pdf")
        print("RMRB Down Complete!")
        if mergePDF(length, "rmrb_", path, date):
            print("RMRB Merge Complete!")

class BJYB:

    def getYMD(self):
        return time.strftime("%Y-%m/%d", time.localtime())

    def getHtml(self, YMD):
        u = "http://epaper.ynet.com/html/{}/node_1331.htm".format(YMD)
        req = requests.get(u)
        return str(req.content.decode('utf-8'))

    def bjyb(self, path, mode):
        if int(mode) == 0:
            date = getDate()
            YMD = self.getYMD()
        else:
            date = str(mode)
            YMD = time.strftime("%Y-%m/%d", time.strptime(date, "%Y%m%d"))

        print("Input Params: Path={path}, Date={date}".format(path=path, date=date))
        URL_LEN = 39
        req_str = self.getHtml(YMD)
        pdfnum = req_str.count('.pdf')
        start = 0
        for index in range(pdfnum):
            end = req_str.find('.pdf', start)
            baseurl = req_str[end-URL_LEN:end]
            start = end+4
            url = "http://epaper.ynet.com" + baseurl + ".pdf"
            downFile(url, path+"bjyb_"+str(date)+"_"+str(index+1)+".pdf")
        print("BJYB Down Complete!")
        if mergePDF(pdfnum, "bjyb_", path, date):
            print("BJYB Merge Complete!")
            for index in range(pdfnum):
                os.remove(path+"bjyb_"+str(date)+"_"+str(index+1)+".pdf")
            print("BJYB Delete Complete!")

class TTZB:
    def init2cipher(self, text):
        out_str = base64.b64decode(text)
        return str(out_str.hex())

    def unCompileCode(self, code):
        c = ""
        for index in range(len(code)):
            c += chr(ord(code[index]) - 1 ^ index)
        return c

    def DesECB(self, cipher, key):
        iv = ""
        k = des(key[0:8], ECB, iv, pad=None, padmode=PAD_PKCS5)
        de = k.decrypt(binascii.a2b_hex(cipher), padmode=PAD_PKCS5)
        return str(de)

    def getText(self, pdfID):
        u = "http://www.ttplus.cn/reader.html?pdfId=" + str(pdfID)
        c = {"SESSION": TTZB_COOKIE}
        r = requests.get(url=u, cookies=c)
        req = r.content.decode("utf-8")
        s = req.find("webViewerLoad")
        rearr = []
        e = req.find(";", s)
        st = req[s + 15:e - 2]
        starr = st.split(",")
        # print(starr[0][2:])
        rearr.append(starr[0][:-1])
        rearr.append(starr[1][2:])
        return rearr
        # return starr[1][2:]

    def getPDF(self, path, url, name):
        req = requests.get(url)
        # print(req.content)
        with open(path + name, "wb") as f:
            f.write(req.content)
        f.close()
        return True

    def dePDF(self, path, srcname, pwd):
        pdf = pikepdf.open(path + srcname, password=pwd[2:-1])
        pdf.save(path + "已解密 " + srcname)

    def getSign(self, kvs):
        VER = "_VER"
        VER_CURRENT_VAL = "1.0"
        SIGN_CURRENT_SECRET = "a7ff2586301b42eea962e9b9c8709689"
        nkvs = ""
        l = []
        kvs[VER] = VER_CURRENT_VAL
        for k in kvs:
            v = kvs[k]
            l.append(k + "=" + v + "&")
        l.sort(key=str.lower)
        nkvs += ''.join(l) + "key=" + SIGN_CURRENT_SECRET
        result = hashlib.md5(nkvs.encode('utf-8'))
        sign = str(result.hexdigest().upper())
        return sign

    def getParam(self, year, sign):
        # ttzb type=11
        # kvs = {"typeId": 11 ,"year": year, "pageSize": 30, "pagenum": 0, "_VER":1.0, "_SIGN":sign}
        st = "typeId=11&year=" + str(year) + "&pageSize=130&pagenum=0&_VER=1.0&_SIGN=" + sign
        return st

    def getAPI(self, param):
        # print(param)
        name = {}
        u = "https://api.ttplus.cn/h5/pdf/all"
        h = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
        r = requests.post(url=u, data=param, headers=h)
        # req = r.content.decode('utf-8')
        rj = r.json()
        for index in range(len(rj["content"]["newsdatas"])):
            id = rj["content"]["newsdatas"][index]["id"]
            title = rj["content"]["newsdatas"][index]["title"] + ".pdf"
            name[id] = title
        # print(rj["content"]["newsdatas"][0])
        return name

    def getOne(self, id):
        kvs = {"newspaperId": str(id), "userId": TTZB_USERID}
        sign = self.getSign(kvs)
        st = "newspaperId=" + str(id) + "&userId=" + str(TTZB_USERID) + "&_VER=1.0&_SIGN=" + sign
        u = "https://api.ttplus.cn/h5/pdf/one"
        h = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
        r = requests.post(url=u, data=st, headers=h)
        rj = r.json()
        name = rj["content"]["newspapertype"] + " " + rj["content"]["updatetime"] + ".pdf"
        # print(name)
        return name

    def ttzb(self, path, TTZB_PARAM):
        pdfID = TTZB_PARAM
        name = self.getOne(pdfID)
        rearr = self.getText(pdfID)
        text = rearr[1]
        cipher = self.init2cipher(text)
        key = self.unCompileCode(TTZB_CODE)
        pdfkey = self.DesECB(cipher, key)
        print("key:" + pdfkey)
        url = rearr[0]
        print("url:" + url)
        self.getPDF(path, url, name)
        print("TTZB Down Complete!")
        self.dePDF(path, name, pdfkey)
        #os.remove(path + name)
        os.rename(path + "已解密 "+ name, path + "tmp.pdf")
        print("TTZB Decrypt Complete!")

class ZQB:

    def getInkey(self, pid):
        u = "http://www.dooland.com/magazine/online_htm5.php?pid=" + str(pid)
        r = requests.get(url=u)
        res = r.content.decode("utf-8")
        s = res.find("data-inkey=")
        return res[s + 12:s + 44]

    def getDest(self, pid, inkey):
        u = "http://www.dooland.com/magazine/InterFace/s_EchoXml_Streamv2_htm5.php?pid=" + str(pid) + "&inkey=" + str(inkey) + "&uid=" + ZQB_UID
        h = {"cookies": ZQB_COOKIE}
        r = requests.get(url=u, headers=h)
        res = r.content.decode("utf-8")
        return str(res)

    def bingo_decode(self, dest, key):
        keyLength = len(key)
        keyArray = []
        for index in range(keyLength):
            keyArray.append((ord(key[index]) % 6))

        destTemp = "";
        for index in range(len(dest)):
            destTemp += (chr(ord(dest[index]) - keyArray[index % keyLength]))
        source = urllib.parse.unquote(destTemp)
        return source

    def src2url(self, source):
        urlArr = []
        start = 0
        num = int(int(source.count(".jpg")) / 2)
        for index in range(num):
            a = source.find('+src=', start)
            b = source.find('+ssrc=', start)
            start = b + 1
            # print(source[a+6: b-1])
            urlArr.append(source[a + 6: b - 1])
        return urlArr

    def getDate():
        return time.strftime("%Y%m%d", time.localtime())

    def getJPG(self, path, urlArr):
        print("ZQB Total " + str(len(urlArr)))
        for index in range(len(urlArr)):
            name = str(path + getDate()) + "_" + str(index + 1) + ".jpg"
            url = urlArr[index]
            req = requests.get(url)
            with open(name, "wb") as f:
                f.write(req.content)
            f.close()
            #print(name + " success")
        return True

    def JPG2PDF(self, path, num):
        for index in range(num):
            doc = fitz.open()
            img_file = path + getDate() + "_" + str(index+1) + ".jpg"
            imgdoc = fitz.open(img_file)
            pdfbytes = imgdoc.convert_to_pdf()
            pdf_name = path + getDate() + "_" + str(index+1) + ".pdf"
            imgpdf = fitz.open(pdf_name, pdfbytes)
            doc.insert_pdf(imgpdf)
            doc.save(path + "zqb_" + getDate() + "_" + str(index+1) + ".pdf")
            doc.close()
            os.remove(path + getDate() + "_" + str(index+1) + ".jpg")

    def getName(self, pid):
        u = "http://www.dooland.com/magazine/online_htm5.php?pid=" + str(pid)
        r = requests.get(url=u)
        res = r.content.decode("utf-8")
        s = res.find("<title>")
        e = res.find("电子杂志 - 读览天下")
        return res[s+7: e-1]

    def zqb(self, path, pid):
        key = self.getInkey(pid)
        dest = self.getDest(pid, key)
        source = self.bingo_decode(dest, key)
        urlArr = self.src2url(source)
        self.getJPG(path, urlArr)
        self.JPG2PDF(path, len(urlArr))
        print("ZQB Down Complete!")
        mergePDF(len(urlArr), "zqb_", path, getDate())

def getAuth(name, tm, rand, uid):
    key = "Li@oss.telecom.ac.cn1"
    m = hashlib.md5()
    #print(f"/{name}-{tm}-{rand}-{uid}-{key}")
    m.update(f"/{name}-{tm}-{rand}-{uid}-{key}".encode("utf-8"))
    return m.hexdigest()

def getRandom():
    s = ""
    for i in  range(32):
        s += random.choice('abcdefghijklmnopqrstuvwxyz1234567890')
    return s

def getDate():
    return time.strftime("%Y%m%d", time.localtime())

def downFile(url, name):
    req = requests.get(url)
    #print(req.content)
    with open(name, "wb") as f:
        f.write(req.content)
    f.close()
    return True

def mergePDF(length, type, path, date):
    file_merger = PyPDF2.PdfFileMerger(strict=False)
    #if type == "rmrb":
    for index in range(length):
        filename = path+type+str(date)+"_"+str(index+1)+".pdf"
        try:
            file_merger.append(filename)
        except:
            continue
    file_merger.write(path+"tmp"+".pdf")
    file_merger.close()
    return True

def up2OSS(name):
    auth = oss2.Auth('', '')
    bucket = oss2.Bucket(auth, '', '')
    bucket.put_object_from_file(name, '/tmp/tmp.pdf')
    return bucket.object_exists(name)

def getURL(name, ip):
    url = "https://oss.telecom.ac.cn/"
    tm = str(int(time.time()) + 3600)
    rand = getRandom()
    #ip = environ['REMOTE_ADDR']
    uid = hashlib.md5((ip+tm).encode("utf-8")).hexdigest()
    auth = getAuth(name, tm, rand, uid)
    finalurl = f"{url}{name}?auth_key={tm}-{rand}-{uid}-{auth}"
    #print(finalurl)
    return finalurl

def querydata2json(data):
    MUST = ["pid", "ptype"]
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
    global TTZB_CODE
    global TTZB_USERID
    global TTZB_COOKIE
    global ZQB_UID
    global ZQB_COOKIE

    try:
        query_data = querydata2json(environ['QUERY_STRING'])
        if query_data == "ERR":
            ERR_INFO = {"Status":"False", "Message": "缺少必要参数，请参考接口文档，确认必要参数", "Info": "https://doc.api.telecom.ac.cn/"}
            start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
            return json.dumps(ERR_INFO, ensure_ascii=False)
        pid = str(query_data["pid"])
        ptype = str(query_data["ptype"])

        PATH = '/tmp/'
        url = ""
        outname = ""
        if ptype == "1":
            outname = f"RMRB-{pid}"
            rmrb = RMRB()
            rmrb.rmrb(PATH, pid)
        elif ptype == "2":
            outname = f"BJYB-{pid}"
            bjyb = BJYB()
            bjyb.bjyb(PATH, pid)
        elif ptype == "3":
            ttzb = TTZB()
            TTZB_CODE = "rayux~ddl|m~"
            if "pid" in query_data:
                TTZB_USERID = query_data["pid"]
            else:
                TTZB_USERID = ""
            if "pcookie" in query_data:
                TTZB_COOKIE = query_data["pcookie"]
            else:
                TTZB_COOKIE = ""
            outname = ttzb.getOne(pid)[:-4]
            ttzb.ttzb(PATH, pid)
        elif ptype == "4":
            zqb = ZQB()
            if "pid" in query_data:
                ZQB_UID = query_data["pid"]
            else:
                ZQB_UID = ""
            if "pcookie" in query_data:
                ZQB_COOKIE = query_data["pcookie"]
            else:
                ZQB_COOKIE = ""
            ZQB_COOKIE = "auth="+ZQB_COOKIE
            outname = zqb.getName(pid)
            zqb.zqb(PATH, pid)

        filetype = ".pdf"
        name = getRandom().upper()[0:16] + filetype
        if up2OSS(name):
            url = getURL(name, environ['REMOTE_ADDR'])

        outjson = {"Status":"True", "PaperName":outname, "PaperUrl":url}
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return json.dumps(outjson, ensure_ascii=False)
    except Exception as r:
        outjson = {"Status": "False", "Message": "未知错误，请参考错误信息，定位原因，或联系作者", "Info": r}
        start_response('200 OK', [('Content-type', 'application/json; charset=utf-8'), ('Access-Control-Allow-Origin', '*')])
        return json.dumps(outjson, ensure_ascii=False)

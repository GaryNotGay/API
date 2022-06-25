# API 接口文档    
    
Author  :  lijishi    
Contact :  lijishi@163.com    
License :  GNU GENERAL PUBLIC LICENSE Version 3    
    
## 1、接口地址 & 代码开源     
    
#### API：https://api.telecom.ac.cn/    
#### APICDN：https://cdn.api.telecom.ac.cn/     
#### APIDOC：https://doc.api.telecom.ac.cn/     
#### Github：https://github.com/GaryNotGay/API    
#### Gitee：https://gitee.com/garynotgay/api    
    
## 2、开发文档    
    
#### 2.1 MangoTV    
请求路径：https://api.telecom.ac.cn/mango    
请求方式：GET    
正确返回：{"Status":"True", "VideoName": "", "VideoTitle": "", "VideoLength": "", "标清/高清/超清/蓝光": ""}    
错误返回：{"Status":"False", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：MGTV视频解析M3U8    
请求示例：https://api.telecom.ac.cn/mango?id=16322652&title=446003&qua=1    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| id | 是 | 16322652 | https://www.mgtv.com/b/[title]/[id].html |
| title | 是 | 446003 | https://www.mgtv.com/b/[title]/[id].html |
| qua | 否 | 1,2,3 | 可选视频质量，360P(0)，540P(1)，720P(2)，1080P(3)，默认全选，英文逗号分隔 |
| hdcn | 否 | xxxxxxxxxxxxxxxxxx-xxxxxxxxx | 从WEB中获取，携带此参数可获取会员视频及1080P清晰度，默认为空 |
    
#### 2.2 Ckey7x    
请求路径：https://api.telecom.ac.cn/ckey7x    
请求方式：GET    
正确返回：{"Status":"True", "VER":"CKEY7", "KEY":""}    
错误返回{"Status":"False", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：TX视频请求参数校验算法    
代码参考：https://www.jianshu.com/p/75619f7e3956    
请求示例：https://api.telecom.ac.cn/ckey7x?platform=40201&vid=100701&sdt=v1010&tm=1651217559&ver=7.1    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| platform | 是 | 40201 | 请求参数之一 |
| vid | 是 | 100701 | 视频vid |
| sdt | 是 | v1010 | 请求参数之一 |
| tm | 是 | 1651217559 | 10位时间戳 |
| ver | 是 | 7.1 | 7.x，其中x为周几 |
    
#### 2.3 Ckey81    
请求路径：https://api.telecom.ac.cn/ckey81    
请求方式：GET    
正确返回：{"Status":"True", "VER":"CKEY8", "KEY":""}    
错误返回：{"Status":"False", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：TX视频请求参数校验算法    
代码参考：https://www.pohaier.com/2018/12/22/227.html    
请求示例：https://api.telecom.ac.cn/ckey81?vid=i0037ryjlwn&time=1623678055&guid=6eb81823f6e496f9a87c88fbe977dee0&platform=4830201&url=https://wetv.vip    


| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| platform | 是 | 40201 | 请求参数之一 |
| vid | 是 | i0037ryjlwn | 视频vid |
| guid | 是 | 6eb81823f6e496f9a87c88fbe977dee0 | 请求参数之一 |
| time | 是 | 1651217559 | 10位时间戳 |
| url | 是 | https://wetv.vip | 请求参数之一 |
    
#### 2.4 Ckey91        
请求路径：https://api.telecom.ac.cn/ckey91    
请求方式：GET    
正确返回：{"Status":"True", "VER":"CKEY9", "KEY":"" , "navigator":{"userAgent":"","appCodeName":"","appName":"","platform":""}}    
错误返回：{"Status":"False", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：TX视频请求参数校验算法    
代码参考：https://github.com/ZSAIm/iqiyi-parser/blob/master/js/tencent.js    
请求示例：https://api.telecom.ac.cn/ckey91?   platform=10201&appver=3.5.57&vid=j002024w2wg&guid=1fcb9528b79f2065c9a281a7d554edd1&tm=1556617308&url=https://wetv.vip    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| platform | 是 | 10201 | 请求参数之一 |
| appver | 是 | 3.5.57 | 请求参数之一 |
| vid | 是 | j002024w2wgguid | 视频vid |
| guid | 是 | 1fcb9528b79f2065c9a281a7d554edd1 | 请求参数之一 |
| tm | 是 | 1651217559 | 10位时间戳 |
| url | 是 | https://wetv.vip | 请求参数之一 |
    
#### 2.5 cmd5x    
请求路径：https://api.telecom.ac.cn/cmd5x    
请求方式：GET    
正确返回：{"Status":"True", "VER":"CMD5X", "KEY":""}    
错误返回：{"Status":"False", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：IQIYI视频请求参数校验算法    
请求示例：https://api.telecom.ac.cn/cmd5x?param=aXFpeWlwYXJhbQ==    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| param | 是 | iqiyiparam | dash请求参数base64格式 |
    
#### 2.6 PPTV    
请求路径：https://api.telecom.ac.cn/pptv    
请求方式：GET    
正确返回：{"Status":"True", "VideoName":"", "VideoLength":"", "[width*high]": ""}    
错误返回：{"Status":"False", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：PPTV视频解析M3U8    
请求示例：https://api.telecom.ac.cn/pptv?cid=26311295&qua=3,4    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| cid | 是 | 26311295 | PPTV视频id，获取方法自行探索 |
| qua | 否 | 3,4 | 可选视频质量，270P(0)，480P(1)，720P(2)，1080P(3)，1080P高码(4)，默认全选，英文逗号分隔 |
    
#### 2.7 qqsport    
请求路径：https://api.telecom.ac.cn/qqsport    
请求方式：GET    
正确返回：{"Status":"True", "LiveName":"", "LiveCommentator":"", "Url": ""}    
错误返回：{"Status":"False", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：TX体育直播解析M3U8    
请求示例：https://api.telecom.ac.cn/qqsport?mid=208:2288013&qua=1    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| mid | 是 | 208:2288013 | TX体育直播id |
| qua | 否 | 3,4 | 可选视频质量，270P(0)，480P(1)，720P(2)，1080P(3)，默认1080P，只可单选 |
| openid | 否 | xxxxx | TX体育cookie，要求三参数匹配 |
| appid | 否 | xxxxx | TX体育cookie，要求三参数匹配 |
| token | 否 | xxxxx | TX体育cookie，要求三参数匹配 |
    
#### 2.8 migu    
请求路径：https://api.telecom.ac.cn/migu    
请求方式：GET    
正确返回：{"Status":"True", "VideoName":"", "VideoLength":"", "VideoUrl": "[{"TrySee":"", "rateDesc":"", "url":"", "videoCoding":""}]"}    
错误返回：{"Status":"False", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：MIGU视频解析M3U8    
请求示例：https://api.telecom.ac.cn/migu?qua=2,3,4,6,8&cid=732903127    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| cid | 是 | 732903127 | MIGU视频id |
| qua | 否 | 3,4 | 可选视频质量，可选范围1-10，已知540P(2)，720P(3)，1080P(4)，原画4K(6)，原画HDR(7)，超清4K(8)，默认2,3,4，大于等于1080P清晰度均需cookie，否则返回试播链接 |
| userId | 否 | xxxxx | MIGU视频cookie，要求两参数匹配 |
| userToken | 否 | xxxxx | MIGU视频cookie，要求两参数匹配 |
    
#### 2.9 yksign    
请求路径：https://api.telecom.ac.cn/yksign    
请求方式：GET    
正确返回：{"Status":"True", "VER":"YOUKU", "KEY":""}    
错误返回：{"Status":"False", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：YK视频请求参数校验算法    
代码参考：https://blog.csdn.net/weixin_41813169/article/details/109815414    
请求示例：https://api.telecom.ac.cn/yksign    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| data | 是 | xxxxxx | 请求参数，通过body传递 |
        
#### 2.10 youku    
请求路径：https://api.telecom.ac.cn/youku    
请求方式：GET    
正确返回：{"Status":"True", "VideoName":"", "VideoLength":"", "VideoUrl": "[{"qua":"", "url":"", "drm":""}]"}    
错误返回：{"Status":"False", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：YK视频解析M3U8    
请求示例：https://api.telecom.ac.cn/youku?vid=XNTg2MDM3NjQzMg==&_m_h5_tk=xxx&_m_h5_tk_enc=xxx&cna=xxx&qua=hd3    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| vid | 是 | XNTg2MDM3NjQzMg== | YK视频vid，v.youku.com/v_show/id_[VID].html |
| cna | 否 | xxxxx | YK视频cookie，要求三参数匹配 |
| _m_h5_tk | 否 | xxxxx | YK视频cookie，要求三参数匹配 |
| _m_h5_tk_enc | 否 | xxxxx | YK视频cookie，要求三参数匹配 |
| qua | 否 | hd2,hd3 | 可选视频质量，360P(sd)，540P(hd)，720P(hd2)，1080P(hd3)，默认全选 |
    
#### 2.11 ykr1    
请求路径：https://api.telecom.ac.cn/ykr1    
请求方式：GET    
正确返回：{"Status":"True", "VER":"YKR1", "R1":"",  "encryptR":""}    
错误返回：{"Status":"False", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：YK视频copyrightDRM关键参数    
请求示例：https://api.telecom.ac.cn/ykr1    
    
#### 2.12 paper    
请求路径：https://api.telecom.ac.cn/paper    
请求方式：GET    
正确返回：{"Status":"True", "PaperName": "", "PaperUrl": ""}    
错误返回：{"Status":"False", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：解析多种报刊链接    
请求示例：https://api.telecom.ac.cn/paper?ptype=1&pid=20220608    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| ptype | 是 | 1 | RMRB(1)，BJYB(2)，TTZB(3)，DLTX(4) |
| pid | 是 | 1/427369/MzAxMzAy | ptype为1/2时，pid应为八位数字日期，ptype为3/4时，为阅读界面的id |
| puser | 否 | xxxxx | ptype为3/4时，需要具有阅读权限的cookie，ptype=3，puser=userId，ptype=4，puser=uid |
| pcookie | 否 | xxxxx | ptype为3/4时，需要具有阅读权限的cookie，ptype=3，pcookie=SESSION，pcookie=auth |
    
#### 2.13 wetvsub    
请求路径：https://api.telecom.ac.cn/wetvsub    
请求方式：GET    
正确返回：{"Status":"True", "VideoName":"", "VideoSub":"[{"url":"", "lang":"", "name":""}]", "[VideoSubZip]":""}    
错误返回：{"Status":"False", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：WETV多语字幕解析    
请求示例：https://api.telecom.ac.cn/wetvsub?vid=i0037ryjlwn&zip=1&lang=zh    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| vid | 是 | i0037ryjlwn | WETV视频id |
| zip | 否 | 1 | 可选是否打包为zip文件，1为是，其他为否，默认为否，选择是时返回字段VideoSubZip |
| lang | 否 | zh | 可选zip文件命名语言，zh为中文，en为英文，默认为英文，仅在zip=1时生效 |
    
#### 2.14 ximalaya    
请求路径：https://api.telecom.ac.cn/ximalaya    
请求方式：GET    
正确返回：{"Status":"True", "UUID":"", "AudioName":"", "AudioLen":"", "AudioUrls":"[{"type":"", "url":""}]"}    
正确返回：{"Status":"True", "UUID":"", "AlbumName":"", "TrackTotalNum":"", "AlbumUrls":"[{"index":"", AudioName":"", "AudioLen":"", "AudioUrls":"[{"type":"", "url":""}]"}]"}    
错误返回：{"Status":"False", "UUID":"", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：ximalaya音频解析    
请求示例：https://api.telecom.ac.cn/ximalaya?all=0&trackid=135045322&qua=0    
请求示例：https://api.telecom.ac.cn/ximalaya?all=1&albumid=30510905&qua=0    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| isall| 是 | 1 | 为1时表示全集，其他表示单集 |
| trackid | 否 | 135045322 | 音频单轨id，isall不为1时必选|
| albumid | 否 | 510905 | 音频专辑id，isall为1时必选 |
| toekn | 否 | dG9rZW4= | 网页cookie[1&_token]，base64加密 |
| qua | 否 | 1,2 | 可选音频质量，M4A_64(0), MP3_64(1), M4A_24(2), MP3_32(3), AAC_24(4)，默认全选 |
    
#### 2.15 qq    
请求路径：https://api.telecom.ac.cn/qq    
请求方式：GET    
正确返回：{"Status":"True", "UUID":"", "VideoName":"", "VideoLen":"", "270P/540P/720P/1080P":""}    
错误返回：{"Status":"False", "UUID":"", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：TX视频解析    
请求示例：https://api.telecom.ac.cn/qq?vid=h0043gj0gds&coverid=mzc0020072xuxyu&qua=3    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| vid| 是 | h0043gj0gds | TX视频vid |
| coverid | 是 | mzc0020072xuxyu | TX视频coverid |
| toekn | 否 | dG9rZW4= | 网页cookie，base64加密，标准格式{"main_login":"","vqq_openid":"","vqq_appid":"","vqq_access_token":"","vqq_vuserid":"","vqq_vusession":""} |
| qua | 否 | 1,2 | 可选视频质量，270P(0), 540P(1), 720P(2), 1080P(3)，默认全选 |
    
#### 2.15 iqiyi    
请求路径：https://api.telecom.ac.cn/iqiyi    
请求方式：GET    
正确返回：{"Status":"True", "UUID":"", "VideoName":"", "VideoLen":"", "360P/540P/720P/1080P":""}    
错误返回：{"Status":"False", "UUID":"", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：IQIYI视频解析    
请求示例：https://api.telecom.ac.cn/iqiyi?id=1ezb353qy5c&qua=3    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| id| 是 | 1ezb353qy5c | IQIYI视频网页id，v_xxxxxxxxxxx |
| p1 | 否 | xxxx | IQIYI视频cookie，P1和P3相匹配 |
| p3 | 否 | xxxx | IQIYI视频cookie，P1和P3相匹配 |
| qua | 否 | 1,2 | 可选视频质量，360P(0), 540P(1), 720P(2), 1080P(3)，默认全选 |
    
#### 2.16 oneword    
请求路径：https://api.telecom.ac.cn/oneword    
请求方式：GET    
正确返回：{"Status":"True", "UUID":"", "ID": "", "hitokoto": "", "type": "", "from": "", "Origin": "https://hitokoto.cn/"}    
错误返回：{"Status":"False", "UUID":"", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：一言·闪光一句    
代码参考：https://hitokoto.cn/    
请求示例：https://api.telecom.ac.cn/oneword?id=1111    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| id | 否 | 1111 | 一言数据库句子ID，可指定返回该句子，默认随机 |
| typeid | 否 | a | 一言数据库类型ID，可指定返回该类型句子，默认随机 |
    
#### 2.17 ykdrm    
请求路径：https://api.telecom.ac.cn/ykdrm    
请求方式：GET    
正确返回：{"Status":"True","VER":"YKDRM","KEY":{"HEX":"","BASE64":""}}    
错误返回：{"Status":"False", "UUID":"", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：YK自研DRM三参数生成KEY    
请求示例：https://api.telecom.ac.cn/ykdrm?param=MSwxLDE=    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| param | 是 | MSwxLDE= | R1,encryptR_server,copyright_key base64编码 |
    
#### 2.18 qqsportreplay    
请求路径：https://api.telecom.ac.cn/qqsportreplay    
请求方式：GET    
正确返回：https://v.qq.com/x/cover/xxxxx.html    
错误返回：{"Status":"False", "UUID":"", "Message":"[Error Message]", "Info":"[Error Info]"}    
接口说明：TX体育回放跳转TX视频    
请求示例：https://api.telecom.ac.cn/qqsportreplay?mid=100002:20244584    

| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| mid | 是 | 100002:20244584 | TX体育mid |
    
## 3、注意事项    
    
##### 项目仅为个人学习，请勿用于非法用途    
    
##### 如有侵权，非常抱歉，请联系作者删除    
    
##### 接口仅为自用测试，不保证任何可用性    

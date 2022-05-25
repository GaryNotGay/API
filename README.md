# API 接口文档        
Author  :  lijishi    
Contact :  lijishi@163.com    
License :  GNU GENERAL PUBLIC LICENSE Version 3    

## 1、接口地址 & 代码开源     
#### API：https://api.telecom.ac.cn/    
#### APICDN：https://cdn.api.telecom.ac.cn/ （暂未上线）    
#### APIDOC：https://doc.api.telecom.ac.cn/ （暂未上线）    
#### Github:    
#### Gitee:https://gitee.com/garynotgay/api    

## 2、开发文档    
#### 2.1 MangoTV    
路径：https://api.telecom.ac.cn/mango    
示例：https://api.telecom.ac.cn/mango?id=16322652&title=446003&qua=1    
    
| 参数 | 必选 | 示例 | 说明 |
| --- | --- | --- | --- |
| id | 是 | 16322652 | https://www.mgtv.com/b/[title]/[id].html |
| title | 是 | 446003 | https://www.mgtv.com/b/[title]/[id].html |
| qua | 否 | 1,2,3 | 可选视频质量，0--360P，1--540P，2--720P，3--1080P（需要会员Cookie），默认全选 |
| hdcn | 否 | xxxxxxxxxxxxxxxxxx-xxxxxxxxx | 从WEB中获取，携带此参数可获取会员视频及1080P清晰度，默认为空 |

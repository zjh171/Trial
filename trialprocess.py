# coding=UTF-8

import re
import urllib
import urllib.request

from model import trial
from util import regulartool, dbhelper
from util import exejs

class BDTB:
    #初始化，传入基地址，是否只看楼主的参数
    def __init__(self,baseUrl):
        #base链接地址
        self.baseURL = baseUrl
        #HTML标签剔除工具类对象
        self.reTool = regulartool.RegularTool()
        #默认的标题
        self.defaultTitle = u"药监局审理药列表"
        self.one = dbhelper.DBHelper()
        self.exejs = exejs.ExeJs()
        self.paramsResponse = None

        self.header = {
            'Content-Type':'application/x-www-form-urlencoded',
            'Connection':'Keep-Alive',
            'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.4.4; HM NOTE 1S MIUI/V6.6.1.0.KHKCNCF)',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cache-Control':'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cookie': 'JSESSIONID=0001PZMkGqYh3qJBRdDWDaEbFNk:-69H35P'
            }

    def __del__(self):
         self.one.close()

    def getParams(self):
        if(None != self.paramsResponse):
            return self.paramsResponse
        url = 'http://sq.cfda.gov.cn/datasearch/SFDACoderServlet'
        params = {
            'colval': self.exejs.createCode()
        }
        params = urllib.parse.urlencode(params)
        params = params.encode('utf-8')

        request = urllib.request.Request(url, params,headers=self.header)
        response = urllib.request.urlopen(request)
        self.paramsResponse = response.read().decode('utf-8')
        return self.paramsResponse

    #获取页面数据
    def getPageInfo(self):
        try:
            #构建URL
            url = self.baseURL
            requestParams = self.getParams()
            params = {
                'code':requestParams[0],
                'ik': requestParams[1],
            }
            params = urllib.parse.urlencode(params)
            params = params.encode('utf-8')
            request = urllib.request.Request(url,None,headers= self.header)
            response = urllib.request.urlopen(request)
            #返回UTF-8格式编码内容
            return response.read().decode('utf-8')
        #无法连接，报错
        except urllib.request.URLError as e:
            if hasattr(e,"reason"):
                print(u"连接服务器失败",e.reason)
        return None


    #获取帖子标题
    def getTitle(self,pageInfo):
        #得到标题的正则表达式
        pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>',re.S)
        result = re.search(pattern,pageInfo)
        if result:
            #如果存在，则返回标题
            return result.group(1).strip()
        else:
            return self.defaultTitle

    #获取每一层楼的内容,传入页面内容
    def getContent(self,pageInfo):
        #匹配所有楼层的内容
        pattern = re.compile('<tr height="30">.*?</tr>|<tr bgcolor="#f5fafe" height="30">.*?</tr>',re.S)
        items = re.findall(pattern,pageInfo)
        contents = []
        for item in items:
            #将文本进行去除标签处理，同时在前后加入换行符
            print(self.getEveryItemInfo(item))
            content = "\n"+self.reTool.replace(item)+"\n"
            contents.append(content.encode('utf-8'))
        return contents

    '''
    每个itemInfo是这样的:
    <tr bgcolor="#f5fafe" height="30">

                                      <td align="center" bgcolor="#f5fafe" class="newsindex"> JXHR1700012</td>
                                      <td align="center" bgcolor="#f5fafe" class="newsindex"> 注射用甲泼尼龙琥珀酸钠</td>
                                      <td align="center" bgcolor="#f5fafe" class="newsindex"> 化药 </td>
                                      <td align="center" bgcolor="#f5fafe" class="newsindex"> 复审 </td>
                                      <td align="center" bgcolor="#f5fafe" class="newsindex">  </td>
                                      <td align="center" bgcolor="#f5fafe" class="newsindex"> / / 上海大陆药业有限公司 </td>
                                      <td align="center" bgcolor="#f5fafe" class="newsindex"> 2017-07-13 </td>
                                    </tr>
    '''

    def getEveryItemInfo(self,itemInfo):
        pattern = re.compile('<td .*?>.*?</td>',re.S)
        items = re.findall(pattern,itemInfo)
        tempTrial = trial.Trial()
        for item in items:
            content = self.reTool.replace(item)
            if(item == items[0]):
                tempTrial.trialId = content
            if(item == items[1]):
                tempTrial.mediName = content
            if (item == items[2]):
                tempTrial.mediSort = content
            if (item == items[3]):
                tempTrial.trialType = content
            if (item == items[4]):
                tempTrial.registerSort = content
            if (item == items[5]):
                tempTrial.companyName = content
            if (item == items[6]):
                tempTrial.startDate = content
        self.one.insertTrial(tempTrial)
        return None

    def setFileTitle(self,title):
        #如果标题不是为None，即成功获取到标题
        if title is not None:
            self.file = open(title + ".txt","w+")
        else:
            self.file = open(self.defaultTitle + ".txt","w+")

    def start(self):
        pageInfo = self.getPageInfo()
        print('90909090909',pageInfo)
        contents = self.getContent(pageInfo)

baseURL = 'http://sq.cfda.gov.cn/datasearch/schedule/search.jsp?tableId=43&tableName=TABLE43&columnName=COLUMN464,COLUMN475&title1=%E8%8D%AF%E5%93%81%E6%B3%A8%E5%86%8C%E8%BF%9B%E5%BA%A6%E6%9F%A5%E8%AF%A2'
print ("baseURL:%s",baseURL)
bdtb = BDTB(baseURL)
bdtb.start()






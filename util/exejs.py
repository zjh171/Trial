import os

import execjs


# 执行本地的js
class ExeJs:
    def createCode(self):
        currentDirectory = os.path.dirname(__file__)
        jsFilePath = os.path.dirname(currentDirectory) + '/resource/createcode.js'
        file = open(jsFilePath,'r',encoding='UTF-8')
        line = file.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = file.readline()

        ctx = execjs.compile(htmlstr)
        code = ctx.call("createCode")
        return code
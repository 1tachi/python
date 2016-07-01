#-*- coding:utf-8 -*-
import urllib2
import urllib
import re
import thread
import time

class QSBK:
    #初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER'
        #初始化headers
        self.headers = {'User-Agent':self.user_agent}
        #存放段子的变量，每一个元素是每一页段子
        self.stories = []
        #存放程序是否继续运行的变量
        self.enable = False

    #传入某一页的索引获得页面代码
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/%s/?s=4890680' %pageIndex
            #构建请求的request
            request = urllib2.Request(url,headers=self.headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #将页面转换为utf-8编码
            pageCode = response.read().decode("utf-8")
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"连接糗事百科失败，错误原因：",e.reason
                return None
    #传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败。。。。"
            return None
        reg = '<div class="content">(.*?)</div>'
        pattern = re.compile(reg,re.S)
        items = re.findall(pattern,pageCode)
        #用了存储每一页的段子
        pageStories = []
        #遍历正则表达式的匹配信息
        for item in items:
            #查看是否含有图片
            #haveImg = re.search("img",items[3])
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR,"\n",item)
            #items[0]是一个段子的发布者，item[1]是一个段子的内容，item[2]是发布时间，item[4]点赞数
            pageStories.append(text.strip())
            return pageStories
    #加载并提取页面的内容，加入列表
    def loadPage(self):
        #如果当前未看见的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                #获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                #将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    #获取完之后页码索引+1，表示下次读取一页
                    self.pageIndex += 1

    #调用该方法，每次敲回车键打印输出一个段子
    def getOneStory(self,pageStories,page):
        #遍历一页段子
        for story in pageStories:
            #等待用户输入
            input = raw_input("请按下回车键：")
            #每当用户输入一次回车，判断一下是否要加载新页面
            self.loadPage()
            #如果输入Q则退出程序
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t内容：\n%s" %(page,story)
    #开始方法
    def start(self):
        print u"正在读取糗事百科，按回车键查看新段子，Q退出"
        #使变量为Ture,程序可以正常进行
        self.enable = True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前读了几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                #从全局list中获取每一页段子
                pageStories = self.stories[0]
                #当前读到的页数+1
                nowPage += 1
                #将全局list中的第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowPage)


spider = QSBK()
spider.start()
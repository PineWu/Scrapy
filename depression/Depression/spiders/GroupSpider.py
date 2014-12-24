__author__ = 'RHX'

from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.item import Item
from scrapy.contrib.exporter import JsonLinesItemExporter


from Depression.items import DepressionItem
from Depression.items import TopicItem
from Depression.items import RecentTopicItem
from Depression.items import ResponseItem
import re


class DepressionSpider(CrawlSpider):
    name = "group"
    allowed_domains = ["douban.com"]
    start_urls = [
        #"http://www.douban.com/group/search?cat=1019&q=%E6%8A%91%E9%83%81%E7%97%87"
        #"http://www.douban.com/group/151898"
        "http://www.douban.com/group/151898/discussion?start=50"
        #"http://www.douban.com/group/search?cat=1019&q=%E6%8A%91%E9%83%81%E7%97%87"
        #"http://www.douban.com/group/151898/"
        #"http://www.douban.com/group/explore?tag=%E5%BF%83%E7%90%86%E5%AD%A6"
        ]

    rules = [
        # Rule(SgmlLinkExtractor(allow=('/group/[^/]+/$'), restrict_xpaths=('//div[@class="result"]')),),callback='parse_home'),
        Rule(SgmlLinkExtractor(allow=(r'/group/151898/discussion\?start=\d'),restrict_xpaths=('//span[@class="next"]') )),
            #restrict_xpaths=('//span[class="next"]/link/@href')),follow=True)

        Rule(SgmlLinkExtractor(allow=('/group/topic/[^/]+/$'),deny=('/group/151898/discussion\?start\='), 
            restrict_xpaths=('//td[@class="title"]')),callback='parse_post', follow=True),

        Rule(SgmlLinkExtractor(allow=('/group/topic/[^/]+/\?start'),restrict_xpaths=('//span[@class="next"]')), 
            callback="parse_reply", follow=True), # this rule is
        ]

    def _get_ID_from_topic_URL(self, url):
        m = re.search("^http://www.douban.com/group/topic/([^/]+)/", url)
        if (m):
            return m.group(1)
        else:
            return 0

    def _get_ID_from_member_URL(self, url):
        m = re.search("^http://www.douban.com/group/people/([^/]+)/$", url)
        if (m):
            return m.group(1)
        else:
            return 0

    def parse_post(self, response):
        self.log("Fetch post: ####### %s" % response.url) #need to be the post ID
        #hxs = HtmlXPathSelector(response)
        itemP = TopicItem()
        itemR = ResponseItem()

        # itemP['title_P'] = response.xpath('.//h1/text()').extract()
        itemP['topicID'] = self._get_ID_from_topic_URL(response.url) # need to understand

        # itemP['link'] = response.url
        # authorURL = response.xpath('//span[@class="from"]/a/@href').extract()
        # itemP['author'] = self._get_ID_from_member_URL("".join(authorURL)) # type change from list to string
        # itemP['author'] = response.xpath('//span[@class="from"]/a/@href').re(r'people/([^/]+)/$') # another way to do so
        # itemP['createTime'] = response.xpath('//h3/span[@class="color-green"]/text()').extract()
        """
        itemP['content'] = response.xpath('//div[@class="topic-content"]/p/text()').extract()
        num = response.xpath('//span[@class="fav-num"]/a/text()').re("\d+")
        if (num):
            itemP['numberLikes'] = num[0]
        else:
            itemP['numberLikes'] = 0
        """
        ul = response.xpath('//ul[@class="topic-reply"]')
        if (len(ul)>1):
            self.parse_reply(response)
        else:
            ul = response.xpath('//ul[@class="topic-reply"]')
            itemR['topicID_R'] = self._get_ID_from_topic_URL(response.url)
            itemR['responseID_R'] = ''#l.xpath('.//li/@id').extract()
            itemR['author_R'] = ''#ul.xpath('.//h4/a/@href').re(r'people/([^/]+)/$')
            itemR['time_R'] = ''#ul.xpath('.//h4/span/text()').extract()
            itemR['content_R'] = ''#ul.xpath('.//p/text()').extract()
            replys = ul.xpath('.//div[@class="reply-quote"]')
            if (len(replys)>0):
                resTos = replys.xpath('.//span[@class="pubdate"]/a/@href').re(r'people/([^/]+)/$')
            else:
                resTos = ['0000000'] # 0 denotes respond to nobody
            itemR['responseTo_R'] = ''

        return itemP, itemR


    def parse_reply(self, response):
        self.log("Extract reply comment: ******* %s" % response.url)
        itemR = ResponseItem()
        itemRs = []
        resTos = []

        ul = response.xpath('//ul[@class="topic-reply"]/li')

        for li in ul:
            ID = li.xpath('.//li/@id').extract()
            author = li.xpath('.//h4/a/@href').re(r'people/([^/]+)/$')
            time = li.xpath('.//h4/span/text()').extract()
            content = li.xpath('.//p/text()').extract()
            replys = li.xpath('.//div[@class="reply-quote"]') # need to correspond to one ul in topic-reply
            if (len(replys)>0):
                resTo = replys.xpath('.//span[@class="pubdate"]/a/@href').re(r'people/([^/]+)/$')
            else:
                resTo = ['0000000'] # 0 denotes respond to nobody
            resTos.append(resTo)

            itemR['author_R'] = author #.append(author)
            itemR['time_R'] = time #.append(time)
            itemR['content_R'] = "".join(content).encode('utf-8').strip() #.append("".join(content).encode('utf-8'))
            itemR['responseTo_R'] = resTo
            itemRs.append(itemR)

        return itemRs
        #JsonLinesItemExporter.export_item(itemR)
        #return itemR # I want to set that, each item with a line


    def parse_home(self, response):
        itemD = DepressionItem()  # !!! take care of the parentheses
        itemD['groupName'] = response.xpath('//h1/text()').re("^\s+(.*)\s+$")
        itemD['groupIntro'] = response.xpath('//div[contains(@class,"group-intro")]/text()').re("^\s+(.*)\s+$")

        itemT = RecentTopicItem()
        itemT['topicID_C'] = []
        itemT['topicTitle_C'] = []
        itemT['author_C'] = []
        itemT['numberResponse_C'] = []
        itemT['lastResponse_C'] =[]

        tr = response.xpath('//tr[contains(@class,"")]')
        for td in tr:
            topicURL = td.xpath('.//td[contains(@class, "title")]/a/@href').extract()
            # topicid = self.get_ID_from_group_URL(self,memberURL) # how to extract from the url
            title = td.xpath('.//td[contains(@class, "title")]/a/@title').extract()
            author = td.xpath('.//td[@nowrap="nowrap"]/a[@class=""]/@href').extract() # could be userID
            responseNumber = td.xpath('.//td[@class="" and @nowrap="nowrap"]/text()').extract()
            lastResponse = td.xpath('.//td[@class="time"]/text()').extract()

            itemT['topicID_C'].append(topicURL)
            itemT['topicTitle_C'].append(title)  # extract the text of all topics in one page, how to get more papges
            itemT['author_C'].append(author)
            itemT['numberResponse_C'].append(responseNumber)
            itemT['lastResponse_C'].append(lastResponse)

        return itemD, itemT

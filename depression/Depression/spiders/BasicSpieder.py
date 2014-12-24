__author__ = 'ronghua'

from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.item import Item
from Depression.items import DepressionItem
from Depression.items import TopicItem
from Depression.items import RecentTopicItem
import re


class DepressionSpider(CrawlSpider):
    name = "depression"
    allowed_domains = ["douban.com"]
    start_urls = ["http://www.douban.com/group/151898"]

    Rule(SgmlLinkExtractor(allow=('/group/topic/[^/]+/$')), callback='parse_post', follow='true')
    # this rule is not effective, try some other rules

    def parse_post(self, response):
        self.log("Fetch each specific post %s" % response.url) #need to be the post ID
        hxs = HtmlXPathSelector(response)
        itemP = TopicItem()

        itemP['title_P'] = hxs.xpath('.//h1/text()').extract()

        return itemP


    def parse(self, response):
        # hxs = HtmlXPathSelector(response)
        itemD = DepressionItem()  # !!! take care of the parentheses
        itemD['groupName'] = response.xpath('//h1/text()').re("^\s+(.*)\s+$")
        itemD['groupIntro'] = response.xpath('//div[contains(@class,"group-intro")]/text()').re("^\s+(.*)\s+$")

        itemT = RecentTopicItem()
        itemT['topicID_R'] = []
        itemT['topicTitle_R'] = []
        itemT['author_R'] = []
        itemT['numberResponse_R'] = []
        itemT['lastResponse_R'] =[]

        tr = response.xpath('//tr[contains(@class,"")]')
        for td in tr:
            topicURL = td.xpath('.//td[contains(@class, "title")]/a/@href').extract()
            # topicid = self.get_ID_from_group_URL(self,memberURL) # how to extract from the url
            title = td.xpath('.//td[contains(@class, "title")]/a/@title').extract()
            author = td.xpath('.//td[@nowrap="nowrap"]/a[@class=""]/@href').extract() # could be userID
            responseNumber = td.xpath('.//td[@class="" and @nowrap="nowrap"]/text()').extract()
            lastResponse = td.xpath('.//td[@class="time"]/text()').extract()

            itemT['topicID_R'].append(topicURL)
            itemT['topicTitle_R'].append(title)  # extract the text of all topics in one page, how to get more papges
            itemT['author_R'].append(author)
            itemT['numberResponse_R'].append(responseNumber)
            itemT['lastResponse_R'].append(lastResponse)


        return itemD, itemT

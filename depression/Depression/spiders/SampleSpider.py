__author__ = 'RHX'

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from Depression.items import DoubanItem
import re

class GroupSpider(CrawlSpider):
    name = "Group222"
    allowed_domains = ["douban.com"]
    start_urls = [
        "http://www.douban.com/group/explore?tag=%E8%B4%AD%E7%89%A9",
        "http://www.douban.com/group/explore?tag=%E7%94%9F%E6%B4%BB",
        "http://www.douban.com/group/explore?tag=%E7%A4%BE%E4%BC%9A",
        "http://www.douban.com/group/explore?tag=%E8%89%BA%E6%9C%AF",
        "http://www.douban.com/group/explore?tag=%E5%AD%A6%E6%9C%AF",
        "http://www.douban.com/group/explore?tag=%E6%83%85%E6%84%9F",
        "http://www.douban.com/group/explore?tag=%E9%97%B2%E8%81%8A",
        "http://www.douban.com/group/explore?tag=%E5%85%B4%E8%B6%A3"
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow=('/group/[^/]+/$', )), callback='parse_group_home_page', process_request='add_cookie'),
    #   Rule(SgmlLinkExtractor(allow=('/group/[^/]+/discussion\?start\=(\d{1,4})$', )), callback='parse_group_topic_list', process_request='add_cookie'),
        Rule(SgmlLinkExtractor(allow=('/group/explore\?tag', )), follow=True, process_request='add_cookie'),
    ]

    def __get_id_from_group_url(self, url):
        m =  re.search("^http://www.douban.com/group/([^/]+)/$", url)
        if(m):
            return m.group(1)
        else:
            return 0



    def add_cookie(self, request):
        request.replace(cookies=[

        ])
        return request

    def parse_group_topic_list(self, response):
        self.log("Fetch group topic list page: %s" % response.url)
        pass


    def parse_group_home_page(self, response):

        self.log("Fetch group home page: %s" % response.url)

        hxs = HtmlXPathSelector(response)
        item = DoubanItem()

        #get group name
        item['groupName'] = hxs.select('//h1/text()').re("^\s+(.*)\s+$")[0]

        #get group id
        item['groupURL'] = response.url
        groupid = self.__get_id_from_group_url(response.url)

        #get group members number
        members_url = "http://www.douban.com/group/%s/members" % groupid
        members_text = hxs.select('//a[contains(@href, "%s")]/text()' % members_url).re("\((\d+)\)")
        item['totalNumber'] = members_text[0]

        #get relative groups
        item['RelativeGroups'] = []
        groups = hxs.select('//div[contains(@class, "group-list-item")]')
        for group in groups:
            url = group.select('div[contains(@class, "title")]/a/@href').extract()[0]
            item['RelativeGroups'].append(url)
        #item['RelativeGroups'] = ','.join(relative_groups)
        return item
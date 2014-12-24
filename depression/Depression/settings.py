# -*- coding: utf-8 -*-

# Scrapy settings for Depression project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Depression'

SPIDER_MODULES = ['Depression.spiders']
NEWSPIDER_MODULE = 'Depression.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Depression (+http://www.yourdomain.com)'

DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
COOKIES_ENABLED = False

#取消默认的useragent,使用新的useragent
#DOWNLOADER_MIDDLEWARES = {
#        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
#        'Depression.middlewares.rotate_useragent.RotateUserAgentMiddleware' :400
#}

# More comprehensive list can be found at
# http://techpatterns.com/forums/about304.html

HTTP_PROXY = 'http://127.0.0.1:8123'

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/536.7',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'
]
#DOWNLOADER_MIDDLEWARES = {
#        'Depression.middlewares.RandomUserAgentMiddleware': 400,
#        'Depression.middlewares.ProxyMiddleware': 410,
#        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
#        Disable compression middleware, so the actual HTML pages are cached
#}

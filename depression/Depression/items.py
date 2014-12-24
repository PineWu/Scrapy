# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DepressionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # group-related info
    groupName = scrapy.Field()
    groupIntro = scrapy.Field()
    creator = scrapy.Field() # use ID to denote
    mostRelatedGroup = scrapy.Field() # group that is most related to this group
    newJoinMember = scrapy.Field() # the 8 recently joined members, denote with ID
    totalMember = scrapy.Field() # the number of members in the group
    similarGroup = scrapy.Field() # the groups members also like to visit

class RecentTopicItem(scrapy.Item):
    # topic-related info, each item may contain more than one terms
    topicID_C = scrapy.Field() # the sort criteria is not definite, not the last response time

    # items in one recent topic, end with *R
    topicTitle_C = scrapy.Field()
    author_C = scrapy.Field() # the creator of the topic, may be more active, denote with ID
    numberResponse_C = scrapy.Field() # the number of responses, how many times the topic has been responsed
    lastResponse_C = scrapy.Field() # the time this topic is last responded

class HotTopicItem(scrapy.Item):
    # topic-related info
    essenceTopic = scrapy.Field()

    # items in one hot topic, end with *H
    topicTitle_H = scrapy.Field()
    author_H = scrapy.Field() # the creator of the topic, may be more active
    numberResponse_H = scrapy.Field() # the number of responses, how many times the topic has been responsed
    lastResponse_H = scrapy.Field() # the time this topic is last responded


class TopicItem(scrapy.Item):
    # this item is used to denote the specific post page
    title_P = scrapy.Field() # title of this post
    topicID = scrapy.Field() # the ID of this topic, also used to locate the topic
    link = scrapy.Field() # the link to this topic
    author = scrapy.Field()
    createTime = scrapy.Field() # the time this topic is created by the author
    groupFrom = scrapy.Field() # the group ID that contains this topic

    lastTopic = scrapy.Field() # the most new topics in this group which may also be related to this topic

    content = scrapy.Field() # the text or words written by the author

    numberLikes = scrapy.Field() # the number of persons who like this topic

    responseMember = scrapy.Field() # all the members who response to this topic

    recommendMember = scrapy.Field() # include all the members that recommend this topic, denote with ID

    likesMember = scrapy.Field() # include all the members that like this topic, denote with ID

class ResponseItem(scrapy.Item):
    # include the response member, response time, post content, etc.
    topicID_R = scrapy.Field() # denote the topic to respond
    responseID_R = scrapy.Field() # denote one response
    author_R = scrapy.Field() # the author who respond to the topic, denote with ID
    time_R = scrapy.Field() # response time to this topic
    content_R = scrapy.Field() # the content of this response post
    responseTo_R = scrapy.Field() # embedded response to specific author, denote the author and network only

class DoubanItem(scrapy.Item):  # For example
    # define the fields for your item here like:
    # name = Field()
    groupName = scrapy.Field()
    groupURL = scrapy.Field()
    totalNumber = scrapy.Field()
    RelativeGroups = scrapy.Field()
    ActiveUesrs = scrapy.Field()

    pass

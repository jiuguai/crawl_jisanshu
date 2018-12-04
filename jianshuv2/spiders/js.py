# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from jianshuv2.items import Jianshuv2Item, SpecialItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.http.response.html import HtmlResponse

class JsSpider2(RedisCrawlSpider):
    name = 'js2'
    allowed_domains = ['jianshu.com']
    # start_urls = ['https://www.jianshu.com/trending/monthly?utm_medium=index-banner-s&utm_source=desktop']
    special_template = 'https://www.jianshu.com/notes/{special_id}/included_collections?page={page}'

    rules = (
        Rule(LinkExtractor(allow=r'p/\w{12}',process_value=lambda u:u.split('?',1)[0]), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'p/87b31dbd7a9e',process_value=lambda u:u.split('?',1)[0]), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        i = {}
        # 标题
        title = response.xpath('//h1/text()').get()

        # 发布时间
        publish_time = response.xpath('//span[@class="publish-time"]//text()').get().strip('*')

        # 作者
        author = response.xpath('//span[@class="name"]/a/text()').get()

        # 用户个人信息地址
        user_profile = response.xpath('//span[@class="name"]/a/@href').get()
        user_profile = response.urljoin(user_profile)

        # 内容
        content = response.xpath('//div[@class="show-content-free"]').getall()

        # 字数
        words_count = response.xpath('//span[@class="wordage"]/text()').re('\d+')
        words_count = words_count[0] if words_count else 0

        # url
        page_url = response.url


        page_data = response.xpath('//script[@data-name="page-data"]')

        # 评论数
        comments_count = page_data.re('"comments_count":(\d+)')
        comments_count = comments_count[0] if comments_count else 0

        # 喜欢人数
        likes_count = page_data.re('"likes_count":(\d+)')
        likes_count = likes_count[0] if likes_count else 0

        # 阅读数
        views_count = page_data.re('views_count":(\d+)')
        views_count = views_count[0] if views_count else 0

        # 专题ID
        special_id = page_data.re('"id":(\d+)')
        special_id = special_id[0] if special_id else 0

        # 专题内容
        special = ''
        item = Jianshuv2Item(
            title = title,
            publish_time = publish_time,
            author = author,
            content = content,
            words_count = words_count,
            page_url = page_url,
            user_profile = user_profile,
            comments_count = comments_count,
            likes_count = likes_count,
            views_count = views_count,
            special_id = special_id,
            special = special,
        )
        sitem = SpecialItem(
            special_id = special_id,
            special = special,
        )
        data = {
            'page':1,
            'item':sitem,
            'url_template':self.special_template.format(page='{page}', special_id=special_id)
        }

        special_url = data['url_template'].format(page=1)
        req = scrapy.Request(special_url, 
                            callback=self.parse_special, 
                            priority=1,
                            dont_filter=True
                            )
        req.meta['data'] = data
        yield item
        yield req

    def parse_special(self,response):
        special_js = json.loads(response.text)
        data = response.meta['data']
        specials = special_js['collections']

        if specials:
            data['page'] += 1
            special_url = data['url_template'].format(page=data['page'])
            data['item']['special'] += ' <sep> '.join([d['title'] for d in specials])
            req = scrapy.Request(special_url, 
                                callback=self.parse_special, 
                                priority=response.request.priority+1,
                                dont_filter=True
                                )
            req.meta['data'] = data
            yield req
        else:
            yield data['item']


class JsSpider(RedisCrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    # start_urls = ['https://www.jianshu.com/trending/monthly?utm_medium=index-banner-s&utm_source=desktop']
    special_template = 'https://www.jianshu.com/notes/{special_id}/included_collections?page={page}'

    rules = (
        Rule(LinkExtractor(allow=r'p/\w{12}',process_value=lambda u:u.split('?',1)[0]), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'p/87b31dbd7a9e',process_value=lambda u:u.split('?',1)[0]), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        i = {}
        # 标题
        title = response.xpath('//h1/text()').get()

        # 发布时间
        publish_time = response.xpath('//span[@class="publish-time"]//text()').get().strip('*')

        # 作者
        author = response.xpath('//span[@class="name"]/a/text()').get()

        # 用户个人信息地址
        user_profile = response.xpath('//span[@class="name"]/a/@href').get()
        user_profile = response.urljoin(user_profile)

        # 内容
        content = response.xpath('//div[@class="show-content-free"]').getall()

        # 字数
        words_count = response.xpath('//span[@class="wordage"]/text()').re('\d+')
        words_count = words_count[0] if words_count else 0

        # url
        page_url = response.url


        page_data = response.xpath('//script[@data-name="page-data"]')

        # 评论数
        comments_count = page_data.re('"comments_count":(\d+)')
        comments_count = comments_count[0] if comments_count else 0

        # 喜欢人数
        likes_count = page_data.re('"likes_count":(\d+)')
        likes_count = likes_count[0] if likes_count else 0

        # 阅读数
        views_count = page_data.re('views_count":(\d+)')
        views_count = views_count[0] if views_count else 0

        # 专题ID
        special_id = page_data.re('"id":(\d+)')
        special_id = special_id[0] if special_id else 0

        # 专题内容
        special = ''
        item = Jianshuv2Item(
            title = title,
            publish_time = publish_time,
            author = author,
            content = content,
            words_count = words_count,
            page_url = page_url,
            user_profile = user_profile,
            comments_count = comments_count,
            likes_count = likes_count,
            views_count = views_count,
            special_id = special_id,
            special = special,
        )
        
        data = {
            'page':1,
            'item':item,
            'url_template':self.special_template.format(page='{page}', special_id=special_id)
        }

        special_url = data['url_template'].format(page=1)
        req = scrapy.Request(special_url, 
                            callback=self.parse_special, 
                            priority=1,
                            )
        req.meta['data'] = data
        yield req

    def parse_special(self,response):
        special_js = json.loads(response.text)
        data = response.meta['data']
        specials = special_js['collections']

        if specials:
            data['page'] += 1
            special_url = data['url_template'].format(page=data['page'])
            data['item']['special'] += ' <sep> '.join([d['title'] for d in specials])
            req = scrapy.Request(special_url, 
                                callback=self.parse_special, 
                                priority=response.request.priority+1,
                                )
            req.meta['data'] = data
            yield req
        else:
            yield data['item']
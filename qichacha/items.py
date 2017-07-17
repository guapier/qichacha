# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QichachaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    company_id=scrapy.Field()
    company_url=scrapy.Field()
    company_name=scrapy.Field()
    cellphone=scrapy.Field()
    email=scrapy.Field()
    address=scrapy.Field()
    unique_social_credit_code=scrapy.Field()
    register_number=scrapy.Field()
    organization_code=scrapy.Field()
    business_status=scrapy.Field()
    lawman=scrapy.Field()
    registered_capital=scrapy.Field()
    company_type=scrapy.Field()
    publish_time=scrapy.Field()
    business_limit=scrapy.Field()
    registration_authority=scrapy.Field()
    approved_time=scrapy.Field()
    company_scale=scrapy.Field()
    industry=scrapy.Field()
    english_name=scrapy.Field()
    former_name=scrapy.Field()
    company_address=scrapy.Field()
    scope_business=scrapy.Field()




class MQichachaItem(scrapy.Item):
    company_id=scrapy.Field()
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    company_status = scrapy.Field()
    lawman = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    address = scrapy.Field()
    register_number = scrapy.Field()
    unique_social_code = scrapy.Field()
    register_capital = scrapy.Field()
    created_date = scrapy.Field()
    company_type = scrapy.Field()
    business_scope = scrapy.Field()
    business_limit = scrapy.Field()

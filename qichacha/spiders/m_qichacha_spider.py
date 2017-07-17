# -*- coding: utf-8 -*-
import scrapy
import csv
from scrapy.http import Request
from qichacha.items import MQichachaItem
import re


class MQichachaSpiderSpider(scrapy.Spider):
    name = 'm_qichacha_spider'
    allowed_domains = ['m.qichacha.com']
    start_urls = ['http://m.qichacha.com/search?key=%E5%89%8D%E6%B5%B7%E4%BC%81%E4%BF%9D%E7%A7%91%E6%8A%80']
    headers = {
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'referer': "http://m.qichacha.com/search?key=%E5%89%8D%E6%B5%B7%E4%BC%81%E4%BF%9D%E7%A7%91%E6%8A%80",
        'cookie': "UM_distinctid=15d3b3ecd43c0a-0cb34ba7f921cb-474a0521-140000-15d3b3ecd4495a; gr_user_id=7f6c054b-29b5-4fdf-8aef-7b9147408511; acw_tc=AQAAAOZxd0UMpwIAmx0Ot4sOcn+22fH+; PHPSESSID=ka4k53ijhjps6aue2oslk35q31; gr_session_id_9c1eb7420511f8b2=2e01c31e-75fe-4c65-b22f-5ca2a270c3da",
        'connection': "keep-alive",
        'cache-control': "no-cache",
    }

    # def start_requests(self):
    #     # with open(getattr(self, "file", "company.csv"), "rU") as f:
    #     #     reader = csv.reader(f)
    #     #     for line in reader:
    #     #         request = Request('http://m.qichacha.com/search?key='+line[0].decode('gbk').encode('utf-8'),headers=self.headers)
    #     #         #request.meta['fields'] = line
    #     #         yield request
    #     with open(("company.csv"), "rU") as f:
    #         reader = csv.reader(f)
    #         for line in reader:
    #             request = Request('http://m.qichacha.com/search?key=' + line[0], headers=self.headers)
    #             # request.meta['fields'] = line
    #             yield request

    def parse(self, response):
        item=MQichachaItem()
        company_url=response.css('div.center-content a::attr(href)').extract_first()
        match_obj = re.match('.*?([a-zA-Z0-9]{10,})', company_url)
        if match_obj:
            company_id = match_obj.group(1)
        item['company_id'] = company_id
        item['company_url']=response.urljoin(company_url)
        request = scrapy.Request(response.urljoin(company_url), headers=self.headers, callback=self.parse_content)
        request.meta['item'] = item
        yield request


    def parse_content(self, response):
        item=MQichachaItem()
        item= response.meta['item']
        company_name=response.css('div.company-name::text').extract_first("暂无");
        company_status=response.css('span.company-status::text').extract_first('暂无')
        lawman=response.css('span.oper::text').extract_first('暂无')
        phone=response.css('a.phone::text').extract_first('暂无')
        email=response.css('a.email::text').extract_first('暂无')
        address=response.css('div.address::text').extract_first('暂无')
        right_item=response.css('div.basic-item-right::text').extract()
        register_number=right_item[1]
        unique_social_code=right_item[2]
        register_capital=right_item[3]
        created_date=right_item[4]
        company_type=right_item[5]
        business_scope=right_item[6]
        company_address=right_item[7]
        business_limit=right_item[8]
        business_status=right_item[9]

        item['company_name']=company_name
        item['company_status']=company_status
        item['lawman']=lawman
        item['phone']=phone
        item['email']=email
        item['address']=address
        item['register_number']=register_number
        item['unique_social_code']=unique_social_code
        item['register_capital']=register_capital
        item['created_date']=created_date
        item['company_type']=company_type
        item['business_scope']=business_scope
        item['business_limit']=business_limit

        yield  item



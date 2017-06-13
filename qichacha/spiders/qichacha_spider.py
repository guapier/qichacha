# -*- coding: utf-8 -*-
import scrapy
import re
from qichacha.items import QichachaItem
from scrapy.http import Request
import csv
try:
    import urlparse as parse
except:
    from urllib import parse


class QichachaSpiderSpider(scrapy.Spider):
    name = "qichacha_spider"
    headers= {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
  'Host':'www.qichacha.com',
  'Referer':'http://www.qichacha.com/search?key=%E5%89%8D%E6%B5%B7',
  'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
  'Cookie':'acw_tc=AQAAAMClKWW7Aw4AA4YOtzlzZwkPcQLk; gr_user_id=902c1daf-8f80-4029-9fa8-c592b8892ee0; _uab_collina=149699319138946038350234; UM_distinctid=15c8bbf57c70-011db702092652-3060750a-fa000-15c8bbf57d07; _umdata=70CF403AFFD707DFE7A81215053B1F94125B615566D35889A27BFF2A817CA2240D48C18462499BD5CD43AD3E795C914C137F70B75F790126A4488D143A0E7980; PHPSESSID=k2ngn9tqd3qmacmunak7404p67; CNZZDATA1254842228=1797299873-1496988018-null%7C1497063794',


}
    allowed_domains = ["qichacha.com"]
    start_urls = ['http://www.qichacha.com/search?key=%E5%89%8D%E6%B5%B7%E4%BC%81%E4%BF%9D%E7%A7%91%E6%8A%80']
    # csv_reader = csv.reader(open('./company.csv'))
    # for row in csv_reader:
    #     start_urls.append('http://www.qichacha.com/search?key='+row[0])
    # def start_requests(self):
    #     with open(getattr(self, "file", "company.csv"), "rU") as f:
    #         reader = csv.reader(f)
    #         for line in reader:
    #             request = Request('http://www.qichacha.com/search?key='+line[0].decode('utf-8').encode('utf-8'),headers=self.headers,callback=self.parse)
    #             #request.meta['fields'] = line
    #             yield request

    def parse(self, response):
        item=QichachaItem()
        _company_url=response.css('a.ma_h1::attr(href)').extract_first()
        if _company_url is not None:
            company_url = parse.urljoin(response.url, _company_url)
            match_obj=re.match('.*?([a-zA-Z0-9]{10,})',_company_url)
            if match_obj:
                company_id=match_obj.group(1)
            item['company_id']=company_id
            item['company_url']=company_url
            print(type(company_url))
            request= scrapy.Request(company_url, headers=self.headers,callback=self.parse_basecontent)
            request.meta['item']=item
            yield request

    def parse_basecontent(self,response):
        item=response.meta['item']
        company_name=response.css('span.text-big.font-bold::text').extract_first("")
        _cellphone=response.css('small.ma_line2::text').extract_first("")
        _email = response.css('small.ma_line2 a::text').extract_first("")
        address=response.css('small.ma_line3::text').extract_first().strip()
        if(_cellphone==''):
            cellphone='暂无'
        else:
            result = re.match('.*?(0\d{3}-\d{8}).*', _cellphone)
            if result:
                cellphone=result.group(1)
            else:
                cellphone=_cellphone


        if (_email == ''):
            email = '暂无'
        else:
            result=re.match('.*?(\\w+@(\\w+.)+[a-z]{2,3}).*',_email)
            if result:
                email = result.group(1)
            else:
                email = _email
        item['company_name']=company_name
        item['email']=email
        item['address']=address
        base_info_url='http://www.qichacha.com/company_getinfos?unique={0}&companyname={1}&tab=base'
        request = scrapy.Request(base_info_url.format(item['company_id'],item['company_name'].encode('utf-8')), headers=self.headers, callback=self.parse_detail_content)
        request.meta['item'] = item
        yield request


    def parse_detail_content(self,response):
        item=response.meta['item']
        _result = response.css('section#Cominfo table.m_changeList td::text').extract()
        result=[element for element in _result if len(element.strip())>0]
        item['unique_social_credit_code']=result[1].strip()
        item['register_number']=result[3].strip()
        item['organization_code']=result[5].strip()
        item['business_status']=result[7].strip()
        item['lawman']=response.css('a.text-primary::text').extract_first()
        item['registered_capital']=result[10].strip()
        item['company_type']=result[12].strip()
        item['publish_time']=result[14].strip()
        item['business_limit']=result[16].strip()
        item['registration_authority']=result[18].strip()
        item['approved_time']=result[20].strip()
        item['company_scale']=result[22].strip()
        item['industry']=result[24].strip()
        item['english_name']=result[26].strip()
        item['former_name']=result[28].strip()
        item['company_address']=result[30].strip()
        item['scope_business']=result[32].strip()

        yield item









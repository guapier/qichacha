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
  'Cookie':'acw_tc=AQAAAH9a5jrnJwEAlh8Otwrltqp2M0uZ; UM_distinctid=15d3b3ecd43c0a-0cb34ba7f921cb-474a0521-140000-15d3b3ecd4495a; hasShow=1; _uab_collina=149993755806215945389267; gr_user_id=7f6c054b-29b5-4fdf-8aef-7b9147408511; _umdata=E2AE90FA4E0E42DE5781CCF86806B4F5E78B1864E8942C6AFE8A955D217A8CF6BB6D2AFA99568EF5CD43AD3E795C914C01C5561BBF94ECE85D0F020B0B81CC82; PHPSESSID=mpkt3jjq1ukh6rn26bmuv22u07; gr_session_id_9c1eb7420511f8b2=5b2f9c02-0014-4761-9ac1-a6a827cb812f; CNZZDATA1254842228=762928867-1499932830-%7C1499932830',


}
    allowed_domains = ["qichacha.com"]
    #start_urls = ['http://www.qichacha.com/search?key=%E5%89%8D%E6%B5%B7%E4%BC%81%E4%BF%9D%E7%A7%91%E6%8A%80']
    # csv_reader = csv.reader(open('./company.csv'))
    # for row in csv_reader:
    #     start_urls.append('http://www.qichacha.com/search?key='+row[0])
    def start_requests(self):
        # with open(getattr(self, "file", "company.csv"), "rU") as f:
        #     reader = csv.reader(f)
        #     for line in reader:
        #         request = Request('http://www.qichacha.com/search?key='+line[0].decode('gbk').encode('utf-8'),headers=self.headers)
        #         #request.meta['fields'] = line
        #         yield request
        with open(("company.csv"), "rU") as f:
            reader = csv.reader(f)
            for line in reader:
                request = Request('http://www.qichacha.com/search?key='+line[0],headers=self.headers)
                #request.meta['fields'] = line
                yield request

    # def start_requests(self):
    #     yield Request('http://www.qichacha.com/search?key=%E5%89%8D%E6%B5%B7%E4%BA%BA%E5%AF%BF%E4%BF%9D%E9%99%A9%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8',headers=self.headers)

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
            request= scrapy.Request(company_url, headers=self.headers,callback=self.parse_basecontent)
            request.meta['item']=item
            yield request

    def parse_basecontent(self,response):
        item=response.meta['item']
        company_name=response.css('div.company-top-name::text').extract_first("")
        _cellphone=response.css('small.ma_line2::text').extract_first("")
        _email = response.css('small.ma_line2 a::text').extract_first("")
        address=response.css('small.ma_line3::text').extract_first().strip()
        if(_cellphone and _cellphone.strip()==''):
            cellphone='暂无'
        else:
            result = re.match('.*?((0\d{3}-\d{8})|(^1[3,4,5,8]\d{9})).*', _cellphone)
            if result:
                cellphone=result.group(1)
            else:
                cellphone=_cellphone


        if (_email and _email.strip() == ''):
            email = '暂无'
        else:
            result=re.match('.*?(\w+@(\w+.)+[a-z]{2,3}).*',_email)
            if result:
                email = result.group(1)
            else:
                email = _email
        item['company_name']=company_name
        item['cellphone']=cellphone
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









# -*- coding: utf-8 -*-
__author__ = 'bobby'

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "qichacha_spider"])
# execute(["scrapy", "crawl", "zhihu"])
# execute(["scrapy", "crawl", "lagou"])
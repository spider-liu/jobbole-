# -*- coding: utf-8 -*-
__author__="spiderliu"
from scrapy.cmdline import execute

import  sys
import os

print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","jobbole"])
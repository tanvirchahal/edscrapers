# -*- coding: utf-8 -*-
import re

from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor

from edscrapers.scrapers.edgov.parser import parse
from edscrapers.scrapers.base import helpers as h


class Crawler(CrawlSpider):

    name = 'grad360'

    allowed_regex = r'^http.*://grad360\.org/.*$'

    def __init__(self):

        sites = ['arts', 'ceds', 'ciidta', 'crdc', 'csp',
                 'easie', 'easn', 'edfacts', 'elc', 'fitw',
                 'nycpstep', 'oese', 'osep', 'pathways', 'pdg',
                 'rtt', 'rttd', 'seed', 'slds']
        self.start_urls = [ f'https://{name}.grad360.org' for name in sites]

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                allow=self.allowed_regex,
            ), callback=parse, follow=True),
        ]


        # Inherit parent
        super(Crawler, self).__init__()

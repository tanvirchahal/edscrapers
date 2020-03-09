# -*- coding: utf-8 -*-
import re
import json
from slugify import slugify

from edscrapers.scrapers import base
from edscrapers.scrapers.base.models import Dataset, Resource
import edscrapers.scrapers.base.helpers as h



def parse(res):

    dataset = Dataset()
    dataset['resources'] = []

    h.get_all_resources(res, dataset, h.get_data_extensions(), deny_list=[])

    if len(dataset['resources']) > 0:

        dataset['source_url'] = res.url
        dataset['title'] = res.xpath('//meta[@name="DC.title"]/@content').get('text')
        if not dataset['title'] or dataset['title'] == 'text':
            dataset['title'] = res.xpath('/html/head/title/text()').get('text')
        dataset['name'] = slugify(res.url)
        dataset['notes'] = res.xpath('//meta[@name="DC.description"]/@content').get('text')
        return dataset

    return None


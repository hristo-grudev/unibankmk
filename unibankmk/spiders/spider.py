import json

import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import UnibankmkItem
from itemloaders.processors import TakeFirst

base = "https://unibank-prod.herokuapp.com/article/{}/40"

class UnibankmkSpider(scrapy.Spider):
	name = 'unibankmk'
	start_urls = [base.format('1')]

	def parse(self, response):
		data = json.loads(response.text)
		next_page = data['payload']['nextPage']
		for post in data['payload']['articles']:
			title = post['title']
			date = post['createdAt']
			description = remove_tags(post['html'])

			item = ItemLoader(item=UnibankmkItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()
		if next_page:
			yield response.follow(base.format(next_page), self.parse)





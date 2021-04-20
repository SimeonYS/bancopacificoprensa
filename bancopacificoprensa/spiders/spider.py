import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import BbancopacificoprensaItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class BbancopacificoprensaSpider(scrapy.Spider):
	name = 'bancopacificoprensa'
	start_urls = ['https://bancopacificoprensa.ec/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="td-ss-main-content td_block_template_11"]//h3[@class="entry-title td-module-title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('(//i[@class="td-icon-menu-right"])[last()]/ancestor::a/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)

	def parse_post(self, response):
		date = response.xpath('//time/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="pf-content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=BbancopacificoprensaItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()

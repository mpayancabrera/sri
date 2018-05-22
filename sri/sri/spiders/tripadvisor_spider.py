import scrapy,ipdb
from sri.items import HotelSentimentItem
 
class TripadvisorSpider(scrapy.Spider):
	name = "tripadvisor"
	start_urls = [
	    "https://www.tripadvisor.es/SmartDeals-g187441-Granada_Province_of_Granada_Andalucia-Hotel-Deals.html"
	]

	def parse_review(self, response):
		item = HotelSentimentItem()
		item['title'] = response.xpath('//span[@class="noQuotes"]/text()').extract()[0]
		item['content'] = response.xpath('//div[@class="entry"]/p/text()').extract()[0]
		item['stars'] = response.xpath('//span[contains(@class, "ui_bubble_rating")]/@alt').extract()[0]
		item['hotel'] = self.currentHotel
		return item

	def parse_hotel(self, response):
		for href in response.xpath('//div[@class="quote"]/a/@href'):
			url = response.urljoin(href.extract())
			hotel = response.xpath('//h1[@id="HEADING"]/text()').extract()[0]
			self.currentHotel = hotel
			yield scrapy.Request(url, callback=self.parse_review)
 
		next_page = response.xpath('//link[@rel="next"]/@href')
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse_hotel)

	def parse(self, response):
		for href in response.xpath('//div[@class="listing_title"]/a/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_hotel)
 
		next_page = response.xpath('//link[@rel="next"]/@href')
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse)
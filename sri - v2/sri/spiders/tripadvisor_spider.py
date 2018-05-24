import scrapy,re
from sri.items import HotelSentimentItem
 
class TripadvisorSpider(scrapy.Spider):
	name = "tripadvisor"
	start_urls = [
	    "https://www.tripadvisor.es/Hotels-g187441-Granada_Province_of_Granada_Andalucia-Hotels.html"
	]

	def parse(self, response):
		for href in response.xpath('//div[@class="listing_title"]/a/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_hotel)

		url = response.url
		if not re.findall(r'oa\d', url):
		    next_page = re.sub(r'(-g187441-)', r'\g<1>oa30-', url)
		else:
			pagenum = int(re.findall(r'oa(\d+)-', url)[0])
			pagenum_next = pagenum + 30
			next_page = url.replace('oa' + str(pagenum), 'oa' + str(pagenum_next))
		yield scrapy.Request(
            next_page,
            meta={'dont_redirect': True},
            callback=self.parse
        )

	def parse_hotel(self, response):
		for href in response.xpath('//div[contains(@class,"quote")]/a/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_review)
		
		url = response.url
		if not re.findall(r'or\d', url):
			next_page = re.sub(r'(-Reviews-)', r'\g<1>or5-', url)
			pagenum = 1
		else:
			pagenum = int(re.findall(r'or(\d+)-', url)[0])
			pagenum_next = pagenum + 5
			next_page = url.replace('or' + str(pagenum), 'or' + str(pagenum_next))
		if pagenum < 100:
			yield scrapy.Request(
				next_page,
				meta={'dont_redirect': True},
				callback=self.parse_hotel
			)


	def parse_review(self, response):
		print("**********Comentario**************")
		item = HotelSentimentItem()
		item['hotel'] = response.xpath('//span[@class="ui_header h2"]/text()').extract()[0]
		item['title'] = response.xpath('//div[contains(@class,"quote")]/h1/text()').extract()[0]
		item['content'] = response.xpath('//div[@class="entry"]/p/text()').extract()[0]
		item['stars'] = response.xpath('//span[contains(@class, "ui_bubble_rating")]/@alt').extract()[0]
		return item
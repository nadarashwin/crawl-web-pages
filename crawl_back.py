#!/usr/local/bin/python2.7
from lxml import html
import requests

class AppCrawler:

	def __init__(self, starting_url, depth):
		self.starting_url = starting_url
		self.depth = depth
		self.apps = []

	def crawl(self):
		self.get_app_from_link(self.starting_url)
		return
	
	def get_app_from_link(self, link):
		start_page = requests.get(link)
#		print start_page.text
		tree = html.fromstring(start_page.text)
		name = tree.xpath('//h1[@itemprop="name"]/text()')[0]
		developer = tree.xpath('//div[@class="left"]/h2/text()')[0]
		price = tree.xpath('//div[@itemprop="price"]/text()')[0]
		links = tree.xpath('//div[@class="center-stack"]//*/a[@class="name"]/@href')
		# print name
		# print developer
		# print price
		# print links

		# return

		app = App(name,developer,price,links)
		self.apps.append(app)


class App:

	def __init__(self, name, developer, price, links):
		self.name = name
		self.developer = developer
		self.price = price
		self.links = links


	def __str__(self):
		return ("Name: " + self.name.encode('UTF-8') + 
        "\r\nDeveloper: " + self.developer.encode('UTF-8') + 
        "\r\nPrice: " + self.price.encode('UTF-8') + "\r\n")

crawler = AppCrawler("https://itunes.apple.com/us/app/candy-crush-saga/id553834731", 0)
crawler.crawl()

for app in crawler.apps:
	print app
print crawler.apps
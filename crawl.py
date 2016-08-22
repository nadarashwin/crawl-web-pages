#!/usr/local/bin/python2.7
from lxml import html
import requests
import time

class AppCrawler:

	def __init__(self, starting_url, depth):
		self.starting_url = starting_url
		self.depth = depth
		self.current_depth = 0
		self.depth_links = []
		self.apps = []
		self.unique_apps = set(self.apps)

	def crawl(self):
		game = self.get_app_from_link(self.starting_url)
		self.apps.append(game)
		self.depth_links.append(game.links)
		# print game.links
		# print self.depth_links

		while self.current_depth < self.depth:
			current_links = []
			for link in self.depth_links[self.current_depth]:
				current_app = self.get_app_from_link(link)
				current_links.extend(current_app.links)
				self.apps.append(current_app)
				time.sleep(5)
			self.current_depth += 1
			self.depth_links.append(current_links)
		
	
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
		return app
#		self.apps.append(app)


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

#print crawler.apps
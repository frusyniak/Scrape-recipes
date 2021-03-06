from copy import copy
import logging
import os
import shelve
import re

from bs4 import BeautifulSoup
import requests

from parsers import Parsers

logging.basicConfig(filename='main.log', level='DEBUG', filemode='w')


class BonApetitScrape:
	"""
	Each instance represents a single recipe scraped from the
	bon apetit website.
	"""
	def __init__(self, url):

		self.url = url
		self.data = self.gather_data()


	def gather_data(self):
		"""
		Act as assistant to the constructor, performing all of the tasks
		that must be performed every time the class is instantiated:

			* make request and soup
			* determine the generation (age) of the soup
			* route the soup to the appropriate parsing function
			* return data structure (dictionary) that includes all the
				information that we will want from the instance:
						* recipe url
						* recipe name
						* recipe author
						* recipe ingredients
		"""
		soup = self.get_page()
		parsed_soup = self.parse(soup)

		return parsed_soup

	def parse(self, soup):
		"""
		Determine the generation of the page's soup, and return a response
		code so that the page's soup can be parsed appropriately
		"""
		# todo determine parser to use

		parse_helper = Parsers(soup)
		parse_helper.bon_apetit_2020()  # change to whatever the parser actually should be.
		return 'response_code'

	def get_page(self):
		"""
		Make the request, return the beautifulsoup object.
		"""
		response = requests.get(self.url)
		self.response = response
		soup = BeautifulSoup(response.text, features='html.parser')
		return soup


class BonApetitCrawler:
	"""
	Crawl bon apetit website. Attributes after instantiation are all
	bon appetit recipe urls.
	"""
	def __init__(self, read_cache=False, debug_mode=False):
		self.base_url = 'https://www.bonappetit.com/'
		self.sitemap = self.base_url + 'sitemap/'

		# define location of the cache
		self.cache_dir = (
			os.path.join(
				os.path.abspath(__file__),
				'cache'
			)
		)
		self.cache_path = os.path.join(self.cache_dir, 'bon_apetit_cache')

		# read the cache, if requested
		if read_cache:
			self.recipe_list = self.read_cache_func()

		else:
			self.recipe_list = self.get_bon_apetit_urls()  # or, whatever we get from the cache ############################################################################################################################## recepie list is now a tuple: ('recipe_extension', 'date_month_week')
			self.urls = [self.base_url + item for item in self.recipe_list]
			if write_cache:
				self.write_cache_func()

		if debug_mode:
			self.html_dir = os.path.join(self.cache_dir, 'html_pages')
			self.make_html_pages()

	def write_cache_fun(self):
		with shelve.open(self.cache_path, 'w') as db:
			db['cache'] = self.recipe_list

	def read_cache_func(self):
		with shelve.open(self.cache_path, 'r') as db:
			self.recipe_list = db['cache']

	def cache_recipe_page_responses(self):
		"""
		Make a request to all the recipe pages, and save them in the
		database.

		Make a locally stored html page for each response, which we can
		use for development.
		"""


	def get_bon_apetit_urls(self):
		"""
		Recursively crawl through the bon apetit website, and get all urls for recipe pages.
		"""
		recipe_pages = BonApetitCrawler.recursive([self.sitemap], [self.sitemap], [])
		return recipe_pages

	@staticmethod
	def recursive(blacklist, to_do, recipe_list=None):

		logging.debug(('=' * 80))

		to_do_next = []
		for url in to_do:
			log_msg = (
				'\n\n\n'
				+ url
				+ '\n\n\n'
				+ str(len(to_do))
				+ '\n\n\n'
				+ str(recipe_list)
				+ '\n\n\n'
			)
			logging.debug(log_msg)

			# make request and makes the soup, searches the soup
			resp = requests.get(url)
			soup = BeautifulSoup(resp.text)
			hrefs = soup.find_all(
				name='a',
				href=True,
				class_='sitemap__link',
			)

			# creates to_do_next
			for i in hrefs:
				concatenated_url = 'https://www.bonappetit.com/' + i.contents[0]
				to_do_next.append(copy(concatenated_url))

			# grows the master list by append to_do_next
			recipe_regex = re.compile(r'https://www.bonappetit.com/recipe/(.*)')
			slideshow_regex = re.compile(r'https://www.bonappetit.com/recipes/slideshow/(.*)')

			# get year, month, and date from sitemap url
			url_param_regex = re.compile(r'https://www.bonappetit.com/sitemap\?year=(\d\d\d\d)&month=(\d+)&week=(\d)')
			mo = re.search(url_param_regex, url)
			try:
				year, month, week = mo[1], mo[2], mo[3]
				date_string = f'{year}_{month}_week_{week}'

				logging.debug(
					f'Url: {url}\n'
					f'Regex: {url_param_regex}\n'
					f'mo: {mo}\n'
					)

				try:
					logging.debug(
						f'mo[1]: {mo[1]}'
						f'mo[2]: {mo[2]}'
						f'mo[3]: {mo[3]}'
					)
				except Exception as e:
					print(e)
					breakpoint()

			except TypeError:
				logging.debug(f'For url {url}, mon/day/wk could not be parsed.')


			for item in to_do_next:

				if item in blacklist:
					continue

				# process recipe
				mo_recipe = re.search(recipe_regex, item)
				logging.debug(item)
				if mo_recipe:
					recipe_extension = mo_recipe[1]
					recipe_list.append((recipe_extension, date_string))
					logging.debug(f'recipe:   {recipe_extension}')
					blacklist.append(item)
					continue

				# process slideshow
				mo_slideshow = re.search(slideshow_regex, item)
				if mo_slideshow:
					resp = requests.get(item)
					soup = BeautifulSoup(resp.text)
					for a in soup.find_all('a', href=True):
						mo = re.search(recipe_regex, a['href'])
						if mo:
							recipe_list.append(mo[1], date_string)
							logging.debug(('*' * 80))

						else:
							logging.debug(
								f'href in slideshow page {item} is '
								f'not a recipe: {a}'
								)

				blacklist.append(item)

				# whenever we get to 10k recipes, that's good enough!
				if len(recipe_list) > 10000:
					return recipe_list

		return BonApetitCrawler.recursive(blacklist, to_do_next, recipe_list)


if __name__ == '__main__':

	crawler = BonApetitCrawler(debug_mode=True)


	# call new url iterator function
	urls = get_bon_apetit_urls('https://www.bonappetit.com/sitemap')

	cache_urls(urls)
	cache_pages_at_urls(urls)


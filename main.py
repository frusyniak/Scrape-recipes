import re

import requests
from bs4 import BeautifulSoup

from parsers import Parsers

class BonApetitScrape:
	"""
	Each instance represents a single recipe scraped from the bon apetit website.
	"""
	def __init__(self, url):

		self.url= url
		self.data=self.get_data()


	def get_data(self):
		"""
		Act as assistant to constructor, performing all tasks that must be done everytime class initializes:
			make request and soup
			determine the age of page
			route the soup to the appropriate parsing function
			return data structure with all infromation wanted from insance:
				recipe name
				ingredients
				recipe author
				recipe url
		"""
		soup = self.get_soup()
		parsed_page= self.parse(soup)


		return parsed_page

	def parse(self, soup):
		"""
		determine the generation of the page's soup, and return a responce code so the page's soup can to parsed correctly
		"""

		#todo deermine which parser to use

		parse_helper = Parsers(soup)
		parse_helper.BA_2020() #change to what the parser should be
		return "response_code"

	def get_soup(self):
		"""
		make the request, return the beautifulsoup object
		"""
		response = requests.get(self.url)
		self.response = response
		soup = BeautifulSoup(response.text, features='html.parser')

		return soup



if __name__ == "__main__":
	import os
	base_dir = os.path.dirname(os.path.abspath(__file__))

	urls= ['https://www.bonappetit.com/recipe/roasty-toasty-pecan-caramel-shortbread-cookies',
	'https://www.bonappetit.com/recipe/grilled-sardines-with-aioli',
	'https://www.bonappetit.com/recipe/vegetarian-ramen'
	]
	for url in urls:
		ba_scr = BonApetitScrape(url)
		file_path = os.path.join(
			base_dir,
			'sample+pages',
			'2020pages',
			f'{url[34:]}.html',
		)
		breakpoint()
		with open(file_path,'w') as html:
			html.write(ba_scr.response.text)

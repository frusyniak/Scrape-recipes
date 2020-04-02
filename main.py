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
		parsed_soup= self.parse(soup)
	

		return soup_data

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
		soup = BeautifulSoup(response.text, features='html.parser')

		return soup



if __name__ == "__main__":
	ba_scr = BonApetitScrape('https://www.bonappetit.com/recipe/roasty-toasty-pecan-caramel-shortbread-cookies')












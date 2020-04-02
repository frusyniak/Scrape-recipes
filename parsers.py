import requests
from bs4 import BeautifulSoup

class Parsers:
	def __init__(self,soup):
		self.soup = soup



	def BA_2020(self):
		"""
		parse the newest page as of 4.1.2020 and return the final initi data structure
		"""

		pass


	def BA_2010(self):
		"""
		parse the old page as of 4.1.2020 and return the final init data structure
		"""
		pass

	def BA_slideshow(self):
		"""
		get all href in thr slideshow sort them with regex and  send to be parsed to the right place
		"""
		pass

if __name__== "__main__":
	pass

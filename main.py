from bs4 import BeautifulSoup
import requests

from parsers import Parsers




class BonApetitScrape:
    """
    Each instance represents a single recepie scraped from the
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
                        * recepie url
                        * recepie name
                        * recepie author
                        * recepie ingredients
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


# def generate_bon_apetit_urls():

#     dates1 = (
#         [num for num in range(1990, 2021)],
#         [num for num in range(1, 13)],
#         [num for num in range(1, 32)],
#     )

#     dates2 = [
#         [num for num in range(1990, 2021)],
#         [num for num in range(1, 13)],
#         [num for num in range(1, 7)]
#     ]
#     return dates2
#     urls = []
#     print(len(dates2))
#     for years in dates2:
#         for year in years:
#             for month in year:
#                 for week in month:
#                     url = (
#                         'https://www.bonappetit.com/sitemap?year='
#                         + year
#                         + '&month='
#                         + month
#                         + '&week='
#                         + week
#                     )
#                     breakpoint()
#                     urls.append(url)

#     breakpoint()

#     return urls

def get_bon_apetit_urls(url):

    def recursive(urls):
        urls_ = []
        for url in urls:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text)
            hrefs = soup.find_all(
                name='a',
                href=True,
                class_='sitemap__link',
            )
            breakpoint()

        return copy(urls_), recursive(urls_)

    urls = [url]

    recursive(urls)



    return hrefs, get_bon_apetit_urls(hrefs)


if __name__ == '__main__':


    # going away soon
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))

    urls = [
        'https://www.bonappetit.com/recipe/vegetarian-ramen',
        'https://www.bonappetit.com/recipe/grilled-sardines-with-aioli',  # slideshow conversion done manually
        'https://www.bonappetit.com/recipe/roasty-toasty-pecan-caramel-shortbread-cookies',
    ]

    # call new url iterator function
    urls = get_bon_apetit_urls('https://www.bonappetit.com/sitemap')



    import sys
    sys.exit()


    for url in urls:
        ba_scr = BonApetitScrape(url)
        file_path = os.path.join(
            base_dir,
            'sample_pages',
            '2020',
            f'{url[34:]}.html',
        )
        break
        # with open(file_path, 'w') as html:
        #     html.write(ba_scr.response.text)



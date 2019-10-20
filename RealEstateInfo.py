import requests
import json

from Writer import Scrape
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Scraper(Scrape):
    def __init__(self):
        Scrape.__init__(self)
        self.data = []
        self.seen = []

    def fetch_data(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(self.CHROME_DRIVER_PATH, options=options)

        headers = {
            'sec-fetch-mode': 'cors',
            'x-newrelic-id': 'VQMDUFFaGwQJU1hSBAc=',
            'dnt': '1',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'accept': '*/*',
            'referer': 'https://www.redfin.com/zipcode/94587/filter/max-price=1M,min-beds=5,viewport=37.77677:37.39043:-122.00974:-122.25144,no-outline',
            'authority': 'www.redfin.com',
            'sec-fetch-site': 'same-origin',
        }

        params = (
            ('al', '1'),
            ('market', 'sanfrancisco'),
            ('max_price', '1000000'),
            ('min_stories', '1'),
            ('num_baths', '4'),
            ('num_beds', '5'),
            ('num_homes', '350'),
            ('ord', 'redfin-recommended-asc'),
            ('page_number', '1'),
            ('poly', '-122.28097 37.41061,-122.03927 37.41061,-122.03927 37.79685,-122.28097 37.79685,-122.28097 37.41061'),
            ('sf', '1,2,3,5,6,7'),
            ('start', '0'),
            ('status', '9'),
            ('uipt', '1,2,3,4,5,6'),
            ('v', '8'),
            ('zoomLevel', '11'),
        )

        response = json.loads(requests.get('https://www.redfin.com/stingray/api/gis', headers=headers, params=params).text.replace('{}&&', ''))
        houses = response['payload']['homes']

        for house in houses:
            try:
                url = 'https://www.redfin.com' + house['url']

                print(f"Getting data for {url}")

                driver.get(url)

                street_address = driver.find_element_by_css_selector('span.street-address').get_attribute('textContent')
                city = driver.find_element_by_css_selector('span.citystatezip > span.locality').get_attribute('textContent')
                state = driver.find_element_by_css_selector('span.citystatezip > span.region').get_attribute('textContent')
                zip_code = driver.find_element_by_css_selector('span.citystatezip > span.postal-code').get_attribute('textContent')
                listed_price = house['price']['value']
                beds = house['beds']
                baths = house['baths']
                monthly_expense = driver.find_element_by_css_selector('div.CalculatorSummary > div.sectionText > p').get_attribute('textContent').replace('$', '').replace(' per month', '').replace(',', '')

                headers = {
                    'Sec-Fetch-Mode': 'cors',
                    'Referer': 'https://www.airdna.co/vacation-rental-data/app/us/california/union-city/rentalizer',
                    'Origin': 'https://www.airdna.co',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                    'DNT': '1',
                }

                params = (
                    ('access_token', 'MjkxMTI|8b0178bf0e564cbf96fc75b8518a5375'),
                    ('city_id', '59193'),
                    ('currency', 'native'),
                    ('address', f"{street_address}, {city}, CA, USA"),
                )

                response = requests.get('https://api.airdna.co/v1/market/estimate', headers=headers, params=params).json()
                nightly_price = response['property_stats']['adr']['ltm']
                occupancy_rate = response['property_stats']['occupancy']['ltm']
                revenue = response['property_stats']['revenue']['ltm']
                monthly_profit = float(revenue)/12 - float(monthly_expense)

                self.data.append(
                    [
                        url,
                        street_address,
                        city,
                        state,
                        zip_code,
                        listed_price,
                        beds,
                        baths,
                        monthly_expense,
                        nightly_price,
                        occupancy_rate,
                        revenue,
                        monthly_profit
                    ]
                )
            except:
                pass

        driver.quit()


scrape = Scraper()
scrape.scrape()
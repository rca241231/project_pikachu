import requests
import json
import re

from modules.Writer import Scrape
from uszipcode import SearchEngine
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from markets.NorCal import *


class Scraper(Scrape):
    def __init__(self,
                 county_info,
                 redfin_cookies,
                 redfin_headers,
                 redfin_params):
        Scrape.__init__(self)
        self.county_info = county_info
        self.redfin_headers = redfin_headers
        self.redfin_params = redfin_params
        self.redfin_cookies = redfin_cookies
        self.data = []
        self.search = SearchEngine(simple_zipcode=True)
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(self.CHROME_DRIVER_PATH, options=self.options)

        # TODO: If new location, change the following
        self.air_dna_headers = {
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://www.airdna.co/vacation-rental-data/app/us/california/union-city/rentalizer',
            'Origin': 'https://www.airdna.co',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'DNT': '1',
        }

    def get_all_redfin_listings(self):
        response = json.loads(requests.get('https://www.redfin.com/stingray/api/gis', headers=self.redfin_headers, params=self.redfin_params, cookies=self.redfin_cookies).text.replace('{}&&', ''))
        houses = response['payload']['homes']
        return houses

    def get_redfin_data(self, url, house):
        self.driver.get(url)
        print(f"Getting data for {url}")

        # Get information from Redfin
        street_address = ' '.join(house['url'].split('/')[3].split('-')[:-1]) if 'Undisclosed' not in ' '.join(house['url'].split('/')[3].split('-')[:-1]) else 'N/A'
        city = house['url'].split('/')[2].replace('-', ' ')
        state = house['url'].split('/')[1]
        zip_code = house['url'].split('/')[3].split('-')[-1]

        listed_price = house['price']['value'] if 'price' in house.keys() and 'value' in house['price'].keys() else 'N/A'
        beds = house['beds'] if 'beds' in house.keys() else 'N/A'
        baths = house['baths'] if 'baths' in house.keys() else 'N/A'

        # Days on Redfin
        days_on_market_info = self.driver.find_elements_by_css_selector('div.more-info > div > span')
        days_on_market = days_on_market_info[-1].find_element_by_css_selector('span.value').get_attribute('textContent').replace('days', '').strip() if len(days_on_market_info) == 0 else 'N/A'


        # School info
        school_data = self.driver.find_elements_by_css_selector('tr.schools-table-row')
        schools = '\n'.join([re.sub("(Parent Rating:)(.*)", '', info.get_attribute('textContent')).replace('homeGreatSchools', 'home GreatSchools').replace('SchoolPublic', 'School Public') for info in school_data[1:]]) if len(school_data) > 1 else 'N/A'

        # Monthly expense info
        try:
            monthly_expense = self.driver.find_element_by_css_selector('div.CalculatorSummary > div.sectionText > p').get_attribute('textContent').replace('$', '').replace(' per month', '').replace(',', '')
        except:
            monthly_expense = 'N/A'

        year_build = house['yearBuilt']['value'] if 'yearBuilt' in house.keys() and 'value' in house['yearBuilt'].keys() else 'N/A'
        lot_size = house['lotSize']['value'] if 'lotSize' in house.keys() and 'value' in house['lotSize'].keys() else 'N/A'

        return street_address, city, state, zip_code, listed_price, beds, baths, days_on_market, schools, monthly_expense, year_build, lot_size

    def get_airdna_data(self, street_address, city, state, monthly_expense):
        # Get information from AirDNA
        full_address = f'{street_address}, {city}, {state}, USA'
        params = (
            ('access_token', 'MjkxMTI|8b0178bf0e564cbf96fc75b8518a5375'),
            ('city_id', '59193'),
            ('accommodates', '6'),
            ('bathrooms', baths if baths != 'N/A' else baths),
            ('bedrooms', beds if beds != 'N/A' else beds),
            ('currency', 'native'),
            ('address', full_address),
        )

        try:
            response = requests.get('https://api.airdna.co/v1/market/estimate', headers=self.air_dna_headers, params=params).json()
            nightly_price = response['property_stats']['adr']['ltm']
            occupancy_rate = response['property_stats']['occupancy']['ltm']
            revenue = response['property_stats']['revenue']['ltm']
            monthly_profit = float(revenue)/12 - float(monthly_expense)
        except:
            print(f'AirDNA connection failed for: {full_address}')
            nightly_price = 'N/A'
            occupancy_rate = 'N/A'
            revenue = 'N/A'
            monthly_profit = 'N/A'
        return nightly_price, occupancy_rate, revenue, monthly_profit

    def get_local_data(self, zip_code):
        county = self.search.by_zipcode(zip_code).county
        employment_total_covered = self.county_info[county]['employment_total_covered']  if county in self.county_info.keys() else 'N/A'
        twelve_month_change_pct = self.county_info[county]['twelve_month_change_pct'] if county in self.county_info.keys() else 'N/A'
        twelve_month_change = self.county_info[county]['twelve_month_change'] if county in self.county_info.keys() else 'N/A'
        avg_weekly_salary = self.county_info[county]['avg_weekly_salary'] if county in self.county_info.keys() else 'N/A'
        avg_weekly_12mo_change_salary = self.county_info[county]['avg_weekly_12mo_change_salary'] if county in self.county_info.keys() else 'N/A'

        return employment_total_covered, twelve_month_change_pct, twelve_month_change, avg_weekly_salary, avg_weekly_12mo_change_salary

    def combine_data(self, house):
        url = 'https://www.redfin.com' + house['url']

        # Get Redfin data
        street_address, city, state, zip_code, listed_price, beds, baths, days_on_market, schools, monthly_expense, year_build, lot_size = self.get_redfin_data(url, house)

        # Get AirDNA Data
        nightly_price, occupancy_rate, revenue, monthly_profit = self.get_airdna_data(street_address, city, state, monthly_expense)

        # Get locality employment information
        employment_total_covered, twelve_month_change_pct, twelve_month_change, avg_weekly_salary, avg_weekly_12mo_change_salary = self.get_local_data(zip_code)

        # Append complete data
        self.data.append(
            [
                url,
                street_address,
                days_on_market,
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
                schools,
                year_build,
                lot_size,
                employment_total_covered,
                twelve_month_change_pct,
                twelve_month_change,
                avg_weekly_salary,
                avg_weekly_12mo_change_salary,
                monthly_profit,
            ]
        )

    def fetch_data(self):
        houses = self.get_all_redfin_listings()
        for house in houses:
            self.combine_data(house)
        self.driver.quit()
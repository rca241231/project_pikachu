import requests
import json
import os
import csv
import multiprocessing
from time import sleep
from random import randint
from modules.Writer import Scrape
from uszipcode import SearchEngine


class Scraper(Scrape):
    def __init__(self,
                 region,
                 county_info,
                 redfin_cookies,
                 redfin_headers,
                 redfin_params,
                 interest_rate,
                 borrowing_pct,
                 mortgage_term_years,
                 insurance_cost
                 ):
        Scrape.__init__(self)
        self.region = region
        self.insurance_cost = insurance_cost
        self.county_info = county_info
        self.interest_rate = interest_rate
        self.borrowing_pct = borrowing_pct
        self.redfin_headers = redfin_headers
        self.redfin_params = redfin_params
        self.redfin_cookies = redfin_cookies
        self.mortgage_term_years = mortgage_term_years
        self.housing_data = {}
        self.data = []
        self.exception_counties = {
            "King County": "Kings County",
        }
        self.search = SearchEngine(simple_zipcode=True)
        self.air_dna_headers = {
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://www.airdna.co/vacation-rental-data/app/us/california/union-city/rentalizer',
            'Origin': 'https://www.airdna.co',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'DNT': '1',
        }
        self.air_dna_access_token = [
            'MjkxMTI|8b0178bf0e564cbf96fc75b8518a5375',
            'ODkwMTc|478ce2c743244a7eb3d1cfddc14909b3',
            'MjA2Mjcw|69e663b4c51c4830a8bde0d3355be8ee',
            'MjA2Mjcz|e35b14ebfb794d849f9484afcffced1d'
        ]

    def get_all_redfin_listings(self):
        response = json.loads(requests.get('https://www.redfin.com/stingray/api/gis', headers=self.redfin_headers, params=self.redfin_params, cookies=self.redfin_cookies).text.replace('{}&&', ''))
        houses = response['payload']['homes']
        return houses

    def get_redfin_data(self, url, mls, house):
        print(f"Getting data for {url}")

        # Get information from Redfin
        street_address = house['streetLine']['value'] if 'value' in house['streetLine'].keys() else 'N/A'
        city = house['city']
        state = house['state']
        zip_code = house['zip']

        listed_price = house['price']['value'] if 'price' in house.keys() and 'value' in house['price'].keys() else 'N/A'
        beds = house['beds'] if 'beds' in house.keys() else 'N/A'
        baths = house['baths'] if 'baths' in house.keys() else 'N/A'

        # Days on Redfin
        days_on_market = house['timeOnRedfin']['value'] / (1000 * 60 * 60 * 24) if 'value' in house['timeOnRedfin'].keys() else 'N/A'
        year_build = house['yearBuilt']['value'] if 'yearBuilt' in house.keys() and 'value' in house['yearBuilt'].keys() else 'N/A'
        lot_size = house['lotSize']['value'] if 'lotSize' in house.keys() and 'value' in house['lotSize'].keys() else 'N/A'
        hoa = house['hoa']['value'] if 'value' in house['hoa'].keys() else 0
        sqft = house['sqFt']['value'] if 'value' in house['sqFt'].keys() else 'N/A'

        # Monthly expense info
        monthly_interest_rate = self.interest_rate/12
        numerator = (float(listed_price)*self.borrowing_pct)*(monthly_interest_rate*((1 + monthly_interest_rate)**(self.mortgage_term_years*12)))
        denominator = ((1+monthly_interest_rate)**(self.mortgage_term_years*12))-1
        monthly_expense = round(numerator/denominator + hoa + self.insurance_cost/12, 2)

        self.housing_data[mls] = {
            "url": url,
            "street_address": street_address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "listed_price": listed_price,
            "beds": beds,
            "baths": baths,
            "days_on_market": round(days_on_market) if isinstance(days_on_market, float) else 'N/A',
            "monthly_expense": monthly_expense,
            "year_build": year_build,
            "lot_size": lot_size,
            "hoa": hoa,
            "sqft": sqft,
        }

    def get_airdna_data(self, mls, house):
        # Get information from AirDNA
        street_address = self.housing_data[mls]['street_address']
        city = self.housing_data[mls]['city']
        state = self.housing_data[mls]['state']
        baths = self.housing_data[mls]['baths']
        beds = self.housing_data[mls]['beds']
        monthly_expense = self.housing_data[mls]['monthly_expense']
        full_address = f'{street_address}, {city}, {state}, USA'
        params = (
            ('access_token', self.air_dna_access_token[randint(0, 3)]),
            ('city_id', '59193'),
            ('accommodates', '6'),
            ('bathrooms', str(baths)[0] if baths != 'N/A' else baths),
            ('bedrooms', str(beds) if beds != 'N/A' else beds),
            ('currency', 'native'),
            ('address', full_address),
        )

        try:
            response = json.loads(requests.get('https://api.airdna.co/v1/market/estimate', headers=self.air_dna_headers, params=params).content.decode())
            nightly_price = response['property_stats']['adr']['ltm']
            occupancy_rate = response['property_stats']['occupancy']['ltm']
            monthly_revenue = round(response['property_stats']['revenue']['ltm']/12, 2)
            monthly_profit = round(monthly_revenue - float(monthly_expense), 2)
        except Exception as e:
            print(f'No AirDNA result for {full_address}.')
            nightly_price = 'N/A'
            occupancy_rate = 'N/A'
            monthly_revenue = 'N/A'
            monthly_profit = 'N/A'

        self.housing_data[mls]['nightly_price'] = nightly_price
        self.housing_data[mls]['occupancy_rate'] = occupancy_rate
        self.housing_data[mls]['monthly_revenue'] = monthly_revenue
        self.housing_data[mls]['monthly_profit'] = monthly_profit


    def get_local_data(self, mls):
        zip_code = self.housing_data[mls]['zip_code']
        county = self.search.by_zipcode(zip_code).county
        if county in self.exception_counties.keys():
            county =  self.exception_counties[county]

        state = self.housing_data[mls]['state']
        employment_total_covered = self.county_info[state][county]['employment_total_covered']  if county in self.county_info[state].keys() else 'N/A'
        twelve_month_change_pct = self.county_info[state][county]['twelve_month_change_pct'] if county in self.county_info[state].keys() else 'N/A'
        twelve_month_change = self.county_info[state][county]['twelve_month_change'] if county in self.county_info[state].keys() else 'N/A'
        avg_weekly_salary = self.county_info[state][county]['avg_weekly_salary'] if county in self.county_info[state].keys() else 'N/A'
        avg_weekly_12mo_change_salary = self.county_info[state][county]['avg_weekly_12mo_change_salary'] if county in self.county_info[state].keys() else 'N/A'

        self.housing_data[mls]['employment_total_covered'] = employment_total_covered
        self.housing_data[mls]['twelve_month_change_pct'] = twelve_month_change_pct
        self.housing_data[mls]['twelve_month_change'] = twelve_month_change
        self.housing_data[mls]['avg_weekly_salary'] = avg_weekly_salary
        self.housing_data[mls]['avg_weekly_12mo_change_salary'] = avg_weekly_12mo_change_salary



    def write_output(self, mls):
        writerrow_top = False if 'data.csv' in os.listdir('./') else True
        with open('./data.csv', mode='a') as output_file:
            writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

            if writerrow_top:
                # Header
                writer.writerow([
                    "region",
                    "url",
                    "street_address",
                    "days_on_market",
                    "city",
                    "state",
                    "zip_code",
                    "hoa",
                    "sqft",
                    "lot_size",
                    "year_build",
                    "listed_price",
                    "beds",
                    "baths",
                    "monthly_expense",
                    "nightly_price",
                    "occupancy_rate",
                    "monthly_revenue",
                    "employment_total_covered",
                    "twelve_month_change_pct",
                    "twelve_month_change",
                    "avg_weekly_salary",
                    "avg_weekly_12mo_change_salary",
                    "monthly_profit",
                ])

            writer.writerow([
                self.region,
                self.housing_data[mls]['url'],
                self.housing_data[mls]['street_address'],
                self.housing_data[mls]['days_on_market'],
                self.housing_data[mls]['city'],
                self.housing_data[mls]['state'],
                self.housing_data[mls]['zip_code'],
                self.housing_data[mls]['hoa'],
                self.housing_data[mls]['sqft'],
                self.housing_data[mls]['lot_size'],
                self.housing_data[mls]['year_build'],
                self.housing_data[mls]['listed_price'],
                self.housing_data[mls]['beds'],
                self.housing_data[mls]['baths'],
                self.housing_data[mls]['monthly_expense'],
                self.housing_data[mls]['nightly_price'],
                self.housing_data[mls]['occupancy_rate'],
                self.housing_data[mls]['monthly_revenue'],
                self.housing_data[mls]['employment_total_covered'],
                self.housing_data[mls]['twelve_month_change_pct'],
                self.housing_data[mls]['twelve_month_change'],
                self.housing_data[mls]['avg_weekly_salary'],
                self.housing_data[mls]['avg_weekly_12mo_change_salary'],
                self.housing_data[mls]['monthly_profit'],
            ])


    def combine_data(self, house):
        mls = house['mlsId']['value']
        url = 'https://www.redfin.com' + house['url']

        # Get Redfin data
        self.get_redfin_data(url, mls, house)

        # Get AirDNA Data
        self.get_airdna_data(mls, house)

        # Get locality employment information
        self.get_local_data(mls)

        # Write output
        self.write_output(mls)


    def fetch_data(self):
        houses = self.get_all_redfin_listings()

        # Create separate processes by houses
        process = []
        for house in houses:
            proc = multiprocessing.Process(target=self.combine_data, args=(house,))
            process.append(proc)
            proc.start()

        for proc in process:
            proc.join()
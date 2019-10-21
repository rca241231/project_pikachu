import requests
import json
import re

from Writer import Scrape
from uszipcode import SearchEngine
from CountyEmployment import CountyInfo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Scraper(Scrape):
    def __init__(self):
        Scrape.__init__(self)
        county = CountyInfo()
        self.data = []
        self.search = SearchEngine(simple_zipcode=True)
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(self.CHROME_DRIVER_PATH, options=self.options)

        # Specification on the house
        self.beds = '5'
        self.max_price = '1250000'
        self.baths = '3'

        # TODO: If new location, change the following
        self.bls_url = "https://beta.bls.gov/maps/cew/CA?industry=10&geo_id=06000&chartData=3&distribution=Quantiles&pos_color=blue&neg_color=orange&showHideChart=show&ownerType=0"
        self.county_info = county.get_employment_info(self.bls_url)
        self.redfin_cookies = {
            'RF_BROWSER_ID': '0p30zjCWSwamY2Y68psP2g',
            '_gcl_au': '1.1.2133428028.1568202210',
            '_ga': 'GA1.2.1022811260.1568202210',
            '_fbp': 'fb.1.1568202210397.1621431309',
            'RF_BROWSER_CAPABILITIES': '%7B%22css-transitions%22%3Atrue%2C%22css-columns%22%3Atrue%2C%22css-generated-content%22%3Atrue%2C%22css-opacity%22%3Atrue%2C%22events-touch%22%3Afalse%2C%22geolocation%22%3Atrue%2C%22screen-size%22%3A4%2C%22screen-size-tiny%22%3Afalse%2C%22screen-size-small%22%3Afalse%2C%22screen-size-medium%22%3Afalse%2C%22screen-size-large%22%3Afalse%2C%22screen-size-huge%22%3Atrue%2C%22html-prefetch%22%3Afalse%2C%22html-range%22%3Atrue%2C%22html-form-validation%22%3Atrue%2C%22html-form-validation-with-required-notice%22%3Atrue%2C%22html-input-placeholder%22%3Atrue%2C%22html-input-placeholder-on-focus%22%3Atrue%2C%22ios-app-store%22%3Afalse%2C%22google-play-store%22%3Afalse%2C%22ios-web-view%22%3Afalse%2C%22android-web-view%22%3Afalse%2C%22activex-object%22%3Atrue%2C%22webgl%22%3Atrue%2C%22history%22%3Atrue%2C%22localstorage%22%3Atrue%2C%22sessionstorage%22%3Atrue%2C%22position-fixed-workaround%22%3Afalse%2C%22passive-event-listener%22%3Atrue%7D',
            'fbm_161006757273279': 'base_domain=.redfin.com',
            'G_ENABLED_IDPS': 'google',
            'cto_lwid': '2d48b00a-63b7-4c77-905f-853d18a685d0',
            'RF_LAST_USER_ACTION': '1568655402939%3A25efc1ddb5192b42547849af36e94d3217ccd7b0',
            'RF_PARTY_ID': '4293663',
            'RF_AUTH': 'f8bf844320ec910ff506452a14b938af130a2b52',
            'RF_W_AUTH': 'f8bf844320ec910ff506452a14b938af130a2b52',
            'RF_SECURE_AUTH': 'baf068aafd5bd27ea5bfdb76787d50f93041a4f5',
            'RF_ACCESS_LEVEL': '3',
            'JSESSIONID': '75782B91CE65C1E0A8B38F3E847FD2DA',
            'RF_LAST_ACCESS': '1568667669596%3Af103da7bc35b8a2ac6a8074d8ad38e4899233679',
            'iterableEndUserId': 'richard.chen.1989%40gmail.com',
            'ki_t': '1568667574824%3B1568742825233%3B1568742839424%3B2%3B9',
            'wordpress_google_apps_login': '0773eaff0ed0398ef402932f31099093',
            'RF_BID_UPDATED': '1',
            '__utmx': '222895640.WTKnaAxUS8WuBy9wsrWkyg$0:1.uxw2gydsRRWC574IItzZJA$0:0.RTV_wZVsTh-aCSuerdlYSQ$0:1.Y2CmQl1SEm4efihwuTldA$0:0.DPiVULlyQUmf2VSSZa1iIg$0:0.HPaeM5zMSp-5hxCpNhjEDg$0:0.Be2giBqURYSxBB66d5SfcQ$0:1',
            'RF_CORVAIR_LAST_VERSION': '284.3.0',
            '_gid': 'GA1.2.2137983007.1571514297',
            'RF_MARKET': 'sanfrancisco',
            'RF_BUSINESS_MARKET': '2',
            'AKA_A2': 'A',
            'AMP_TOKEN': '%24NOT_FOUND',
            'nhfy_badgecount': '20',
            'RF_LISTING_VIEWS': '112839118.112200998.111971925.112814555.111078864.113153741.113357034.112572946.111958975.112339817.112405158.112408910.110142814.113173890.112924556.81198215.112809087.112927527.111911401.110623683',
            'RF_VISITED': 'null',
            'userPreferences': 'parcels%3Dtrue%26schools%3Dfalse%26mapStyle%3Ds%26statistics%3Dtrue%26agcTooltip%3Dfalse%26agentReset%3Dfalse%26ldpRegister%3Dfalse%26afCard%3D2%26schoolType%3D0%26lastSeenLdp%3DnoSharedSearchCookie%26viewedSwipeableHomeCardsDate%3D1571595481892',
            'fbsr_161006757273279': 'PSBLw8aAWcoDGhAtbedHziNIng03R43lza2vyYqYHew.eyJ1c2VyX2lkIjoiNTA0NDMzNzY1IiwiY29kZSI6IkFRRHRKRE1zaHEyWGZqZTZpQWVYM2VmNnZGcUVrZ3Y1S2Jocm9mMWNmamdyczhtMlBtcUtzQUJ4dmdjcjJNUHZXTGRjTFlXLVJNMkFDZHhsZzVhNlhqdzJNbFBUYWs5WFRxNzEyU3g1UDZuQ3ZCSERaSzdiaU1mbjNzX180UzdfMmhYc2RaZGcxcHBfMDVVb3lVdVl1ZF8ydjk2VkhIdUJkY3RkSHNjcUY0US03S2h0UlNOU2RKa2VnM3RBVEVhN2p6VlJLeFJ1VVRSb2RPUi1QNUg2Wkh2dF9GWnNtOVdmVGtiZFRCNXUxYnREUlhBcFV0bl81WVE1MC1JWnZLUVh0TnhxWWJ1eno5VTZDeTVfMGFhM1VsSmQyMFpzVG5mejI2ZTFCbENlVi1xSFEzOUJBSEhTTi1jRmdQbDBxeE5Uby02MDFOXzZiQko1OHM3b2JrNkkxVktzQmpmeVJHWmdBeVpQcFNTYWFtMWp5dzROR1hmRWZzRFR5c0ZkRzYydWtqOCIsIm9hdXRoX3Rva2VuIjoiRUFBQ1NiMDZTM3I4QkFJcFVXNEt1MFFCWkI0Q1pCYjE0UFZYUldXNGxUUVlCZzZQOTU4aWVYWkFxUTFDTlF5VnAyUDlaQVNmY0VEV2xaQlpCNWkxRjhBUnNFMGFWTGtySnJha3BJZUtCWkEwNTdpYXRDbDhjdHdmcFZlQ2J0eEc2dFpDYzJmaTdTWGp5bnBaQTFUdFc2OVREcDhCWkFvektnWTFQMlFwN0VZMjBDbTA2WkN3T1NNU2N2N1pDSVZGZHhKamZNOVBTWkE4SXA3R1RVWkN6ajRwNHNyUnpUQiIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNTcxNTk1NDgyfQ',
            'RF_LAST_SEARCHED_CITY': 'San%20Jose',
            '__utmxx': '222895640.WTKnaAxUS8WuBy9wsrWkyg$0:1571278253:8035200:.uxw2gydsRRWC574IItzZJA$0:1568202211:8035200:.RTV_wZVsTh-aCSuerdlYSQ$0:1568742846:8035200:.Y2CmQl1SEm4efihwuTldA$0:1571595289:8035200:.DPiVULlyQUmf2VSSZa1iIg$0:1571595482:8035200.HPaeM5zMSp-5hxCpNhjEDg$0:1571514351:8035200:.Be2giBqURYSxBB66d5SfcQ$0:1570826559:8035200:',
            '_gat_UA-294985-1': '1',
            'unifiedLastSearch': 'name%3DAlameda%2520County%26subName%3DCA%252C%2520USA%26url%3D%252Fcounty%252F303%252FCA%252FAlameda-County%26id%3D9_303%26type%3D5%26isSavedSearch%3D%26countryCode%3DUS',
        }
        self.redfin_headers = {
            'sec-fetch-mode': 'cors',
            'x-newrelic-id': 'VQMDUFFaGwQJU1hSBAc=',
            'dnt': '1',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'accept': '*/*',
            'referer': 'https://www.redfin.com/county/303/CA/Alameda-County/filter/max-price=1.25M,min-beds=5,mr=5:345+5:343+6:17151',
            'authority': 'www.redfin.com',
            'sec-fetch-site': 'same-origin',
        }
        self.redfin_params = (
            ('al', '3'),
            ('market', 'sanfrancisco'),
            ('max_price', self.max_price),
            ('min_stories', '1'),
            ('num_beds', self.beds),
            ('num_baths', self.baths),
            ('num_homes', '10000'),
            ('ord', 'redfin-recommended-asc'),
            ('page_number', '1'),
            ('region_id', '345,343,17151,303'),
            ('region_type', '5,5,6,5'),
            ('sf', '1,2,3,5,6,7'),
            ('start', '0'),
            ('status', '9'),
            ('uipt', '1,2,3,4,5,6'),
            ('v', '8'),
        )
        self.air_dna_headers = {
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://www.airdna.co/vacation-rental-data/app/us/california/union-city/rentalizer',
            'Origin': 'https://www.airdna.co',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'DNT': '1',
        }

    def fetch_data(self):
        response = json.loads(requests.get('https://www.redfin.com/stingray/api/gis', headers=self.redfin_headers, params=self.redfin_params, cookies=self.redfin_cookies).text.replace('{}&&', ''))
        houses = response['payload']['homes']

        for house in houses:
            url = 'https://www.redfin.com' + house['url']
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
            days_on_market_info = self.driver.find_elements_by_css_selector('div.more-info > div > span')
            days_on_market = days_on_market_info[-1].find_element_by_css_selector('span.value').get_attribute('textContent').replace('days', '').strip() if len(days_on_market_info) == 0 else 'N/A'

            try:
                monthly_expense = self.driver.find_element_by_css_selector('div.CalculatorSummary > div.sectionText > p').get_attribute('textContent').replace('$', '').replace(' per month', '').replace(',', '')
                schools = '\n'.join([re.sub("(Parent Rating:)(.*)", '', info.get_attribute('textContent')).replace('homeGreatSchools', 'home GreatSchools').replace('SchoolPublic', 'School Public') for info in self.driver.find_elements_by_css_selector('tr.schools-table-row')[1:]])
            except:
                monthly_expense = 'N/A'
                schools = 'N/A'

            year_build = house['yearBuilt']['value'] if 'yearBuilt' in house.keys() and 'value' in house['yearBuilt'].keys() else 'N/A'
            lot_size = house['lotSize']['value'] if 'lotSize' in house.keys() and 'value' in house['lotSize'].keys() else 'N/A'

            # Get information from AirDNA
            full_address = f'{street_address}, {city}, {state}, USA'
            params = (
                ('access_token', 'MjkxMTI|8b0178bf0e564cbf96fc75b8518a5375'),
                ('city_id', '59193'),
                ('accommodates', '6'),
                ('bathrooms', baths if baths != 'N/A' else self.baths),
                ('bedrooms', beds if beds != 'N/A' else self.beds),
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

            # Get locality employment information
            county = self.search.by_zipcode(zip_code).county
            employment_total_covered = self.county_info[county]['employment_total_covered']  if county in self.county_info.keys() else 'N/A'
            twelve_month_change_pct = self.county_info[county]['twelve_month_change_pct'] if county in self.county_info.keys() else 'N/A'
            twelve_month_change = self.county_info[county]['twelve_month_change'] if county in self.county_info.keys() else 'N/A'
            avg_weekly_salary = self.county_info[county]['avg_weekly_salary'] if county in self.county_info.keys() else 'N/A'
            avg_weekly_12mo_change_salary = self.county_info[county]['avg_weekly_12mo_change_salary'] if county in self.county_info.keys() else 'N/A'

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

        self.driver.quit()

scrape = Scraper()
scrape.scrape()
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

        cookies = {
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
            'RF_LISTING_VIEWS': '112200998.111971925.112814555.111078864.113153741.113357034.112572946.111958975.112339817.112405158.112408910.110142814.113173890.112924556.81198215.112809087.112927527.111911401.110623683.94780200',
            '_dc_gtm_UA-294985-1': '1',
            '_gat_UA-294985-1': '1',
            'unifiedLastSearch': 'name%3D94587%26subName%3DCA%252C%2520USA%26url%3D%252Fzipcode%252F94587%26id%3D9_39234%26type%3D4%26isSavedSearch%3D%26countryCode%3DUS',
            'RF_VISITED': 'null',
            'userPreferences': 'parcels%3Dtrue%26schools%3Dfalse%26mapStyle%3Ds%26statistics%3Dtrue%26agcTooltip%3Dfalse%26agentReset%3Dfalse%26ldpRegister%3Dfalse%26afCard%3D2%26schoolType%3D0%26lastSeenLdp%3DnoSharedSearchCookie%26viewedSwipeableHomeCardsDate%3D1571594953149',
            'fbsr_161006757273279': 'POpWr1ot9SHRl_3SVlcT2JcqL1idzasaOhs7hyr8xEo.eyJ1c2VyX2lkIjoiNTA0NDMzNzY1IiwiY29kZSI6IkFRQW8yR3VxSHhiMERvbHBBdmJBbG4wcW9Yb2VVWVhsTzdfeWFRcDVfWVZqeGNCVzVxVjdFSnhUV3lkQkp4TW4tTjBlNWJ3VlEtRUxEeG9vNU0zZ1Fsbkg3aFlUU0FFUmNIUU5leThrTGJpa0Zyd1hIYzdRczFCMHBsdmRtZzhCaUJ3RlpHNW5YdVo2VDBpenpLRkpvcnVoTU9hQXJZdGo5NjNYaThFV0R2b1Bwd0daRURFUGRGVS1aOE01X2M2MEsyWnViOEpZZTVXNnloZF9zalBRQjQzTV82Uzh0Z1A0cWtWdUNlSUVoSFBCaF9VYWZfUTdCc0FMV0E3WFc5cjdjeWpyQ2NxTFlqZTJTc1BfOXRPUm95eUdKT3VaYXBTdk4tVWZRb3BJWDNqRmdLYTRyU0htaUoyVkhCWS01Q2RyVURzSnBnRjNMdE1rSEZRMWlmdjNWY2xwTFdfU3dBaGNaSzUwZmhmc1pCUEhUWHMySERiLUpyajRpLTJNTVBXYU5wMCIsIm9hdXRoX3Rva2VuIjoiRUFBQ1NiMDZTM3I4QkFJWkJFZnNyVDlFck13ekdaQUN2WEtPdGdaQnp6b2RxNGtMWkEwVE9HRVpBU1dSNHFxZEpIR000bUVmYmRjVW5lTFpCMnVMSGhaQmh3dFBndWJNazY0bVpCS1ZyTEtKMTQyalJoZnF0WkJ3cjNFcGt1aUVuSWFaQk1jc3ZaQldCZFlZQUZxZkZWUW14Y04yWkE5c012Vzk5dlZkbVpDSG9CdmRKaXpYQ3VRclNITHNLc1pBMkZBVkRMcm5mUTBaQllaQk9JdkZnY1pCTjBOc0oyRENRRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNTcxNTk0OTUzfQ',
            'RF_LAST_SEARCHED_CITY': 'Union%20City',
            '__utmxx': '222895640.WTKnaAxUS8WuBy9wsrWkyg$0:1571278253:8035200:.uxw2gydsRRWC574IItzZJA$0:1568202211:8035200:.RTV_wZVsTh-aCSuerdlYSQ$0:1568742846:8035200:.Y2CmQl1SEm4efihwuTldA$0:1571594874:8035200:.DPiVULlyQUmf2VSSZa1iIg$0:1571594953:8035200.HPaeM5zMSp-5hxCpNhjEDg$0:1571514351:8035200:.Be2giBqURYSxBB66d5SfcQ$0:1570826559:8035200:',
        }

        headers = {
            'sec-fetch-mode': 'cors',
            'x-newrelic-id': 'VQMDUFFaGwQJU1hSBAc=',
            'dnt': '1',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'accept': '*/*',
            'referer': 'https://www.redfin.com/zipcode/94587/filter/max-price=1.25M,min-beds=5,min-baths=3,viewport=37.6259:37.5617:-122.02162:-122.52974,no-outline',
            'authority': 'www.redfin.com',
            'sec-fetch-site': 'same-origin',
        }

        params = (
            ('al', '3'),
            ('market', 'sanfrancisco'),
            ('max_price', '1250000'),
            ('min_stories', '1'),
            ('num_baths', '3'),
            ('num_beds', '5'),
            ('num_homes', '350'),
            ('ord', 'redfin-recommended-asc'),
            ('page_number', '1'),
            ('poly', '-122.7838 37.52686,-121.76756 37.52686,-121.76756 37.65526,-122.7838 37.65526,-122.7838 37.52686'),
            ('sf', '1,2,3,5,6,7'),
            ('start', '0'),
            ('status', '9'),
            ('uipt', '1,2,3,4,5,6'),
            ('v', '8'),
            ('zoomLevel', '10'),
        )


        response = json.loads(requests.get('https://www.redfin.com/stingray/api/gis', headers=headers, params=params, cookies=cookies).text.replace('{}&&', ''))
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
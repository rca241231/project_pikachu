from modules.CountyEmployment import CountyInfo

max_price = '1250000'
beds = '5'
baths = '3'

county = CountyInfo()
county_info = county.get_employment_info("https://beta.bls.gov/maps/cew/CA?industry=10&geo_id=06000&chartData=3&distribution=Quantiles&pos_color=blue&neg_color=orange&showHideChart=show&ownerType=0")
redfin_cookies = {
    'RF_BROWSER_ID': 'bQi7XbxLSWS0UuKi2LGYfw',
    'RF_BID_UPDATED': '1',
    '_gcl_au': '1.1.2147212583.1571550525',
    'cto_lwid': '791dc4e9-319b-41a2-946c-f7a4c3b17f6d',
    '_ga': 'GA1.2.1980282281.1571550526',
    '_fbp': 'fb.1.1571550525572.747764494',
    'G_ENABLED_IDPS': 'google',
    'fbm_161006757273279': 'base_domain=.redfin.com',
    'RF_BUSINESS_MARKET': '2',
    '__gads': 'ID=b70c6ffb9e16a983:T=1571551223:S=ALNI_MaLwJf7KTaEu-wpz0KXXA40b3AaDA',
    'RF_CORVAIR_LAST_VERSION': '285.0.2',
    '_gid': 'GA1.2.1841975139.1571804879',
    'RF_LISTING_VIEWS': '113162708.27753221.110175074.111830133.112200998.113010849.113357034.112374379.113002794.113106800.113344122.113161528.113372282.113359991.111865057.112698508',
    'RF_LDP_VIEWS_FOR_CHAT': '%7B%22viewsData%22%3A%7B%2210-19-2019%22%3A%7B%22110175074%22%3A1%2C%22111830133%22%3A1%2C%22111865057%22%3A1%2C%22112374379%22%3A1%2C%22112698508%22%3A3%2C%22113002794%22%3A1%2C%22113010849%22%3A1%2C%22113106800%22%3A1%2C%22113161528%22%3A1%2C%22113344122%22%3A1%2C%22113357034%22%3A3%7D%2C%2210-22-2019%22%3A%7B%22113162708%22%3A1%7D%7D%2C%22expiration%22%3A%222021-10-19T06%3A00%3A23.028Z%22%2C%22totalPromptedLdps%22%3A0%7D',
    '__utmx': '222895640.DPiVULlyQUmf2VSSZa1iIg$0:0.Y2CmQl1SEm4efihwuTldA$0:1.cr1AtTjKTP2VQs80cLw4Lw$0:1.HPaeM5zMSp-5hxCpNhjEDg$0:1',
    'AKA_A2': 'A',
    'AMP_TOKEN': '%24NOT_FOUND',
    'RF_MARKET': 'socal',
    'RF_LAST_SEARCHED_CITY': 'Los%20Angeles',
    'unifiedLastSearch': 'name%3DSanta%2520Monica%26subName%3DSanta%2520Monica%252C%2520CA%252C%2520USA%26url%3D%252Fcity%252F17882%252FCA%252FSanta-Monica%26id%3D9_17882%26type%3D2%26isSavedSearch%3D%26countryCode%3DUS',
    'RF_GOOGLE_ONE_TAP_DISMISSED': 'lastDismissalDate%3D1571814243951%26doNotShowAgain%3Dtrue',
    'RF_BROWSER_CAPABILITIES': '%7B%22css-transitions%22%3Atrue%2C%22css-columns%22%3Atrue%2C%22css-generated-content%22%3Atrue%2C%22css-opacity%22%3Atrue%2C%22events-touch%22%3Afalse%2C%22geolocation%22%3Atrue%2C%22screen-size%22%3A2%2C%22screen-size-tiny%22%3Afalse%2C%22screen-size-small%22%3Afalse%2C%22screen-size-medium%22%3Afalse%2C%22screen-size-large%22%3Afalse%2C%22screen-size-huge%22%3Atrue%2C%22html-prefetch%22%3Afalse%2C%22html-range%22%3Atrue%2C%22html-form-validation%22%3Atrue%2C%22html-form-validation-with-required-notice%22%3Atrue%2C%22html-input-placeholder%22%3Atrue%2C%22html-input-placeholder-on-focus%22%3Atrue%2C%22ios-app-store%22%3Afalse%2C%22google-play-store%22%3Afalse%2C%22ios-web-view%22%3Afalse%2C%22android-web-view%22%3Afalse%2C%22activex-object%22%3Atrue%2C%22webgl%22%3Atrue%2C%22history%22%3Atrue%2C%22localstorage%22%3Atrue%2C%22sessionstorage%22%3Atrue%2C%22position-fixed-workaround%22%3Afalse%2C%22passive-event-listener%22%3Atrue%7D',
    '_dc_gtm_UA-294985-1': '1',
    'RF_VISITED': 'null',
    'userPreferences': 'parcels%3Dtrue%26schools%3Dfalse%26mapStyle%3Ds%26statistics%3Dtrue%26agcTooltip%3Dfalse%26agentReset%3Dfalse%26ldpRegister%3Dfalse%26afCard%3D2%26schoolType%3D0%26lastSeenLdp%3DnoSharedSearchCookie%26viewedSwipeableHomeCardsDate%3D1571814506070',
    '_gat_UA-294985-1': '1',
    'fbsr_161006757273279': '7ApZMFj4bouqBCIIinad-XqC8ZhB-3ZzRR_tw07HzSo.eyJ1c2VyX2lkIjoiNTA0NDMzNzY1IiwiY29kZSI6IkFRQ3o3UEJSUVgzTXpUaWhMbUJLeEZEMnNWcUZGdzl0RzJwQlVzWmFDTDhaaWxwZW1nejQtRkktaWQ4WnJRd1otdm1xQkZkVG0wRmRtLWk2TUE3UUlhMEM4bTlOUW4wTzYxanl2SVBWLURrSzBJeDVkUTY0cm9PRVNKVkNma0o0U2lJa2daMERXN3ZROG8yLU9VcW1FTUNlVnhXZVAxT092dnRzUG80Q3lSOF9YSTV1cFJHX2tGdklnYVQyYzBpYk8td196SmFXbVY3bFhIQjdkVU9ZZ3I4Q3BLWGFGWVFCOXNubHhuVG9rNmpiRXFPaGlqNHNNcXVveWhDd2NnUkg2Ymo2OGpFdmNyZnRrY2lJZlplbXBsNXNRQlRteDlOVmtzbUpoVnhNbV9UTDhfLTd1VlRaWE12VE41VThYeW9ZN3BjbElOQ2taWjVOR1Q1VzNHS0pjeXRsIiwib2F1dGhfdG9rZW4iOiJFQUFDU2IwNlMzcjhCQUxMZHZDVm1lR2s4ZmFONmZpWkFzOW14cUQ2dXcwaGhlbUR3cmEzN1pBbFIwWkFGc3BlNnlCUVFDR0VobXdaQjhiNW1mMUhmWkFZa1NrUlhLVGZSWkNVQjlPSEtsUlpBZ2phZk9tWkN3dGtUQXFlNmhCN0R5bXYxd1pCeFpDMGtqYXFxWWEycE4xNFpDSEhhOXRFcVdLbks5c0lkb0x2WHIxakpQcmRnQ0dKM2VZRWRVUHpZY2R1ZWFoZ2lJY1BjUWdzSEFSTFVtSFZoNjN6IiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE1NzE4MTQ1MDZ9',
    '__utmxx': '222895640.DPiVULlyQUmf2VSSZa1iIg$0:1571814507:8035200.Y2CmQl1SEm4efihwuTldA$0:1571807409:8035200:.cr1AtTjKTP2VQs80cLw4Lw$0:1571807409:8035200:.HPaeM5zMSp-5hxCpNhjEDg$0:1571807409:8035200:',
}

redfin_headers = {
    'sec-fetch-mode': 'cors',
    'x-newrelic-id': 'VQMDUFFaGwQJU1hSBAc=',
    'dnt': '1',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'accept': '*/*',
    'referer': 'https://www.redfin.com/city/17882/CA/Santa-Monica/filter/property-type=house+multifamily,max-price=1.25M,min-beds=5,viewport=34.12368:33.71914:-118.0203:-118.84771,mr=6:11203',
    'authority': 'www.redfin.com',
    'sec-fetch-site': 'same-origin',
}

redfin_params = (
    ('al', '1'),
    ('market', 'socal'),
    ('max_price', max_price),
    ('min_stories', '1'),
    ('num_beds', beds),
    ('num_baths', baths),
    ('num_homes', '1000'),
    ('ord', 'redfin-recommended-asc'),
    ('page_number', '1'),
    ('poly', '-118.84771 33.71914,-118.0203 33.71914,-118.0203 34.12368,-118.84771 34.12368,-118.84771 33.71914'),
    ('region_id', '11203,17882'),
    ('region_type', '6,6'),
    ('sf', '1,2,3,5,6,7'),
    ('start', '0'),
    ('status', '9'),
    ('uipt', '1,4'),
    ('v', '8'),
    ('zoomLevel', '11'),
)

import markets
import os
import multiprocessing
from modules.RealEstateInfo import Scraper

if __name__ == "__main__":
    try:
        os.remove('data.csv')
    except:
        print('data.csv does not exist.')

    print("Number of cpu: ", multiprocessing.cpu_count())

    for key, obj in markets.__dict__.items():
        if key[:2] != "__":
            print(f'Scraping data from {key}')
            county_info = eval(f"markets.{key}.county_info")
            redfin_cookies = eval(f"markets.{key}.redfin_cookies")
            redfin_headers = eval(f"markets.{key}.redfin_headers")
            redfin_params = eval(f"markets.{key}.redfin_params")
            scrape = Scraper(county_info, redfin_cookies, redfin_headers, redfin_params)
            scrape.scrape()



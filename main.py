import os
import multiprocessing
from modules.RealEstateInfo import Scraper
from markets import markets


def print_markets(markets):
    for market in markets.redfin_params_markets.keys():
        print(f"Getting information for {markets}, {markets.redfin_params_markets[market]}")


def connstruct_market_procs(markets):
    scrapers = [
        Scraper(
            markets.employment_info[markets.redfin_params_markets[key]['state']],
            markets.redfin_params_markets[key]['redfin_cookies'],
            markets.redfin_params_markets[key]['redfin_headers'],
            markets.redfin_params_markets[key]['redfin_params']
        )
        for key in markets.redfin_params_markets.keys()
    ]
    return scrapers


if __name__ == "__main__":
    # Delete data to fresh document
    try:
        os.remove('data.csv')
    except:
        print('data.csv does not exist.')
    print("Number of cpu: ", multiprocessing.cpu_count())

    # Load markets
    markets = markets.Markets()

    # Print markets
    print_markets(markets)

    # Construct scrapers
    market_scraper_procs = connstruct_market_procs(markets)

    # Start process
    process = []
    for market_scraper_proc in market_scraper_procs:
        proc = multiprocessing.Process(target=market_scraper_proc.scrape(), args=())
        process.append(proc)
        proc.start()

    for proc in process:
        proc.join()

import os
import multiprocessing
from modules.RealEstateInfo import Scraper
from markets import markets

# Market Constants
interest_rate = 0.04
borrowing_pct = 0.8
mortgage_term_years = 30
insurance_cost = 1500

def print_markets(markets):
    for market in markets.redfin_params_markets.keys():
        print(f"Getting information for {market}, {markets.redfin_params_markets[market]['state']}")


def connstruct_market_procs(markets):
    scrapers = [
        Scraper(
            county_info=markets.employment_info[markets.redfin_params_markets[key]['state']],
            redfin_cookies=markets.redfin_params_markets[key]['redfin_cookies'],
            redfin_headers=markets.redfin_params_markets[key]['redfin_headers'],
            redfin_params=markets.redfin_params_markets[key]['redfin_params'],
            interest_rate=interest_rate,
            borrowing_pct=borrowing_pct,
            mortgage_term_years=mortgage_term_years,
            insurance_cost=insurance_cost
        )
        for key in markets.redfin_params_markets.keys()
    ]
    return scrapers


if __name__ == "__main__":
    # Delete data to refresh document
    try:
        os.remove('data.csv')
    except:
        print('data.csv does not exist.')
    print("Number of CPUs: ", multiprocessing.cpu_count())

    # Load markets
    markets = markets.Markets()

    # Print markets
    print_markets(markets)

    # Construct scrapers
    market_scraper_procs = connstruct_market_procs(markets)

    # Start process
    process = []
    for market_scraper_proc in market_scraper_procs:
        proc = multiprocessing.Process(target=market_scraper_proc.scrape, args=())
        process.append(proc)
        proc.start()

    for proc in process:
        proc.join()

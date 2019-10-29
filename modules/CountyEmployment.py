from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_DRIVER_PATH = './chromedriver'

class CountyInfo():
    def __init__(self):
        self.CHROME_DRIVER_PATH = './chromedriver'

    def get_employment_info(self, state):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(self.CHROME_DRIVER_PATH, options=options)
        county_dict = {}
        url = f"https://beta.bls.gov/maps/cew/{state}?industry=10&geo_id=06000&chartData=3&distribution=Quantiles&pos_color=blue&neg_color=orange&showHideChart=show&ownerType=0"

        driver.get(url)
        county_list = [info.find_element_by_css_selector('td.align-left:nth-of-type(1) > a').get_attribute('textContent').strip() for info in driver.find_element_by_id('datatable1').find_elements_by_css_selector('tbody > tr')]
        employment_total_covered_list = [info.find_element_by_css_selector('td:nth-of-type(3) > a').get_attribute('textContent').strip() for info in driver.find_element_by_id('datatable1').find_elements_by_css_selector('tbody > tr')]
        twelve_month_change_pct_list = [info.find_element_by_css_selector('td:nth-of-type(4)').get_attribute('textContent').strip() for info in driver.find_element_by_id('datatable1').find_elements_by_css_selector('tbody > tr')]
        twelve_month_change_list = [info.find_element_by_css_selector('td:nth-of-type(5)').get_attribute('textContent').strip() for info in driver.find_element_by_id('datatable1').find_elements_by_css_selector('tbody > tr')]
        avg_weekly_salary_list = [info.find_element_by_css_selector('td:nth-of-type(7) > a').get_attribute('textContent').strip() for info in driver.find_element_by_id('datatable1').find_elements_by_css_selector('tbody > tr')]
        avg_weekly_12mo_change_salary_list = [info.find_element_by_css_selector('td:nth-of-type(8)').get_attribute('textContent').strip() for info in driver.find_element_by_id('datatable1').find_elements_by_css_selector('tbody > tr')]

        for (county,
             employment_total_covered,
             twelve_month_change_pct,
             twelve_month_change,
             avg_weekly_salary,
             avg_weekly_12mo_change_salary
        ) in zip(county_list,
                 employment_total_covered_list,
                 twelve_month_change_pct_list,
                 twelve_month_change_list,
                 avg_weekly_salary_list,
                 avg_weekly_12mo_change_salary_list
        ):
            if state not in county_dict.keys():
                county_dict[state] = {}
            county_dict[state][county] = {
                'employment_total_covered': employment_total_covered,
                'twelve_month_change_pct': twelve_month_change_pct,
                'twelve_month_change': twelve_month_change,
                'avg_weekly_salary': avg_weekly_salary,
                'avg_weekly_12mo_change_salary': avg_weekly_12mo_change_salary
            }

        driver.quit()

        return county_dict
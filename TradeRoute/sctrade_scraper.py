from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from collections import namedtuple
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
import locale
import json
import time
import re


locale.setlocale(locale.LC_ALL, '')


Shop = namedtuple("Shop", "path buys sells")
Commodity = namedtuple("Commodity", "name price stock refresh")
ua = UserAgent()


BASE_URL = "https://sc-trade.tools/shops/"
HEADERS = {
    "User-Agent": ua.random
}
SHOP_SELECT = "//div[contains(@class, 'form-select-options')]"
SHOP_OPTION = ".//div[contains(@class, 'form-select-option')]"
SELL_WAIT = "//h2[contains(text(),'Sell')]"
BUY_WAIT = "//h2[contains(text(),'Buy')]"
BUY_TABLE = "//h2[contains(text(),'Buy')]/following-sibling::app-transactions/table"
SELL_TABLE = "//h2[contains(text(),'Sell')]/following-sibling::app-transactions/table"
INVENTORY_REGEX = r"Max (?P<stock>[0-9,]+) SCU \+ [<>=]*(?P<rate>[0-9,]+)/min"


chrom_param = "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " \
              "Chrome/101.0.4951.67 Safari/537.36,--lang=en,--start-maximized,--ignore-certificate-errors "


def get_shops(driver, wait):
    driver.get(BASE_URL)
    wait.until(EC.presence_of_element_located((By.XPATH, SHOP_SELECT)))
    selector = driver.find_element(By.XPATH, SHOP_SELECT)
    selector_options = selector.find_elements(By.XPATH, SHOP_OPTION)
    return [s.get_attribute("innerText").strip() for s in selector_options]


def get_table_commodities(table):
    rows = table.find_elements(By.XPATH, ".//tbody/tr")
    result = []
    for r in rows:
        row_elements = r.find_elements(By.XPATH, ".//td")

        com_elt = row_elements[0].find_element(By.XPATH, ".//a")
        price_elt = row_elements[1].find_element(By.XPATH, ".//span")
        invent_elt = row_elements[2]

        commodity_name = com_elt.text.strip()
        price = locale.atof(price_elt.text.strip()) / 100
        invent_text = invent_elt.text.strip()
        invent_search = re.search(INVENTORY_REGEX, invent_text)
        if invent_search is None:
            print(invent_text)
        stock_amt = locale.atof(invent_search.group("stock")) * 100
        refresh_rate = locale.atof(invent_search.group("rate")) * 100
        com = Commodity(commodity_name, price, stock_amt, refresh_rate)
        result.append(com)
    return result


if __name__ == "__main__":
    chrome_options = Options()
    for param in chrom_param.split(","):
        if len(param.strip()) != 0:
            chrome_options.add_argument(param.strip())
    driver = webdriver.Chrome(r"./chromedriver", options=chrome_options)
    wait = WebDriverWait(driver, 10)

    shops = get_shops(driver, wait)
    shop_list = []

    for s in shops:
        print("Retrieving: " + s)
        driver.get(BASE_URL + s)

        wait.until(EC.presence_of_element_located((By.XPATH, SELL_WAIT)))
        wait.until(EC.presence_of_element_located((By.XPATH, BUY_WAIT)))
        time.sleep(1)

        try:
            buy_table = driver.find_element(By.XPATH, BUY_TABLE)
            buy_coms = get_table_commodities(buy_table)
        except NoSuchElementException:
            buy_coms = []
        try:
            sell_table = driver.find_element(By.XPATH, SELL_TABLE)
            sell_coms = get_table_commodities(sell_table)
        except NoSuchElementException:
            sell_coms = []

        shop = Shop(s, buy_coms, sell_coms)
        shop_list.append(shop)

    with open("shops.json", "w") as fp:
        json.dump(shop_list, fp, )



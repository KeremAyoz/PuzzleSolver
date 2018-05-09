from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def parse_google_search(query, site=None):
    word_list = set()
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")
    search_bar = driver.switch_to.active_element
    if site is None:
        search_bar.send_keys(query)
    else:
        search_bar.send_keys(query + " " + "site:" + site)

    search_bar.send_keys(Keys.ENTER)
    driver.get(driver.current_url + "&lr=lang_en")

    # result_elements = driver.find_elements_by_class_name("st")
    # for elem in result_elements:
    #     for word in elem.text.split():
    #         word_list.add(word)

    result_headers = driver.find_elements_by_id("rso")
    for elem in result_headers:
        for word in elem.text.split():
            word_list.add(word)

    driver.close()
    return word_list


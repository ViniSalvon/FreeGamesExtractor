from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from time import sleep

import constants as ct
import json


def scroll_to_the_bottom(driver: WebDriver):
    at_bottom = driver.execute_script("return (window.innerHeight + window.scrollY) >= document.body.scrollHeight;")

    while not at_bottom:
        driver.execute_script("window.scrollBy(0, 100);")
        sleep(0.1)
        at_bottom = driver.execute_script("return (window.innerHeight + window.scrollY) >= document.body.scrollHeight;")
    
    sleep(0.3)
    return


def extract_titles(entries: list[WebElement], titles: list[WebElement]) -> tuple[list[WebElement]]:
    output_titles: list = []
    output_links: list = []

    for id, entry in enumerate(entries):
        if '\npromoted' in entry.text:
            continue
        else:
            output_titles.append(titles[id].text)
            output_links.append(titles[id].get_attribute('href'))
    
    return (output_titles, output_links)


def extract_dates(dates: list[WebElement]) -> list:
    output_dates = []
    for date in dates:
        new_date = date.get_attribute('datetime').split('T')[0]
        output_dates.append(new_date)
    
    return output_dates


def save_to_json(content: list, first_n_entries: int = None):
    data_to_save = content[:first_n_entries] if first_n_entries else content

    with open('free_games.json', 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    return



if __name__ == '__main__':
    f: WebDriver = Firefox()
    f.get(ct.URL_MAIN)

    wdw_wait_0 = WebDriverWait(
        driver=f,
        timeout=ct.WDW_TIMEOUT_0,
        poll_frequency=ct.WDW_PF_0,
        ignored_exceptions=None
    )

    wdw_wait_0.until(EC.element_to_be_clickable((By.XPATH, ct.XP_DIV_ENTRIES)))
    entries_divs: list[WebElement] = f.find_elements(By.XPATH, ct.XP_DIV_ENTRIES)
    
    wdw_wait_0.until(EC.element_to_be_clickable((By.XPATH, ct.XP_TITLES)))
    all_titles: list[WebElement] = f.find_elements(By.XPATH, ct.XP_TITLES)

    wdw_wait_0.until(EC.element_to_be_clickable((By.XPATH, ct.XP_ENTRY_TIME)))
    scroll_to_the_bottom(f)
    all_times: list[WebElement] = f.find_elements(By.XPATH, ct.XP_ENTRY_TIME)

    titles, links = extract_titles(entries_divs, all_titles)
    dates = extract_dates(all_times)

    titles = titles[2:]
    links = links[2:]
    dates = dates[2:]
    
    output = []
    for it in range(len(titles)):
        output.append({'game': titles[it], 'link': links[it], 'date': dates[it]})
    
    save_to_json(output)


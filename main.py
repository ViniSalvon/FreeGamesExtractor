from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from rich import print
import constants as CT
import json
from tqdm import tqdm


def zoom_out(driver: Firefox, zoom_out_qtd: int):
    driver.set_context('chrome')
    zoom_step = 0.1
    current_zoom = float(driver.execute_script(
        "return Services.prefs.getCharPref('layout.css.devPixelsPerPx');"
    ))
    new_zoom = max(0.3, current_zoom - (zoom_step * zoom_out_qtd))

    driver.execute_script(
        f"Services.prefs.setCharPref('layout.css.devPixelsPerPx', '{new_zoom}');"
    )

    driver.set_context('content')
    return


def save_to_json(content: list, first_n_entries: int = None):

    if first_n_entries and not (isinstance(first_n_entries, int)):
        raise ValueError("first_n_entries deve ser um inteiro")
    data_to_save = content[:first_n_entries] if first_n_entries else content

    with open('free_games.json', 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    return


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')  # Ativa o modo headless

    f: WebDriver = Firefox(options=options)  # Passa as opções ao inicializar o WebDriver
   
    wdw_wait_0 = WebDriverWait(
        driver=f,
        timeout=CT.WDW_TIMEOUT_0,
        poll_frequency=CT.WDW_PF_0,
        ignored_exceptions=None
    )

    print('[bold green]Inicializando o sistema e navegando...[/bold green]')
 
    f.get("about:newtab")
    f.maximize_window()
    zoom_out(f, 5)


    f.get(CT.URL_MAIN)
    
    print("[bold green]Coletando dados...[/bold green]")
    wdw_wait_0.until(EC.element_to_be_clickable((By.XPATH, CT.XP_ENTRIES)))
    wdw_wait_0.until(EC.element_to_be_clickable((By.XPATH, CT.XP_ENTRY_TIME)))
    
    entries_divs: list[WebElement] = f.find_elements(By.XPATH, CT.XP_ENTRIES)

    output = []
    num_entries = len(entries_divs) - 2
    with tqdm(total=num_entries, desc="\033[1;32mProcessando dados...\033[0m", unit="entry", colour='green') as pbar:
        for div in entries_divs[2:]:
            title: str = div.find_element(By.XPATH, CT.XP_TITLES).text
            link: str = div.find_element(By.XPATH, CT.XP_TITLES).get_attribute('href')
            date: str = div.find_element(By.XPATH, CT.XP_ENTRY_TIME).get_attribute('datetime').split('T')[0]
            output.append({'title': title, 'link': link, 'date': date})
            pbar.update(1)
    
    print("[bold green]Salvando dados em free_games.json...[/bold green]")
    save_to_json(output, CT.SAVE_ENTRIES)

    f.close()
    print("[bold green]Dados salvos com sucesso![/bold green]")



    

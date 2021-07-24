from os import link
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup

def get_top_result(name: str):
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    driver.get("https://myanimelist.net/anime.php")
    # print(driver.title)

    search_bar = driver.find_element_by_id("q")
    search_bar.send_keys(name)
    search_bar.send_keys(Keys.RETURN)

    try:
        content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "content")))
        cur_url = driver.current_url
        page = requests.get(cur_url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="content")
        link = results.find("a", class_="hoverinfo_trigger")["href"]
        return link

    except:
        driver.quit()

    driver.close()


def get_image_character(name: str) -> str:
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    driver.get("https://myanimelist.net/character.php")

    search_bar = driver.find_element_by_id("q")
    search_bar.send_keys(name)
    search_bar.send_keys(Keys.RETURN)

    try:
        content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "content")))
        cur_url = driver.current_url
        page = requests.get(cur_url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="content")
        link = results.find("img", class_="lazyload")["data-src"]

        return link.replace("/r/42x62", '')

    except:
        driver.quit()

    driver.close()
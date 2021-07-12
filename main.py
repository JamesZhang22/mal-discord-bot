import requests
from bs4 import BeautifulSoup
from typing import Dict


def create_dict_of_name_id() -> Dict[int, str]:
    name_id_dict = {}
    page = requests.get("https://myanimelist.net/sitemap/anime-000.xml")
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.find_all("url")
    for element in elements:
        link = str(element.find("loc"))
        new = link.replace("<loc>https://myanimelist.net/anime/", '').replace("</loc>", '').replace("/", ", ")
        new_split = new.split(', ')
        name_id_dict[new_split[1]] = new_split[0]

    return name_id_dict

name_id = create_dict_of_name_id()


def get_anime_stats(name: str) -> str:
    url = "https://myanimelist.net/anime/" + str(name_id[name])
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="content")

    rating = results.find("div", class_="score-label score-8").text
    rank_wrapper = results.find("span", class_="numbers ranked")
    rank = rank_wrapper.find("strong").text
    popularity_wrapper = results.find("span", class_="numbers popularity")
    popularity = popularity_wrapper.find("strong").text

    return rating, rank, popularity


example = get_anime_stats('Cowboy_Bebop')
print(example)

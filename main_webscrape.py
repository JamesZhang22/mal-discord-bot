import requests
from bs4 import BeautifulSoup
from typing import Dict, List


def create_dict_of_name_id() -> Dict[int, str]:
    name_id_dict = {}
    page = requests.get("https://myanimelist.net/sitemap/anime-000.xml")
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.find_all("url")
    for element in elements:
        link = str(element.find("loc"))
        new = link.replace("<loc>https://myanimelist.net/anime/", '').replace("</loc>", '').replace("/", ", ")
        new_split = new.split(', ')
        name_id_dict[new_split[1].replace("__", ": ").replace("_", " ").lower()] = new_split[0]

    return name_id_dict

name_id = create_dict_of_name_id()

all_genres = ['action', 'adventure', 'cars', 'comedy', 'dementia', 'demons', 'drama', 'ecchi', 'fantasy', 'game', 'harem', 'hentai', 'historical', 'horror', 'josei', 'kids', 'magic', 'martial arts', 'mecha', 'military', 'music', 'mystery', 'parody', 'police', 'psychological', 'romance', 'samurai', 'school', 'sci-fi', 'seinen', 'shoujo', 'shoujo ai', 'shounen', 'shounen ai', 'slice of life', 'space', 'sports', 'super power', 'supernatural', 'thriller', 'vampire', 'yoai', 'yuri']


def get_anime_stats(name: str) -> str:
    name = name.replace("(", '').replace(")", '').lower()
    url = "https://myanimelist.net/anime/" + str(name_id[name])
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="content")

    name_wrapper = soup.find("div", class_="h1-title")
    true_name = name_wrapper.find("strong").text
    rating_wrapper = results.find("div", class_="fl-l score")
    rating = rating_wrapper.find("div").text
    rank_wrapper = results.find("span", class_="numbers ranked")
    rank = rank_wrapper.find("strong").text
    popularity_wrapper = results.find("span", class_="numbers popularity")
    popularity = popularity_wrapper.find("strong").text
    episodes = results.find("div", class_="spaceit").text.replace("\n", "").replace(" ", "").replace("Episodes:", "")
    genres_wrapper = results.find_all("a")
    genres = []
    for genre in genres_wrapper:
        if genre.text.lower() in all_genres:
            genres.append(genre.text)
    similars = []
    similar_shows_wrapper = results.find_all("ul", class_="anime-slide js-anime-slide")
    for similar_show_wrapper in similar_shows_wrapper:
        if similar_show_wrapper['data-slide'] == "7":
            true_similar_shows_wrapper = similar_show_wrapper
            similar_shows = true_similar_shows_wrapper.find_all("li", class_="btn-anime")
        elif similar_show_wrapper['data-slide'] == "8":
            true_similar_shows_wrapper = similar_show_wrapper
            similar_shows = true_similar_shows_wrapper.find_all("li", class_="btn-anime auto")
    for show in similar_shows:
        similars.append(show['title'])
    img_wrapper = results.find("img", alt=true_name)
    img_url= img_wrapper['data-src']


    return true_name, rating, rank, popularity, episodes, genres, similars, img_url


def get_genre_list(genre: str) -> List[str]:
    shows = []
    genres = {
        'action': 1, 
        'adventure': 2, 
        'cars': 3, 
        'comedy': 4, 
        'dementia': 5, 
        'demons': 6, 
        'drama': 8, 
        'ecchi': 9, 
        'fantasy': 10, 
        'game': 11, 
        'harem': 35, 
        'hentai': 12, 
        'historical': 13, 
        'horror': 14, 
        'josei': 43, 
        'kids': 15, 
        'magic': 16, 
        'martial arts': 17, 
        'mecha': 18, 
        'military': 38, 
        'music': 19, 
        'mystery': 7, 
        'parody': 20, 
        'police': 39, 
        'psychological': 40, 
        'romance': 22, 
        'samurai': 21, 
        'school': 23, 
        'sci-fi': 24, 
        'seinen': 42, 
        'shoujo': 25, 
        'shoujo ai': 26, 
        'shounen': 27, 
        'shounen ai': 28, 
        'slice of life': 36, 
        'space': 29, 
        'sports': 30, 
        'super power': 31, 
        'supernatural': 37, 
        'thriller': 41,
        'vampire': 32, 
        'yoai': 33, 
        'yuri': 34
    }

    number = genres[genre.lower()]
    url = "https://myanimelist.net/anime/genre/" + str(number)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="content")

    name_wrapper = results.find_all("h2", class_="h2_anime_title")
    for name in name_wrapper:
        link = name.find("a")
        shows.append(link.text)

    return shows
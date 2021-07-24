from os import stat
import requests, random
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple

from automation import *


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


def get_anime_stats(name: str) -> Tuple:
    name = name.replace("(", '').replace(")", '').lower()
    url = get_top_result(name)
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
    genres = genres[0:3]
    genres = ', '.join(genres)
    similars = []
    similar_shows_wrapper = results.find_all("ul", class_="anime-slide js-anime-slide")
    for similar_show_wrapper in similar_shows_wrapper:
        if similar_show_wrapper['data-slide'] == "7":
            true_similar_shows_wrapper = similar_show_wrapper
            similar_shows = true_similar_shows_wrapper.find_all("li", class_="btn-anime")
        elif similar_show_wrapper['data-slide'] == "8":
            true_similar_shows_wrapper = similar_show_wrapper
            similar_shows = true_similar_shows_wrapper.find_all("li", class_="btn-anime")
    for show in similar_shows:
        similars.append(show['title'])
    similars = similars[0:3]
    similars = ', '.join(similars)
    img_wrapper = results.find("img", alt=true_name)
    img_url= img_wrapper['data-src']
    desc = results.find("p", itemprop="description").text.split("\n")[0]


    return true_name, rating, rank, popularity, episodes, genres, similars, img_url, desc, url


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


def get_user(name: str) -> Tuple:
    url = "https://myanimelist.net/profile/" + name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="contentWrapper")

    name = results.find("span", class_="di-ib po-r")
    if not name:
        return False
    else:
        name = results.find("span", class_="di-ib po-r").text.replace("\n", '').strip()
    image_wrapper = results.find("div", class_="user-image mb8")
    image_url = image_wrapper.find("img")["data-src"]
    online_joined_wrapper = results.find("ul", class_="user-status border-top pb8 mb4")
    online_joined_li = online_joined_wrapper.find_all("span")
    online = online_joined_li[1].text
    infotexts = {}
    infotext_wrapper = results.find("ul", class_="user-status border-top mt12 mb12")
    infotext_details = infotext_wrapper.find_all("li", class_="link")
    for infotext in infotext_details:
        key = infotext.find("span", class_="user-status-title di-ib fl-l fw-b").text
        val = infotext.find("span", class_="user-status-title di-ib fl-r fw-b")
        if not val:
            infotexts[key] = 0
        else:
            infotexts[key] = val.text
    friends = results.find("a", class_="fl-r fs11 fw-n ff-Verdana").text.replace("All (", "").replace(")", "")


    return name, image_url, online, infotexts, friends, url


def get_user_anime_stats(name: str) -> Tuple:
    url = "https://myanimelist.net/profile/" + name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="contentWrapper")

    stats_container = results.find("div", class_="stats anime")
    if not stats_container:
        return False
    name = results.find("span", class_="di-ib po-r").text.replace("\n", '').strip()
    image_wrapper = results.find("div", class_="user-image mb8")
    image_url = image_wrapper.find("img")["data-src"]
    entries_container = stats_container.find("ul", class_="stats-data fl-r")
    entries = entries_container.find("span", class_="di-ib fl-r").text
    info_wrapper = stats_container.find("ul", class_="stats-status fl-l")
    infotexts = []
    infotexts_wrapper = info_wrapper.find_all("li", class_="clearfix mb12")
    for infotext in infotexts_wrapper:
        val = infotext.find("span").text
        infotexts.append(val)
    shows = []
    favorites_wrapper = results.find("ul", class_="favorites-list anime")
    if not favorites_wrapper:
        shows = []
    else:
        favorite_shows = favorites_wrapper.find_all("li", class_="list di-t mb8")
        for show in favorite_shows:
            show_container = show.find("div", class_="di-tc va-t pl8 data")
            show_name = show_container.find("a").text
            shows.append(show_name)

    return name, entries, infotexts, shows[0:5], url, image_url


def get_user_manga_stats(name: str) -> Tuple:
    url = "https://myanimelist.net/profile/" + name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="contentWrapper")

    stats_container = results.find("div", class_="stats manga")
    if not stats_container:
        return False
    name = results.find("span", class_="di-ib po-r").text.replace("\n", '').strip()
    image_wrapper = results.find("div", class_="user-image mb8")
    image_url = image_wrapper.find("img")["data-src"]
    entries_container = stats_container.find("ul", class_="stats-data fl-r")
    entries = entries_container.find("span", class_="di-ib fl-r").text
    info_wrapper = results.find_all("ul", class_="stats-status fl-l")[1]
    infotexts = []
    infotexts_wrapper = info_wrapper.find_all("li", class_="clearfix mb12")
    for infotext in infotexts_wrapper:
        val = infotext.find("span").text
        infotexts.append(val)
    mangas = []
    favorites_wrapper = results.find("ul", class_="favorites-list manga")
    if not favorites_wrapper:
        manga = []
    else:
        favorite_mangas = favorites_wrapper.find_all("li", class_="list di-t mb8")
        for manga in favorite_mangas:
            manga_container = manga.find("div", class_="di-tc va-t pl8 data")
            manga_name = manga_container.find("a").text
            mangas.append(manga_name)

    return name, entries, infotexts, mangas[0:5], url, image_url


def get_random_character() -> str:
    # url = "https://myanimelist.net/character.php?limit=150"
    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, "html.parser")
    # results = soup.find(id="contentWrapper")
    # character_names = []
    # character_wrappers = results.find_all("td", class_="people")
    # for character_wrapper in character_wrappers:
    #     character_name = character_wrapper.find("a", class_="fs14 fw-b").text
    #     character_names.append(character_name)

    data_list = ['Lamperouge, Lelouch', 'Levi', 'Lawliet, L', 'Monkey D., Luffy', 'Okabe, Rintarou', 'Yagami, Light', 'Roronoa, Zoro', 'Zoldyck, Killua', 'Elric, Edward', 'Uzumaki, Naruto', 'Sakata, Gintoki', 'Makise, Kurisu', 'Uchiha, Itachi', 'Guts', 'Ackerman, Mikasa', 'Hikigaya, Hachiman', 'Yeager, Eren', 'Kaneki, Ken', 'Rem', 'Saitama', 'Hatake, Kakashi', 'Spiegel, Spike', 'Kirigaya, Kazuto', 'Yato', 'Senjougahara, Hitagi', 'Megumin', 'Gojou, Satoru', 'Joestar, Joseph', 'Morow, Hisoka', 'Mustang, Roy', 'Zero Two', 'Kamina', 'Aisaka, Taiga', 'Oshino, Shinobu', 'Sakurajima, Mai', 'Saber', 'Gasai, Yuno', 'Onizuka, Eikichi', 'Yuuki, Asuna', 'Araragi, Koyomi', 'Holo', 'Dazai, Osamu', 'Alucard', 'Todoroki, Shouto', 'Reigen, Arataka', 'Evergarden, Violet', 'Uchiha, Sasuke', 'Kurosaki, Ichigo', 'Midoriya, Izuku', 'Orihara, Izaya', 'C.C.', 'Miyazono, Kaori', 'Sanji', 'Son, Gokuu', 'Dragneel, Natsu', 'Oreki, Houtarou', 'Michaelis, Sebastian', 'Souryuu, Asuka Langley', 'Toosaka, Rin', 'Akemi, Homura', 'Emilia', 'Bakugou, Katsuki', 'Yukinoshita, Yukino', 'Smith, Erwin', 'Kuujou, Joutarou', 'Revy', 'Usui, Takumi', 'Kamado, Tanjirou', 'Takanashi, Rikka', 'Freecss, Gon', 'Kurapika', 'Scarlet, Erza', 'Satou, Kazuma', 'Koro-sensei', 'Heiwajima, Shizuo', 'Arlert, Armin', 'Gremory, Rias', 'Kageyama, Shigeo', 'Hei', 'Shinomiya, Kaguya', 'Misaka, Mikoto', 'Senkuu', 'Yukihira, Souma', 'Shiina, Mashiro', 'Saiki, Kusuo', 'Ayanokouji, Kiyotaka', 'Tokisaki, Kurumi', 'Nakano, Miku', 'Vegeta', 'Askeladd', 'Hinata, Shouyou', 'Akabane, Karma', 'Sora', 'Emiya, Kiritsugu', 'Trafalgar, Law', 'Suzumiya, Haruhi', 'Fujiwara, Chika', 'Matoi, Ryuuko', 'Nara, Shikamaru', 'Ishigami, Yuu', 'Natsuki, Subaru', 'Zoë, Hange', 'Shiro', 'Liebert, Johan', 'Izumi, Konata', 'Ginko', 'Ayanami, Rei', 'Ikari, Shinji', 'Tachibana, Kanade', 'Tempest, Rimuru', 'Nico, Robin', 'Vash the Stampede', 'Meruem', 'Nishimiya, Shouko', 'Simon', 'Okazaki, Tomoya', 'Gilgamesh', 'Elric, Alphonse', 'Mugen', 'Okumura, Rin', 'Azusagawa, Sakuta', 'Kageyama, Tobio', 'Lucy', 'Akiyama, Mio', 'Agatsuma, Zenitsu', 'Hirasawa, Yui', 'Brando, Dio', 'Kamado, Nezuko', 'Katsuragi, Misato', 'Himura, Kenshin', 'Ban', 'Usopp', 'Kaiki, Deishuu', 'Nami', 'Tony Tony, Chopper', 'Gaara', 'Suzuya, Juuzou', 'Hyuuga, Hinata', 'Nishinoya, Yuu', 'Phantomhive, Ciel', 'Souma, Kyou', 'Degurechaff, Tanya', 'Oikawa, Tooru', 'Akame', 'Kirisaki, Chitoge', 'Jiraiya', 'Kagura', 'Shiina, Mayuri', 'Zeppeli, Gyro', 'Furukawa, Nagisa', 'Kyon', 'Callenreese, Aslan Jade', 'Death the Kid', 'Walker, Allen', 'Accelerator', 'Ryuk', 'Ichinose, Chizuru', 'Inaba, Himeko', 'Kirishima, Touka', 'Zaraki, Kenpachi', 'Himejima, Akeno', 'Kusanagi, Motoko', 'Momonga', 'Kira, Yoshikage', 'Miyamura, Izumi', 'Nakano, Nino', 'Griffith', 'Kougami, Shinya', 'Meliodas', 'Yuzuriha, Inori', 'Jabami, Yumeko', 'Hanekawa, Tsubasa', 'Iwakura, Lain', 'Itadori, Yuuji', 'Hashibira, Inosuke', 'Kamui, Kanna', 'Kuroko, Tetsuya', 'Makishima, Shougo', 'Raphtalia', 'Tomoe', 'Kozume, Kenma', 'Natsume, Takashi', 'Aqua', 'Namikaze, Minato', 'Tomori, Nao', 'Thorfinn', 'Archer', 'Esdeath', 'Suou, Tamaki', 'Kochou, Shinobu', 'Katou, Megumi', 'All Might', 'Howl', 'Nagato, Yuki', 'Ryougi, Shiki', 'Power', 'Uchiha, Madara', 'Sung, Jin-Woo', 'Asta', 'Blouse, Sasha']
    
    return random.choice(data_list)

print(get_random_character())
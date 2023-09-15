import time
import subprocess
import os
import random
import pyperclip
from InquirerPy import inquirer
from jikanpy import Jikan

api = Jikan()

# Genre IDs from Jikan
# Master dictionary, this is so we can have our selected genre's
# name appear in InquirerPy when we use it later down in the prompts
masterdict = {
    "Shounen": 27,
    "Fantasy": 10,
    "Drama": 8,
    "Sci-fi": 24,
    "Romance": 22,
    "Comedy": 4,
    "Seinen": 42,
    "Horror": 14,
    "Sports": 30,
    "Mecha": 18,
}

anime_set: dict[str, dict] = dict()
manga_set: dict[str, dict] = dict()

def get_random_anime(genre_id):
    # Rate limits for the API
    requests_per_second = 2
    start_time = time.time()

    # This is a hack, since Jikan doesn't allow us to random search based on genre
    # we have to submit an empty query with a specified genre -- the genre_id parameter,
    # it'll be used down in the code when we select our genre -- then we fetch
    # a couple of anime based on that query, return just the title, and finally we
    # fetch a random anime from that anime pool we got
    for i in range(10):
        elapsed_time = time.time() - start_time

        # Rate limit delays so we don't bork the API
        if elapsed_time < 1.0 / requests_per_second:
            time.sleep(1.0 / requests_per_second - elapsed_time)

        response = api.search(
            search_type="anime", query="", page=i + 1, parameters={"genres": genre_id}
        )

        start_time = time.time()

        for anime in response["data"]:
            anime_set[anime["title"]] = anime

    random_anime_title = random.choice(list(anime_set.keys()))
    return random_anime_title # return the random anime so we can use it down in the main func
    

def get_random_manga(genre_id):
    requests_per_second = 2
    start_time = time.time()

    for i in range(10):
        elapsed_time = time.time() - start_time

        if elapsed_time < 1.0 / requests_per_second:
            time.sleep(1.0 / requests_per_second - elapsed_time)

        response = api.search(
            search_type="manga", query="", page=i + 1, parameters={"genres": genre_id}
        )

        start_time = time.time()

        for manga in response["data"]:
            manga_set[manga["title"]] = manga

    random_manga_title = random.choice(list(manga_set.keys()))
    return random_manga_title

def random_animanga():
    # Initial prompts
    choice = inquirer.select(message="Select one: ", choices=["Anime", "Manga"]).execute()
    os.system("clear")
    genre = inquirer.select(message="Choose a genre: ", choices=[item for item in masterdict]).execute()

    genre_id = masterdict[genre] # Selected genre is used as a parameter for our query

    time.sleep(1)
    os.system("clear")

    if choice == "Anime":
        print("Fetching anime...")
        anime = get_random_anime(genre_id)
        os.system("clear")

        print(
            f"You selected: \033[93m{genre}\033[0m.\nYour random anime is \033[91m{anime}\033[0m."  # Colored output
        )

        time.sleep(1)

        prompt = inquirer.select(
            message="Want to watch it? (Requires ani-cli)",
            choices=["Yes", "No"],
        ).execute()

        if prompt == "Yes":
            subprocess.run(["ani-cli", anime])
    else:
        print("Fetching manga...")
        manga = get_random_manga(genre_id)
        os.system("clear")

        print(
            f"You selected: \033[93m{genre}\033[0m.\nYour random manga is \033[91m{manga}\033[0m."  # Colored output
        )

        time.sleep(1)

        prompt = inquirer.select(
            message="Want to read it on Mangadex?",
            choices=["Yes", "No"],
        ).execute()

        if prompt == "Yes":
            pyperclip.copy(f"https://mangadex.org/search?q={manga}")
            print("\033[93mLink copied to your clipboard!\033[0m")

random_animanga()

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
manga_set = anime_set

def get_random_animanga(media_type, genre_id):
    # Rate limits for the API
    requests_per_second = 2
    start_time = time.time()
    media_set = {}

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
            search_type=media_type, query="", page=i + 1, parameters={"genres": genre_id}
        )

        start_time = time.time()

        for media in response["data"]:
            media_set[media["title"]] = media

    random_media_title = random.choice(list(media_set.keys()))
    return random_media_title # return the random anime so we can use it down in the main func
    

def random_animanga():
    # Initial prompts
    choice = inquirer.select(message="Select one: ", choices=["Anime", "Manga"]).execute()
    os.system("clear")
    genre = inquirer.select(message="Choose a genre: ", choices=[item for item in masterdict]).execute()

    genre_id = masterdict[genre] # Selected genre is used as a parameter for our query

    time.sleep(1)
    os.system("clear")

    if choice == "Anime":
        media_type = "anime"
        print("Fetching anime...")
    else:
        media_type = "manga"
        print("Fetching manga...")
    
    media = get_random_animanga(media_type, genre_id)
    os.system("clear")

    print(
        f"You selected: \033[93m{genre}\033[0m.\nYour random {media_type} is \033[91m{media}\033[0m."  # Colored output
    )

    time.sleep(1)

    if choice == "Anime":
        prompt = inquirer.select(
            message="Want to watch it? (Requires ani-cli)",
            choices=["Yes", "No"],
        ).execute()

        if prompt == "Yes":
            subprocess.run(["ani-cli", media])
    else:
        prompt = inquirer.select(
            message="Want to read it on Mangadex?",
            choices=["Yes", "No"],
        ).execute()

        if prompt == "Yes":
            pyperclip.copy(f"https://mangadex.org/search?q={media}")
            print("\033[93mLink copied to your clipboard!\033[0m")

random_animanga()

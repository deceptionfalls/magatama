import time
import subprocess
import os
import random
from InquirerPy import inquirer
from jikanpy import Jikan

api = Jikan()

# Genre IDs from Jikan
SHOUNEN_ID = 27
SEINEN_ID = 42
COMEDY_ID = 4
HORROR_ID = 14
SPORTS_ID = 30
DRAMA_ID = 8
ROMANCE_ID = 22
FANTASY_ID = 10
SCI_FI_ID = 24
MECHA_ID = 18

# Master dictionary, this is so we can have our selected genre's
# name appear in InquirerPy when we use it later down in the prompts
masterdict = {
    "Shounen": SHOUNEN_ID,
    "Fantasy": FANTASY_ID,
    "Drama": DRAMA_ID,
    "Sci-fi": SCI_FI_ID,
    "Romance": ROMANCE_ID,
    "Comedy": COMEDY_ID,
    "Seinen": SEINEN_ID,
    "Horror": HORROR_ID,
    "Sports": SPORTS_ID,
    "Mecha": MECHA_ID,
}

anime_set: dict[str, dict] = dict()


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
    return random_anime_title  # return the random anime so we can use it down in the main func


def random_anime():
    # Initial prompt
    genre = inquirer.select(
        message="Choose a genre: ",
        choices=[item for item in masterdict],
    ).execute()

    # Selected genre is used as a parameter for our query
    genre_id = masterdict[genre]

    time.sleep(1)
    os.system("clear")
    print("Fetching anime...")

    anime = get_random_anime(genre_id)

    os.system("clear")
    print(
        f"You selected: \033[93m{genre}\033[0m. Your random anime is \033[91m{anime}\033[0m."  # Colored output
    )

    time.sleep(1)

    prompt = inquirer.select(
        message="Want to watch it? (Requires ani-cli)",
        choices=["Yes", "No"],
    ).execute()

    if prompt == "Yes":
        subprocess.run(["ani-cli", anime])


random_anime()

# Magatama
A python CLI utility that can give you a random anime or manga from a selected genre, you can then watch the fetched anime straight from the terminal using `ani-cli`. Made using InquirerPy and the Jikan API to pull data from MyAnimeList.

## Demo
https://github.com/tsukki9696/magatama/assets/127806743/98ab56cd-4fcb-44ce-a12d-79697402e6c7

## Dependencies
- Python 3.x 
- [InquirerPy](https://github.com/kazhala/InquirerPy) 0.3.3
- [JikanPy](https://github.com/abhinavk99/jikanpy) 1.0.0
- [clipboard](https://pypi.org/project/clipboard/) 0.0.4
- [ani-cli](https://github.com/pystardust/ani-cli) 4.6 (optional)

## Installation
Clone this repository, then download the dependencies.
```
git clone https://github.com/tsukki9696/magatama.git
cd magatama/
pip install -r requirements.txt
```

**TODO**: Package script to PyPI and the AUR.

## Usage
```
python magatama.py
```

Move up and down genres with the arrow keys, confirm with Enter/Return.

## Limitations
Currently, the script is quite slow, and since the API requests from Jikan are fairly limited, I can only do so much optimisation, but improving the fetching speed is in my plans.

## Credits
- JikanPy wrapper and the Jikan API maintainers
- InquirerPy maintainers
- ani-cli maintainers
- [Where I got this whole idea from](https://www.youtube.com/watch?v=_xf1TMs0ysk&t=194s&pp=ygUdcHl0aG9uIHByb2plY3RzIGZvciBiZWdpbm5lcnM%3D)

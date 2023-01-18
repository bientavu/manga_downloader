import os

from dotenv import load_dotenv

load_dotenv()

INPUTS = {
    "overgeared": [
        "https://mangas-origines.fr/manga/overgeared-remake/chapitre-",
        "wp-manga-chapter-img",
        "manga_origines_fr"
    ],
    "the-player-that-cant-level-up": [
        "https://reaperscans.fr/serie/the-player-who-can-t-level-up/chapitre-",
        "wp-manga-chapter-img",
        "reaperscans_fr"
    ],
    "second-life-ranker": [
        "https://www.pantheon-scan.fr/second-life-ranker-",
        "wp-image",
        "pantheon_scan_fr"
    ],
    "black-haze": [
        "https://www.mangascantrad.fr/manga/black-haze/chapitre-",
        "wp-manga-chapter-img",
        "mangascantrad_fr"
    ],
    "a-returners-magic-should-be-special": [
        "https://www.pantheon-scan.fr/a-returners-magic-should-be-special-chapitre-",
        "wp-image",
        "pantheon_scan_fr"
    ],
    "the-beginning-after-the-end": [
        "https://www.pantheon-scan.fr/the-beginning-after-the-end-chapitre-",
        "wp-image",
        "pantheon_scan_fr"
    ],
    "tower-of-god": [
        "https://mangas-origines.fr/manga/tower-of-gods/",
        "wp-manga-chapter-img",
        "manga_origines_fr"
    ],
    "nano-machine": [
        "https://mangas-origines.fr/manga/1-nano-machine/chapitre-",
        "wp-manga-chapter-img",
        "manga_origines_fr"
    ],
    "tomb-raider-king": [
        "https://mangas-origines.fr/manga/12-tomb-raider-king/chapitre-",
        "wp-manga-chapter-img",
        "manga_origines_fr"
    ],
    "lecteur-omniscient": [
        "https://mangas-origines.fr/manga/lecteur-omniscient/chapitre-",
        "wp-manga-chapter-img",
        "manga_origines_fr"
    ],
    "lexpert-de-la-tour-tutoriel": [
        "https://mangas-origines.fr/manga/lexpert-de-la-tour-tutoriel/chapitre-",
        "wp-manga-chapter-img",
        "manga_origines_fr"
    ]
}


# VARIABLES
SELECT_MANGA = "the-player-that-cant-level-up"
CHAPTER_FROM = 1
CHAPTER_TO = 2
SEASON_NUMBER = 1
EPISODE_FROM = 32
EPISODE_TO = 32
CLASS_SRC_NAME = "src"

# Needs to be changed in .env
WORKING_DIR = os.getenv('WORKING_DIR')
OUTPUT_CBZ_DIR = os.getenv('OUTPUT_CBZ_DIR') + SELECT_MANGA + "/"
EXTENSION_DIR = os.getenv('EXTENSION_DIR')
WEBDRIVER_DIR = os.getenv('WEBDRIVER_DIR')

# CONSTANTS
URL = INPUTS[SELECT_MANGA][0]
CHAPTER_NUMBERS = list(range(CHAPTER_FROM, CHAPTER_TO + 1))
EPISODE_NUMBERS = list(range(EPISODE_FROM, EPISODE_TO + 1))
EXTENSION_URL = "chrome-extension://lkngoeaeclaebmpkgapchgjdbaekacki/popup.html"

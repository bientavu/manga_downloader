import os

from dotenv import load_dotenv

load_dotenv()

INPUTS = {
    "overgeared": [
        "https://www.pantheon-scan.fr/overgeared-chapitre-",
        "alignnone",
        "no_selenium"
    ],
    "the-player-that-cant-level-up": [
        "https://reaperscans.fr/serie/the-player-that-can-t-level-up/chapitre-",
        "wp-manga-chapter-img",
        "selenium_flaresolverr"
    ],
    "second-life-ranker": [
        "https://www.pantheon-scan.fr/second-life-ranker-",
        "wp-image",
        "no_selenium"
    ],
    "black-haze": [
        "https://www.mangascantrad.fr/manga/black-haze/chapitre-",
        "wp-manga-chapter-img",
        "no_selenium"
    ],
    "a-returners-magic-should-be-special": [
        "https://www.pantheon-scan.fr/a-returners-magic-should-be-special-chapitre-",
        "wp-image",
        "no_selenium"
    ],
    "the-beginning-after-the-end": [
        "https://www.pantheon-scan.fr/the-beginning-after-the-end-chapitre-",
        "wp-image",
        "no_selenium"
    ],
    "tower-of-god": [
        "https://s-mangavf.cc/manga/tower-of-god-scan/",
        "img-responsive",
        "selenium_flaresolverr"
    ]
}

# VARIABLES
SELECT_MANGA = "tower-of-god"
CHAPTER_FROM = 1
CHAPTER_TO = 3
CLASS_SRC_NAME = "data-src"
# Needs to be changed in .env
WORKING_DIR = os.getenv('WORKING_DIR')
OUTPUT_CBZ_DIR = os.getenv('OUTPUT_CBZ_DIR') + SELECT_MANGA + "/"
EXTENSION_DIR = os.getenv('EXTENSION_DIR')
WEBDRIVER_DIR = os.getenv('WEBDRIVER_DIR')

# CONSTANTS
URL = INPUTS[SELECT_MANGA][0]
CHAPTER_NUMBERS = list(range(CHAPTER_FROM, CHAPTER_TO + 1))
EXTENSION_URL = "chrome-extension://lkngoeaeclaebmpkgapchgjdbaekacki/popup.html"

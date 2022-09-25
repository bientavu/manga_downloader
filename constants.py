INPUTS = {
    "overgeared": [
        "https://www.pantheon-scan.fr/overgeared-chapitre-",
        "alignnone",
        "No"
    ],
    "the-player-that-cant-level-up": [
        "https://reaperscans.fr/serie/the-player-that-can-t-level-up/chapitre-",
        "wp-manga-chapter-img",
        "Yes"
    ],
    "second-life-ranker": [
        "https://www.pantheon-scan.fr/second-life-ranker-chapitre-",
        "alignnone",
        "No"
    ],
}

SELECT_MANGA = "the-player-that-cant-level-up"
URL = INPUTS[SELECT_MANGA][0]
WORKING_DIR = "/Users/axel/Documents/perso/repos/manga_downloader/chapters/"
OUTPUT_CBZ_DIR = "/Users/axel/Documents/perso/repos/manga_downloader/chapters_cbz/"
CHAPTER_FROM = 15
CHAPTER_TO = 18
CHAPTER_NUMBERS = list(range(CHAPTER_FROM, CHAPTER_TO + 1))
CHAPTER_ZERO = False

import os
import json
from dotenv import load_dotenv

load_dotenv()

# VARIABLES
SELECT_MANGA = "the-player-that-cant-level-up"
CHAPTER_FROM = 10
CHAPTER_TO = 12
SEASON_NUMBER = 1
EPISODE_FROM = 32
EPISODE_TO = 32
CLASS_SRC_NAME = "src"

# Needs to be changed in .env
WORKING_DIR = os.getenv('WORKING_DIR')
OUTPUT_CBZ_DIR = os.getenv('OUTPUT_CBZ_DIR') + SELECT_MANGA + "/"
EXTENSION_PATH = os.getenv('EXTENSION_PATH')
WEBDRIVER_PATH = os.getenv('WEBDRIVER_PATH')

# CONSTANTS
INPUTS_JSON = open('inputs.json')
INPUTS = json.load(INPUTS_JSON)
URL = INPUTS[SELECT_MANGA][0]
CHAPTER_NUMBERS = list(range(CHAPTER_FROM, CHAPTER_TO + 1))
EPISODE_NUMBERS = list(range(EPISODE_FROM, EPISODE_TO + 1))
EXTENSION_URL = "chrome-extension://lkngoeaeclaebmpkgapchgjdbaekacki/popup.html"

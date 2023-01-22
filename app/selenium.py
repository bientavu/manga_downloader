import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup as BSHTML
from pyvirtualdisplay import Display

from variables_and_constants import WEBDRIVER_PATH


def retrieve_imgs_urls_with_selenium(url):
    display = Display(visible=0, size=(800, 800))
    display.start()

    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('start-maximized')
    options.add_argument('enable-automation')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument("--remote-debugging-port=9222")
    # options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    driver = uc.Chrome(chrome_options=options, executable_path=WEBDRIVER_PATH)
    driver.get(url)
    time.sleep(4)
    html = driver.page_source
    soup = BSHTML(html, 'html.parser')
    return soup.findAll('img')

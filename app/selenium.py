import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup as BSHTML


def retrieve_imgs_urls_with_selenium(url):
    chrome_options_uc = uc.ChromeOptions()
    driver = uc.Chrome(options=chrome_options_uc, use_subprocess=True)
    driver.get(url)
    time.sleep(4)
    html = driver.page_source
    soup = BSHTML(html, 'html.parser')
    return soup.findAll('img')

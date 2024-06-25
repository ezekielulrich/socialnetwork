from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pickle
import os.path as path
from random import uniform


class Bot:
    def setUp(self):
        options = webdriver.FirefoxOptions()
        # options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        options.add_argument('--start-fullscreen')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--incognito")
        options.add_argument('--disable-blink-features=AutomationControlled')

        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(20)
        self.times_restarted = 0

    def tear_down(self):
        self.driver.quit()

    def goto(self, url):
        try:
            self.driver.get(url)
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def login(self, username, password, tfa=True):
        self.goto("https://www.instagram.com/")

        if not path.isfile("./cookies.pkl"):
            self.goto("https://www.instagram.com/accounts/login/")
            time.sleep(uniform(3, 6))

            self.driver.find_element(By.NAME, "username").send_keys(username)
            password = self.driver.find_element(By.NAME, "password").send_keys(password)
            self.driver.find_element(By.XPATH, "//button[contains(.,'Log in')]").click()
            time.sleep(uniform(3, 6))

            if tfa:
                code = input("Please enter the 2FA code sent to your mobile device: ")
                self.driver.find_element(By.NAME, "verificationCode").send_keys(code)
                confirm = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Confirm')]"))
                )
                time.sleep(uniform(3, 6))
                confirm.click()

            self.driver.find_element(By.XPATH, "//button[contains(.,'Save info')]").click()
            time.sleep(uniform(3, 6))
            self.driver.find_element(By.XPATH, "//button[contains(.,'Not Now')]").click()

            pickle.dump(self.driver.get_cookies() , open("./cookies.pkl","wb"))
        else:
            cookies = pickle.load(open("./cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)


    def get_my_followers(self, username):
        self.goto(f"https://instagram.com/{username}/")

        followers = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//a[@href='/{username}/followers/']")
            )
        )
        time.sleep(uniform(3, 6))
        followers.click()

        my_followers = set()

        old_last = None
        while True:
            followers = self.driver.find_elements(
                By.XPATH, '//span[@class="_ap3a _aaco _aacw _aacx _aad7 _aade"]'
            )

            last = followers[-1]
            if last == old_last:
                break
            old_last = last
            last.location_once_scrolled_into_view

            for follower in followers:
                name = follower.text
                my_followers.add(name)
                print(name)

            ActionChains(self.driver).send_keys(Keys.CONTROL, Keys.END).perform()
            time.sleep(uniform(2, 4))

        return my_followers

    def get_followers(self, my_followers, start_profile, filename="relations.txt"):
        count = start_profile - 1

        for profile in my_followers[start_profile - 1 :]:
            print(f"{count} / {len(my_followers)}")

            try: 
                self.goto(f"https://instagram.com/{profile}/")
                time.sleep(uniform(3, 6))
                button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//a[@href='/{profile}/followers/']")
                    )
                )
                button.click()

                users = set()
                old_last = None
                while True:
                    followers = self.driver.find_elements(
                        By.XPATH, '//span[@class="_ap3a _aaco _aacw _aacx _aad7 _aade"]'
                    )

                    last = followers[-1]
                    if last == old_last:
                        break
                    old_last = last
                    last.location_once_scrolled_into_view

                    for follower in followers:
                        name = follower.text
                        if name in my_followers:
                            users.add((profile, name))
                            print(name)

                    ActionChains(self.driver).send_keys(Keys.CONTROL, Keys.END).perform()
                    time.sleep(uniform(2, 5))

                with open(filename, "a") as f:
                    for relation in users:
                        f.write(f"https://www.instagram.com/{relation[0]}/ https://www.instagram.com/{relation[1]}/\n")
                
                print(f"{profile} follows {len(users)} of your connections")

            except Exception as ex: 
                print(f"Error, skipping: {ex}")
                pass


            with open(
                "start_profile.txt", "w+"
            ) as f:
                f.write(str(count))
                count += 1
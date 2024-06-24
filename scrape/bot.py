from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class Bot:
    def setUp(self):
        options = webdriver.FirefoxOptions()
        # options.add_argument("--headless")

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

        self.goto("https://www.instagram.com/accounts/login/")

        self.driver.find_element(By.NAME, "username").send_keys(username)
        password = self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[contains(.,'Log in')]").click()
        time.sleep(3)

        if tfa:
            code = input("Please enter the 2FA code sent to your mobile device: ")
            self.driver.find_element(By.NAME, "verificationCode").send_keys(code)
            confirm = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Confirm')]"))
            )
            confirm.click()

        saveinfo = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save info')]"))
        )
        saveinfo.click()
        self.driver.find_element(By.XPATH, "//button[contains(.,'Not Now')]").click()

    def get_my_followers(self, username):
        self.goto(f"https://instagram.com/{username}/")

        followers = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//a[@href='/{username}/followers/']")
            )
        )
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
            time.sleep(1)

        return my_followers

    def get_followers(self, my_followers, start_profile, filename="relations.txt"):
        count = start_profile - 1

        for profile in my_followers[start_profile - 1 :]:
            print(f"{count} / {len(my_followers)}")

            try: 
                self.goto(f"https://instagram.com/{profile}/")
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
                    time.sleep(2)

                with open(filename, "a") as f:
                    for relation in users:
                        f.write(f"https://www.instagram.com/{relation[0]}/ https://www.instagram.com/{relation[1]}/\n")

            except Exception as ex: 
                print(f"Error, skipping: {ex}")
                pass

            print(f"{profile} follows {len(users)} of your connections")

            with open(
                "start_profile.txt", "w+"
            ) as f:  # keep track of last profile checked
                f.write(str(count))
                count += 1

        """
        n_my_followers = len(followers)
        count_my_followers = start_profile - 1

        for current_profile in followers[start_profile - 1 : -1] + [
            followers[-1]
        ]:

            with open(
                "start_profile.txt", "w+"
            ) as outfile:  # keep track of last profile checked
                outfile.write(str(count_my_followers))

            followers = self.driver.find_elements(By.CLASS_NAME, "-nal3")
            followers[2].click()
            time.sleep(2)
            initialise_vars = 'elem = document.getElementsByClassName("isgrP")[0]; followers = parseInt(document.getElementsByClassName("g47SY")[1].innerText); times = parseInt(followers * 0.14); followersInView1 = document.getElementsByClassName("FPmhX").length'
            initial_scroll = "elem.scrollTop += 500"
            next_scroll = "elem.scrollTop += 2000"

            with open("./jquery-3.3.1.min.js", "r") as jquery_js:
                # 3) Read the jquery from a file
                jquery = jquery_js.read()
                # 4) Load jquery lib
                self.driver.execute_script(jquery)
                # scroll down the page
                self.driver.execute_script(initialise_vars)
                # self.driver.execute_script(scroll_followers)
                self.driver.execute_script(initial_scroll)
                time.sleep(random.randint(2, 5))

                next = True
                follow_set = set()
                # check how many people this person follows
                nr_following = int(
                    re.sub(
                        ",",
                        "",
                        self.driver.find_elements(By.CLASS_NAME, "g47SY")[2].text,
                    )
                )

                n_li = 1
                while next:
                    print(
                        str(count_my_followers)
                        + "/"
                        + str(n_my_followers)
                        + " "
                        + str(n_li)
                        + "/"
                        + str(nr_following)
                    )
                    time.sleep(random.randint(7, 12) / 10.0)
                    self.driver.execute_script(next_scroll)
                    time.sleep(random.randint(7, 12) / 10.0)
                    if not (n_li < nr_following - 11):
                        next = False

                    n_li = len(self.driver.find_elements(By.CLASS_NAME, "FPmhX"))
                    last_5_following.appendleft(n_li)
                    last_5_following.pop()
                    # if instagram starts blocking requests, reload page and start again
                    if len(set(last_5_following)) == 1:
                        print(
                            "Instagram seems to keep on loading. Refreshing page in 7 seconds"
                        )
                        self.times_restarted += 1
                        if self.times_restarted == 4:
                            print(
                                "Instagram is blocking your request. Terminating program. Start it again later."
                            )
                            sys.exit()
                        time.sleep(7)
                        self.get_followers(
                            followers, count_my_followers, relations_file
                        )

                self.times_restarted = 0

                following = self.driver.find_elements(By.CLASS_NAME, "FPmhX")
                for follow in following:
                    profile = follow.get_attribute("href")
                    if profile in followers:
                        follow_set.add((current_profile, profile))


        sys.exit()
        """

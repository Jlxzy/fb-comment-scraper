import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

DECLINE_COOKIES_XPATH = "//div[@aria-label='Decline optional cookies']"
MOST_RELEVANT_XPATH = "//div[@role='button'][.//*[contains(text(),'Most relevant')]]"
ALL_COMMENTS_XPATH = "//div[@role='menuitem'][.//*[contains(text(),'All comments')]]"
# WARNING: css selector may change due to fb obfuscation, may need updating
SCROLLABLE_CONTAINER_XPATH = "div.xb57i2i.x1q594ok.x5lxg6s.x78zum5.xdt5ytf.x6ikm8r.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.xx8ngbg.xwo3gff.x1n2onr6.x1oyok0e.x1odjw0f.x1iyjqo2.xy5w88m"

class FbCommentScraper:
    def __init__(self, email: str, password: str, post_url: str):
        self.email = email
        self.password = password
        self.post_url = post_url

        # init webdriver
        options = Options()
        options.set_preference("dom.webdriver.enabled", False)  # Disable webdriver flag
        options.set_preference("general.platform.override", "Win32")  # Spoof OS if needed

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)

        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def scrape(self):
        """
        Logs in to facebook and scrapes comments from given post
        """
        self.login()
        self.html = self.get_html()
        self.driver.quit()

        self.comments = self.parse_comments()

    def dismiss_cookies(self):
        """
        Dismisses cookie popup
        """
        try:
            cookie_elem = self.driver.find_element(By.XPATH, DECLINE_COOKIES_XPATH)
            cookie_elem.click()
        except NoSuchElementException:
            pass

    def login(self):
        """
        Logs in to Facebook using the selenium webdriver and personal credentials
        """
        self.driver.get("https://www.facebook.com/")

        self.dismiss_cookies()

        email_elem = self.driver.find_element(By.ID, "email")
        email_elem.send_keys(self.email)

        password_elem = self.driver.find_element(By.ID, "pass")
        password_elem.send_keys(self.password)

        password_elem.send_keys(Keys.RETURN)

        print("Pausing for manual captcha if necessary...")

        usr_input = ''

        while(usr_input != 'y' and usr_input != 'Y'):
            print("Enter (y) to continue: ", end="")
            usr_input = input()

        print("Logged in")

    def get_html(self) -> str:
        """
        Gets the html source for the given post's page

        :return: HTML source of the post's page
        :rtype: str
        """
        self.driver.get(self.post_url)
        print("Opened post page")

        self.dismiss_cookies()

        filter_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, MOST_RELEVANT_XPATH))
        )
        filter_button.click()

        all_comments_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, ALL_COMMENTS_XPATH))
        )
        all_comments_option.click()
        time.sleep(2)

        container = self.driver.find_element(By.CSS_SELECTOR, SCROLLABLE_CONTAINER_XPATH)

        # get initial scroll height
        last_height = self.driver.execute_script("return arguments[0].scrollHeight", container)

        print("Scrolling...", end="")

        # simulates scrolling whilst there are more comments to be loaded
        while True:
            # scroll to the bottom of the page
            print(".", end="")
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", container)
            time.sleep(2.5)

            new_height = self.driver.execute_script("return arguments[0].scrollHeight", container)

            # if scroll height hasn't changed, no more comments so exit loop
            if new_height == last_height:
                time.sleep(10)
                self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", container)
                time.sleep(2.5)

                new_height = self.driver.execute_script("return arguments[0].scrollHeight", container)

                if new_height == last_height:
                    break
            last_height = new_height

        print("\nFinished scrolling")

        return self.driver.page_source

    def parse_comments(self) -> list[tuple[str, str, str]]:
        """
        Parses the post comments from the loaded page's html

        :return: List of parsed comments, stored as tuples of name, comment, and comment url
        :rtype: list[tuple[str, str, str]]
        """
        page = BeautifulSoup(self.html, 'html.parser')

        comment_divs = page.find_all("div", attrs={"aria-label": re.compile(r"^Comment by")})
        comments = []

        for div in comment_divs:
            aria_label = div.get("aria-label", "")

            match = re.match(r"^Comment by (.+?) (?:\d|a|·)", aria_label)
            if match:
                name = match.group(1)
            else:
                name = aria_label.replace("Comment by ", "").strip()

            text_tag = div.find("div", {"dir": "auto"})
            text = text_tag.get_text(strip=True) if text_tag else ""

            link_tag = div.find("a")
            link = link_tag['href']

            comments.append((name, text, link))

        print("\nComments parsed")

        return comments

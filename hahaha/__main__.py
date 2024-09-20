from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger


from orjson import loads

import time
import random


class hahaha:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()

        options.add_argument("lang=ko_KR")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def _mimic_human(self) -> None:
        sleep_time = random.randint(500, 5000) / 1000
        logger.info(f"Sleeping for {sleep_time} to mimic human behavior")
        time.sleep(sleep_time)

    def _check_login(self) -> None:
        while True:
            current_session = self.driver.get_cookie("sessionid")
            if current_session:
                session = current_session["value"]
                logger.debug(f"Got Session: {session}")
                break

    def main(self, url: str):
        self.driver.get("https://instagram.com")
        logger.info("로그인 ㄱㄱ")
        self._check_login()

        json_endpoint = f"view-source:{url}?__a=1&__d=dis"

        self._mimic_human()

        self.driver.get(json_endpoint)
        content = self.driver.find_element(By.CLASS_NAME, "line-content")

        parsed_json = loads(content.text)
        carousel_media = parsed_json["items"][0]["carousel_media"]

        for media in carousel_media:
            candidate = media["image_versions2"]["candidates"]
            largest_image = max(candidate, key=lambda x: x["width"])
            print(largest_image["url"])

        time.sleep(15)


if __name__ == "__main__":
    instance = hahaha()
    instance.main("https://www.instagram.com/p/C_-tr4YSjeH/")

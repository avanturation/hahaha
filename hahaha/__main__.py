import argparse
import os
import random
import time

import chromedriver_autoinstaller
import httpx
from loguru import logger
from orjson import loads
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm


class hahaha:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()

        options.add_argument("lang=ko_KR")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )

        chromedriver_autoinstaller.install()

        self.driver = webdriver.Chrome(options=options)

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

    def _download_image(
        self, url: str, prefix: str = "", folder_name="default"
    ) -> None:
        if not os.path.exists(f"./{folder_name}"):
            os.makedirs(folder_name)

        filename = f"{folder_name}/{prefix}{url.split('/')[-1].split('?')[0]}"
        with open(filename, "wb") as fp:
            with httpx.stream("GET", url) as resp:
                total_bytes = int(resp.headers["Content-Length"])

                with tqdm(
                    total=total_bytes,
                    unit_scale=True,
                    unit_divisor=1024,
                    unit="B",
                    desc=filename,
                ) as progress:
                    num_bytes_downloaded = resp.num_bytes_downloaded

                for chunk in resp.iter_bytes(1024):
                    fp.write(chunk)
                    progress.update(resp.num_bytes_downloaded - num_bytes_downloaded)
                    num_bytes_downloaded = resp.num_bytes_downloaded

    def _parse_data(self) -> dict:
        content = self.driver.find_element(By.CLASS_NAME, "line-content")
        parsed_json = loads(content.text)

        return parsed_json["items"][0]

    def main(self, url_array: list):
        self.driver.get("https://instagram.com")
        logger.info("Login to Proceed.")

        self._check_login()
        self._mimic_human()

        for url in url_array:
            self.driver.get(f"view-source:{url}?__a=1&__d=dis")
            self._mimic_human()

            content = self._parse_data()
            carousel_media = content["carousel_media"]
            username = content["user"]["username"]
            post_code = content["code"]

            for media in carousel_media:
                candidate = media["image_versions2"]["candidates"]
                largest_image = max(candidate, key=lambda x: x["width"])

                self._download_image(
                    largest_image["url"],
                    prefix=f"{username}_{post_code}_",
                    folder_name=post_code,
                )
                self._mimic_human()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "--url",
        dest="url",
        type=str,
        nargs="+",
        help="Instagram post URL to save",
        required=True,
    )

    url_array = argparser.parse_args().url

    instance = hahaha()
    instance.main(url_array)

""" Класс загрузки альбомов ВК """

import logging
import os
import re
import time

import requests
import yt_dlp  # type: ignore[import-untyped]
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL  # type: ignore[import-untyped]

DELAY_SECONDS = 3


class Downloader:
    """Класс загрузки альбомов"""

    def __init__(self, filename: str, html_class: str, prefix: str):
        self.filename = filename
        self.html_class = html_class
        self.prefix = prefix

    def download_album(
        self,
        url: str = "",
        mode: str = "link",
        seria_start_number: int = 0,
        filename: str = "",
    ) -> bool:
        """Скачивает альбом ВК

        Parameters
        ----------
        url: str:
            ссылка на альбом
        mode: str:
            режим работы программы "link"(по ссылке)/"file"(из html файла) \n
            по файлу имеет смысл скачивать, если слишком длинный
            скроллинг страницы.
        seria_start_number: int:
            номер файла, если необходимо скачать не с первого
        filename: str:
            имя файла html, если необходим
        Returns
        -------
        bool
            успех/ не успех
        """

        album_text = ""
        index_series = 0
        if filename is not None:
            self.filename = filename

        if mode == "link":
            res = requests.get(
                url,
                headers={
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/96.0.4664.45 Safari/537.36"
                },
                timeout=5,
            )
            if res.status_code == 200:
                album_text = res.text
            else:
                logging.error(
                    f"Ошибка загрузки альбома, {res.status_code} - {res.text}"
                )
                return False
        elif mode == "file":
            with open(filename, "r", encoding="utf-8") as text:
                album_text = text.read()
        soup = BeautifulSoup(album_text, "html.parser")
        links = soup.find_all("a", class_=re.compile(self.html_class))
        for link in links:
            # Если необходимо скачать не с первой серии
            if index_series < seria_start_number:
                index_series += 1
                continue
            url = self.prefix + link.get("href")
            self.download_file(url)
            time.sleep(DELAY_SECONDS)
        self.rename_mp4()
        return True

    @staticmethod
    def rename_mp4():
        """Переименование файлов после скачивания в mp4"""
        files = os.listdir(path=".")
        for file in files:
            os.rename(file, file.replace(".unknown_video", ".mp4"))
            logging.debug(f"Файл {file} переименован")

    @staticmethod
    def download_file(url: str) -> bool:
        """Скачивание файла по ссылке

        Parameters
        ----------
        url : str
            ссылка на файл
        """
        ydl_opts = {
            "format": "url240",
            "postprocessors": [
                {
                    "key": "FFmpegMetadata",
                }
            ],
        }
        with YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                logging.debug(f"Файл {url} успешно загружен")
                return True
            except yt_dlp.utils.DownloadError as e:
                logging.error(str(e))
                return False

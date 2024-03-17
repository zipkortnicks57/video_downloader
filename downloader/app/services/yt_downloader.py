""" Класс загрузки видео из Youtube """

from downloader.app.services.downloader import Downloader


class YtDownloader(Downloader):
    """Класс загрузки видео из Youtube"""

    def __init__(self):
        super().__init__(
            filename="yt.html",
            html_class="yt-simple-endpoint style-scope ytd-video-renderer",
            prefix="https://youtube.com",
        )

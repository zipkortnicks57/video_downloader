""" Класс загрузки альбомов ВК """

from downloader.app.services.downloader import Downloader


class VkDownloader(Downloader):
    """Класс загрузки видео из VK"""

    def __init__(self):
        super().__init__(
            filename="source/vk.html",
            html_class="^VideoCardThumb",
            prefix="https://vk.com",
        )

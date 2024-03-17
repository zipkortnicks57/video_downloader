""" Описание интерфейса командной строки """

import click

from downloader.app.services.downloader import Downloader
from downloader.app.services.vk_downloader import VkDownloader
from downloader.app.services.yt_downloader import YtDownloader


@click.group()
def cli_group():
    """Cоздание группы команд"""
    pass  # pylint: disable=W0107


@cli_group.command()
@click.option("--url", help="адрес файла ВК для скачивания")
def download_file(url: str):
    """Скачивание файла ВК"""
    VkDownloader.download_file(url)


@cli_group.command()
@click.option("--url", help="адрес альбома ВК для скачивания")
@click.option(
    "--mode",
    default="link",
    help='режим работы программы \
              "link"(по ссылке)/"file"(из html файла)',
)
@click.option(
    "--seria_start_number",
    default=0,
    help="номер файла, \
              если необходимо скачать не с первого",
)
@click.option("--filename", default="source/vk.html", help="имя файла html")
@click.option("--source", default="vk", help="ресурс vk/youtube")
def download_album(
    url: str = "",
    mode: str = "link",
    seria_start_number: int = 0,
    filename: str = "source/vk.html",
    source: str = "vk",
):
    """Скачивание альбома ВК"""
    if source == "vk":
        dw: Downloader = VkDownloader()
    if source == "youtube":
        dw = YtDownloader()
    dw.download_album(url, mode, seria_start_number, filename)


cli = click.CommandCollection(sources=[cli_group])

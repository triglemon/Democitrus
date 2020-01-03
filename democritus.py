import discord
from aiohttp import ClientSession
from discord.ext import commands
from discord import Game
from bs4 import BeautifulSoup as Soup
from datetime import datetime


class Source:
    """
    _.-={ Source }=-._
    Represents a single source or outlet of articles and associated metadata for scraping

    == Attributes ==
        name: Name of the outlet
        category: Local/International/Culture
        url: Homepage
        surl: Scraping url
        title: Title tag
        link: Link tag
        date: Date tag
    """
    name: str
    category: str
    url: str
    surl: str
    title: str
    link: str
    date: str

    def __init__(self, name: str, category: str, url: str, surl: str, title: str, link: str, date: str) -> None:
        self.name = name
        self.category = category
        self.url = url
        self.surl = surl
        self.title = title
        self.link = link
        self.date = date

    def __str__(self):
        return self.name


class Feed:
    """
    _.-={ Feed }=-._
    Encompasses all functions related to news scraping and posting

    == Attributes ==

    """

    def __init__(self):
        pass

    def get_news(self, category):
        pass

    def post(self):
        pass

    def post_number(self):
        pass

    def post_category(self):
        pass


class Democritus(commands.Bot):
    """
    _.-={ democritus }=-._
    Helper bot for my own server's purposes.

    == Additional Attrs ==
        session: aiohttp client session for http requests
        feed: for handling functions related to news aggregation
    """
    session: ClientSession
    feed: Feed

    def __init__(self) -> None:
        super().__init__(command_prefix='$',
                         description='''Rob's Helper Bot.''',
                         activity=Game('waiting for Godot'))


bot = Democritus()
with open('token') as file:
    token = file.read()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)

bot.run(token)

import discord
import asyncio
from aiohttp import ClientSession
from discord.ext import commands
from discord import Game
from typing import Dict, List
from bs4 import BeautifulSoup as Soup
from datetime import datetime


async def fetch(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            response.raise_for_status()
        return await response.text()


class Source:
    """
    _.-={ Source }=-._
    Represents a single source or outlet of articles and associated metadata for scraping

    == Attributes ==
        name: Name of the outlet
        category: Local/International/Culture
        url: Homepage
        surl: Scraping url
        item: Item tag
        title: Title tag
        link: Link tag
        date: Date tag
    """
    name: str
    category: str
    url: str
    surl: str
    item: str
    title: str
    link: str
    date: str

    def __init__(self, name: str, category: str, url: str, surl: str, item: str, title: str, link: str, date: str) -> None:
        self.name = name
        self.category = category
        self.url = url
        self.surl = surl
        self.item = item
        self.title = title
        self.link = link
        self.date = date

    def __str__(self):
        return self.name


class Democitrus(commands.Bot):
    """
    _.-={ democritus }=-._
    Helper bot for my own server's purposes.

    == Additional Attrs ==
        session: aiohttp client session for http requests
        sources: all sources separated into groups based on type
        posts: list of all posts
    """
    session: ClientSession
    sources: Dict[str: List[Source]]

    def __init__(self) -> None:
        super().__init__(command_prefix='$',
                         description='''Rob's Helper Bot.''',
                         activity=Game('waiting for Godot'))
        self.session = ClientSession()

    def get_news(self, *c_list):
        s_list = []
        for category in c_list:
            s_list += self.sources[category]
        h_list = await asyncio.gather(*[[fetch(self.session, source.surl), source] for source in s_list])
        for html in h_list:
            source, doc = html[0], html[1]
            soup = Soup(doc)
            articles = soup.find_all(source.item)
                
    def get_all_news(self):
        self.get_news('local', 'international', 'books', 'culture')

    def post(self):
        pass

    def post_number(self):
        pass

    def post_category(self):
        pass


bot = Democitrus()
with open('token') as file:
    token = file.read()


@bot.event
async def on_ready():
    bot.sources['local'] = [Source('Toronto Star',
                                   'local',
                                   'www.thestar.ca',
                                   'http://www.thestar.com/content/thestar/feed.RSSManagerServlet.articles.news.rss',
                                   'item',
                                   'title',
                                   'link',
                                   'pubDate')]
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)

bot.run(token)

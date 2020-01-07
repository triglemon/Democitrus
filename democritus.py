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
    Represents a single source of articles and associated metadata for scraping

    == Attributes ==
        name: Name of the source
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


class Post:
    """
    _.-={ Post }=-._
    A class representing a single article as a message ready to be posted on discord.

    == Attributes ==

    """
    def __init__(self, title: str, link: str, date: str, name: str) -> None:
        self.embed = discord.Embed(title=title, url=link, description=date)
        self.embed.set_author(name=name)
        self.message = None

    async def post(self, ctx: commands.Context) -> None:
        self.message = await ctx.send(embed=self.embed)


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
    sources: Dict[str, List[Source]]
    posts: Dict[str, List[Post]]

    def __init__(self) -> None:
        super().__init__(command_prefix='$',
                         description="""Rob's Helper Bot.""",
                         activity=Game('waiting for Godot'))
        self.session = ClientSession()
        self.sources = {'local': [],
                        'international': [],
                        'books': [],
                        'culture': []}

    async def get_news(self, *c_list: str) -> None:
        s_list = []
        for category in c_list:
            s_list += self.sources[category]
        h_list = await asyncio.gather(*[[fetch(self.session, source.surl), source] for source in s_list])
        for html in h_list:
            source, doc = html[0], html[1]
            soup = Soup(doc)
            a_list = soup.find_all(source.item)
            for articles in a_list:
                title = articles[source.title]
                date = articles[source.date]
                link = articles[source.link]
                self.posts[source.category].append(Post(title, link, date, source.name))

    async def get_all_news(self) -> None:
        await self.get_news('local', 'international', 'books', 'culture')

    async def post(self, ctx: commands.Context, category: str) -> None:
        for post in self.posts[category]:
            await post.post(ctx)

    def post_number(self):
        pass

    def post_category(self):
        pass


bot = Democitrus()
with open('token') as file:
    token = file.read()


@bot.event
async def on_ready() -> None:
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
async def post(ctx, category: str) -> None:
    await bot.get_all_news()
    await bot.post(ctx, category)

bot.run(token)

import discord
from discord import Embed
from pydantic import BaseModel
import json
import re
import cloudscraper
from bs4 import BeautifulSoup
from settings import LINK_SCRAPER_GEMINI

scraper = cloudscraper.create_scraper()

def prettify_collection_payload(
    payload: dict[str, list[str]],
) -> (str, str):  # (title, description)
    """returns title and description in order to construct discord.Embed"""
    title = ""
    description = ""
    for key, value in payload.items():
        title = f"**{' '.join(word.capitalize() for word in key.split('_'))}**: \n"
        for element in value:
            description += f"* {element} \n"
    return title, description

def extract_tag_contents(url):
    response = scraper.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove script and style elements
    for unwanted in soup(['script', 'style']):
        unwanted.decompose()

    # Extract and clean text
    text = soup.get_text(separator="\n", strip=True)
    return text

async def scrape_link(msg: discord.Message):
    link_regex = r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)"

    link_collection = list(re.findall(link_regex, msg.content))
    if not link_collection:
        return

    collected_data: list[str] = []
    for link in link_collection:
        try:
            collected_data.append(extract_tag_contents(link))
        except Exception as e:
            return await msg.reply(
                embed=Embed(title=f"failed to fetch provided link, details: {e} ")
            )

    class BulletPoints(BaseModel):
        article_bullet_points: list[str]

    try:
        res = await LINK_SCRAPER_GEMINI.send_prompt(
            f""
            f"return as few bullet points as possible without sacrificing any important information. data:{str(collected_data)}",
            response_schema=BulletPoints,
        )
        parsed_data = json.loads(res)
        title, desc = prettify_collection_payload(parsed_data)
    except Exception as e:
        return await msg.reply(
            embed=Embed(title=f"failed to parse gemini response, details: {e} ")
        )

    return await msg.reply(embed=Embed(title=title, description=desc))

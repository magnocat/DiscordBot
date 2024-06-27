import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_kabum_promotions():
    url = 'https://www.kabum.com.br/hardware'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    promotions = []
    for product in soup.select('.productCard'):
        try:
            title = product.select_one('.productCard-name').get_text(strip=True)
            price = product.select_one('.priceCard-value').get_text(strip=True)
            link = product.select_one('a')['href']
            link = f"https://www.kabum.com.br{link}"
            promotions.append(f"{title} - {price}\n{link}")
        except AttributeError:
            continue
    return promotions

@bot.command(name='promocoes')
async def promocoes(ctx):
    await ctx.send("Buscando promoções...")
    promotions = get_kabum_promotions()
    if promotions:
        for promo in promotions:
            await ctx.send(promo)
    else:
        await ctx.send("Não foram encontradas promoções no momento.")

TOKEN = os.getenv('HEROKU_DISCORD')  # Carrega o token do ambiente
bot.run(TOKEN)

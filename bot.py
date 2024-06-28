import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timezone, timedelta
import subprocess
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configurar o fuso horário para o Horário de Brasília (BRT)
brt = timezone(timedelta(hours=-3))

# Lista de comandos disponíveis para o comando !ajuda
available_commands = {
    'promocoes': 'Busca promoções no site da Kabum.',
    'hora': 'Mostra a hora atual.',
    'data': 'Mostra a data completa atual.',
    'ativar_funcao': 'Ativa uma função específica no bot.',
    'desativar_funcao': 'Desativa uma função específica no bot.',
    'startmc': 'Inicia o servidor Minecraft.',
    'stopmc': 'Para o servidor Minecraft.',
    'statusmc': 'Verifica o status do servidor Minecraft.',
    'ajuda': 'Mostra a lista de comandos disponíveis.',
    'piada': 'Mostra uma piada aleatória.'
}

# Função para adicionar o aviso de ajuda em cada comando
async def send_help_message(ctx):
    help_message = "Digite `!ajuda` para ver todos os comandos disponíveis."
    await ctx.send(f"---\n{help_message}\n---")

def get_kabum_promotions():
    url = 'https://www.kabum.com.br/hardware'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 403:
        print("Access denied")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    promotions = []
    for product in soup.select('.productCard'):
        try:
            title = product.select_one('.nameCard').get_text(strip=True)
            price = product.select_one('.priceCard').get_text(strip=True)
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
    await send_help_message(ctx)

@bot.command(name='hora')
async def hora(ctx):
    now = datetime.now(tz=brt).strftime('%H:%M:%S')
    await ctx.send(f"A hora atual é {now} (Horário de Brasília).")
    await send_help_message(ctx)

@bot.command(name='data')
async def data(ctx):
    today = datetime.now(tz=brt).strftime('%d/%m/%Y %H:%M:%S')
    await ctx.send(f"A data completa atual é {today} (Horário de Brasília).")
    await send_help_message(ctx)

# Comando de ativar função (simulado)
@bot.command(name='ativar_funcao')
async def ativar_funcao(ctx, *, funcao: str):
    await ctx.send(f"A função `{funcao}` foi ativada.")
    await send_help_message(ctx)

# Comando de desativar função (simulado)
@bot.command(name='desativar_funcao')
async def desativar_funcao(ctx, *, funcao: str):
    await ctx.send(f"A função `{funcao}` foi desativada.")
    await send_help_message(ctx)

@bot.command(name='ajuda')
async def ajuda(ctx):
    help_text = "Aqui estão os comandos disponíveis:\n"
    for command, description in available_commands.items():
        help_text += f"`!{command}`: {description}\n"
    await ctx.send(help_text)

# Comando para iniciar o servidor Minecraft
@bot.command(name='startmc')
async def startmc(ctx):
    # Substitua pelo caminho do seu script ou comando para iniciar o servidor Minecraft
    result = subprocess.run(['./start_minecraft_server.sh'], capture_output=True, text=True)
    await ctx.send(f"Servidor Minecraft iniciado.\n{result.stdout}")
    await send_help_message(ctx)

# Comando para parar o servidor Minecraft
@bot.command(name='stopmc')
async def stopmc(ctx):
    # Substitua pelo caminho do seu script ou comando para parar o servidor Minecraft
    result = subprocess.run(['./stop_minecraft_server.sh'], capture_output=True, text=True)
    await ctx.send(f"Servidor Minecraft parado.\n{result.stdout}")
    await send_help_message(ctx)

# Comando para verificar o status do servidor Minecraft
@bot.command(name='statusmc')
async def statusmc(ctx):
    # Substitua pelo comando que verifica o status do servidor Minecraft
    result = subprocess.run(['./status_minecraft_server.sh'], capture_output=True, text=True)
    await ctx.send(f"Status do servidor Minecraft:\n{result.stdout}")
    await send_help_message(ctx)

# Comando para buscar piadas aleatórias em português
@bot.command(name='piada')
async def piada(ctx):
    joke_url = "https://us-central1-kivson.cloudfunctions.net/charadas-aleatorias"
    response = requests.get(joke_url)
    if response.status_code == 200:
        joke = response.json()
        await ctx.send(f"{joke['pergunta']} - {joke['resposta']}")
    else:
        await ctx.send("Não foi possível obter uma piada no momento.")
    await send_help_message(ctx)

# Mensagem de boas-vindas
@bot.event
async def on_member_join(member):
    welcome_messages = [
        f"Bem-vindo, {member.mention}! Esperamos que você se divirta aqui!",
        f"Olá, {member.mention}! Bem-vindo ao nosso servidor!",
        f"{member.mention} acabou de entrar no servidor. Dêem as boas-vindas!"
    ]
    channel = discord.utils.get(member.guild.text_channels, name="geral")
    if channel:
        await channel.send(random.choice(welcome_messages))

# Definir quem pode alterar e configurar o bot
@bot.command(name='set_admin')
@commands.has_permissions(administrator=True)
async def set_admin(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="BotAdmin")
    if not role:
        role = await ctx.guild.create_role(name="BotAdmin", permissions=discord.Permissions.all())
    await member.add_roles(role)
    await ctx.send(f"O usuário {member.mention} agora é um administrador do bot.")
    await send_help_message(ctx)

@bot.command(name='remove_admin')
@commands.has_permissions(administrator=True)
async def remove_admin(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="BotAdmin")
    if role:
        await member.remove_roles(role)
        await ctx.send(f"O usuário {member.mention} não é mais um administrador do bot.")
    await send_help_message(ctx)

TOKEN = os.getenv('HEROKU_DISCORD')

if TOKEN is None:
    raise ValueError("No token found. Please set the HEROKU_DISCORD environment variable.")

bot.run(TOKEN)

import discord
from discord.ext import commands
import os
from datetime import datetime, timezone, timedelta
from commands import setup_commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configurar o fuso horário para o Horário de Brasília (BRT)
brt = timezone(timedelta(hours=-3))

# Configurar comandos
setup_commands(bot)

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

# Chamar `!ajuda` automaticamente para comandos inexistentes
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.invoke(bot.get_command('ajuda'))
    else:
        print(f"Erro: {error}")

TOKEN = os.getenv('HEROKU_DISCORD')

if TOKEN is None:
    raise ValueError("No token found. Please set the HEROKU_DISCORD environment variable.")

bot.run(TOKEN)
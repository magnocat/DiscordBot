import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta
import subprocess
import random
from utils import get_kabum_promotions, kabum_teste

# Configurar o fuso horário para o Horário de Brasília (BRT)
brt = timezone(timedelta(hours=-3))

available_commands = {
    'promocoes': 'Busca promoções no site da Kabum.',
    'ativar_funcao': 'Ativa uma função específica no bot.',
    'desativar_funcao': 'Desativa uma função específica no bot.',
    'minecraft': 'Exibe comandos relacionados ao Minecraft.',
    'teste': 'Executa a função de teste para scraping da Kabum.',
    'ajuda': 'Mostra a lista de comandos disponíveis.'
}

# Função para adicionar o aviso de ajuda em cada comando
async def send_help_message(ctx):
    help_message = "Digite `!ajuda` para ver todos os comandos disponíveis."
    await ctx.send(f"---\n{help_message}\n---")

def setup_commands(bot):
    @bot.command(name='promocoes')
    async def promocoes(ctx):
        await ctx.send(f"Buscando promoções, {ctx.author.name}...")
        promotions = get_kabum_promotions()
        if promotions:
            for promo in promotions:
                await ctx.send(promo)
        else:
            await ctx.send(f"Não foram encontradas promoções no momento, {ctx.author.name}.")
        await send_help_message(ctx)

    @bot.command(name='ativar_funcao')
    async def ativar_funcao(ctx, *, funcao: str):
        await ctx.send(f"A função `{funcao}` foi ativada, {ctx.author.name}.")
        await send_help_message(ctx)

    @bot.command(name='desativar_funcao')
    async def desativar_funcao(ctx, *, funcao: str):
        await ctx.send(f"A função `{funcao}` foi desativada, {ctx.author.name}.")
        await send_help_message(ctx)

    @bot.command(name='ajuda')
    async def ajuda(ctx):
        help_text = "Aqui estão os comandos disponíveis:\n"
        for command, description in available_commands.items():
            help_text += f"`!{command}`: {description}\n"
        now = datetime.now(tz=brt).strftime('%d/%m/%Y %H:%M:%S')
        help_text += f"\nData e hora atuais: {now} (Horário de Brasília)"
        await ctx.send(help_text)

    @bot.command(name='set_admin')
    @commands.has_permissions(administrator=True)
    async def set_admin(ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="BotAdmin")
        if not role:
            role = await ctx.guild.create_role(name="BotAdmin", permissions=discord.Permissions.all())
        await member.add_roles(role)
        await ctx.send(f"O usuário {member.mention} agora é um administrador do bot, {ctx.author.name}.")
        await send_help_message(ctx)

    @bot.command(name='remove_admin')
    @commands.has_permissions(administrator=True)
    async def remove_admin(ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="BotAdmin")
        if role:
            await member.remove_roles(role)
            await ctx.send(f"O usuário {member.mention} não é mais um administrador do bot, {ctx.author.name}.")
        await send_help_message(ctx)

    @bot.command(name='minecraft')
    async def minecraft(ctx):
        minecraft_commands = {
            'startmc': 'Inicia o servidor Minecraft.',
            'stopmc': 'Para o servidor Minecraft.',
            'statusmc': 'Verifica o status do servidor Minecraft.'
        }
        help_text = "Comandos do Minecraft:\n"
        for command, description in minecraft_commands.items():
            help_text += f"`!{command}`: {description}\n"
        await ctx.send(help_text)

    @bot.command(name='startmc')
    async def startmc(ctx):
        result = subprocess.run(['./start_minecraft_server.sh'], capture_output=True, text=True)
        await ctx.send(f"Servidor Minecraft iniciado, {ctx.author.name}.\n{result.stdout}")
        await send_help_message(ctx)

    @bot.command(name='stopmc')
    async def stopmc(ctx):
        result = subprocess.run(['./stop_minecraft_server.sh'], capture_output=True, text=True)
        await ctx.send(f"Servidor Minecraft parado, {ctx.author.name}.\n{result.stdout}")
        await send_help_message(ctx)

    @bot.command(name='statusmc')
    async def statusmc(ctx):
        result = subprocess.run(['./status_minecraft_server.sh'], capture_output=True, text=True)
        await ctx.send(f"Status do servidor Minecraft, {ctx.author.name}:\n{result.stdout}")
        await send_help_message(ctx)

    @bot.command(name='teste')
    async def teste(ctx):
        await ctx.send(f"Iniciando teste de scraping, {ctx.author.name}...")
        kabum_teste()
        await ctx.send(f"Teste de scraping concluído, {ctx.author.name}. Confira o console do Replit para os resultados.")
        await send_help_message(ctx)
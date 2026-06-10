import os
import re
import sys
import datetime
import discord
from discord import app_commands
from dotenv import load_dotenv
import troxa

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class TresTroxaUtils(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

bot = TresTroxaUtils()

# detector de ANGELOS!!!!!
@bot.event
async def on_message(message: discord.Message):
    imunes = troxa.load_imunes()
    if message.author.bot or message.author.id in imunes:
        return

    # print("mensagem recebida!")
    content = message.content or ""
    padrao_angelo = re.compile(troxa.cria_regex_com_grupos("angelo"), re.IGNORECASE | re.DOTALL)

    try:
        match_angelo = padrao_angelo.search(content)
    except Exception:
        return

    if match_angelo:
        result = troxa.marca_angelo(content) or (content[:60] + ('...' if len(content) > 60 else ''))

        try:
            await message.reply(f'Pera aí... **ANGELO????**\n'
                                f'> {result} \n'
                                f'-# COMO OUSA citar o nome do mestre EM VÃO?! **Tá de castigo!**')
        except Exception as e:
            pass

        if message.guild:
            membro = message.author
            duracao_segundos = 60

            try:
                duracao = datetime.timedelta(seconds=duracao_segundos)
                await membro.timeout(duracao, reason="angelo")
            except Exception as e:
                pass

# Iniciando o bot real oficial
@bot.event
async def on_ready():
    print(f"Logado como: {bot.user}")
    try:
        await bot.tree.sync()
        print("DEU BOM!!!!")
    except Exception as e:
        print("Deu merda, erro: ", e)

def load_cogs():
    cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
    sys.path.insert(0, os.path.dirname(__file__))
    for fname in os.listdir(cogs_dir):
        if fname.endswith(".py") and fname != "__init__.py":
            mod_name = f"cogs.{fname[:-3]}"
            try:
                module = __import__(mod_name, fromlist=["*"])
                if hasattr(module, "setup"):
                    module.setup(bot)
                    print(f"Deu certo: {mod_name}")
            except Exception as e:
                print(f"Erro no {mod_name}: {e}")

if __name__ == "__main__":
    load_cogs()
    load_dotenv()
    TOKEN = os.environ['TOKEN']
    bot.run(TOKEN)
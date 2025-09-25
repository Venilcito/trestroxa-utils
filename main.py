import os
import sys
import discord
from discord import app_commands

intents = discord.Intents.default()
intents.members = True

class TresTroxaUtils(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

bot = TresTroxaUtils()

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
    TOKEN = os.environ['TOKEN']
    bot.run(TOKEN)
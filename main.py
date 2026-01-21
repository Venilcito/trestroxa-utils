import os
import re
import sys
import datetime
import discord
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class TresTroxaUtils(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

bot = TresTroxaUtils()

# detector de ANGELOS!!!!!
substituicoes = {
    'a': '[ᴀ4AâÂáÁàÀ🅰🅰️]',
    'n': '[NɴŋñÑ🅽]',
    'g': '[Gɢ🅶]',
    'e': '[E3ᴇéÉèÈêÊ🅴]',
    'l': '[ʟLI🅻]',
    'o': '[ᴏO0ôÔõÕóÓòÒº🅾⭕0️⃣]'
}

def cria_regex_com_grupos(palavra: str) -> str:
    regex = ''
    for letra in palavra.lower():
        grupo = substituicoes.get(letra, re.escape(letra))
        regex += '(' + grupo + ')'
        regex += '.*?'
    return regex

padrao_angelo = re.compile(cria_regex_com_grupos("angelo"), re.IGNORECASE)

def marca_angelo(texto: str) -> str | None:
    regex = ''
    for letra in 'angelo':
        regex += '(' + substituicoes[letra] + ')'
        regex += '.*?'
    padrao = re.compile(regex, re.IGNORECASE)

    match = padrao.search(texto)
    if not match:
        return None

    last_index = 0
    grupos = list(match.groups())

    resultado = '"'
    for grupo in grupos:
        busca = grupo.lower()
        idx = texto.lower().find(busca, last_index)

        if idx == -1:
            idx = last_index

        resultado += texto[last_index:idx]

        if 0 <= idx < len(texto):
            resultado += f' **{texto[idx].upper()}** '
            last_index = idx + 1
        else:
            last_index = idx

    rest = texto[last_index:last_index + 30]
    if last_index + 30 < len(texto):
        resultado += f'{rest}..."'
    else:
        resultado += f'{rest}"'
    return resultado

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # print("mensagem recebida!")
    content = message.content or ""

    try:
        match_angelo = padrao_angelo.search(content)
    except Exception:
        return

    if match_angelo:
        result = marca_angelo(content) or (content[:60] + ('...' if len(content) > 60 else ''))

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
    TOKEN = os.environ['TOKEN']
    bot.run(TOKEN)
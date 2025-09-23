import discord
from discord import app_commands
import os
from typing import Optional
import nest_asyncio
import asyncio

# --- Configurações Iniciais ---
intents = discord.Intents.default()
intents.members = True  # necessário pra acessar membros
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# --- Evento: Bot Pronto (VERSÃO DE DIAGNÓSTICO) ---
@client.event
async def on_ready():
    print("==============================================")
    print("O evento 'on_ready' foi ativado!")
    print(f"Logado como: {client.user} (ID: {client.user.id})")

    try:
        await tree.sync()
        print("SUCESSO: Comandos sincronizados.")
        print("Verifique a aba 'Integrações' no Discord AGORA.")
    except Exception as e:
        print("!!!!!!!!!! FALHA NA SINCRONIZAÇÃO !!!!!!!!!!")
        print(f"Ocorreu um erro: {e}")

    print("==============================================")


# --- Mapeamento de letras para emojis ---
mapa_emojis = {
    "a": "🅰", "b": "🅱", "c": "🅲", "d": "🅳", "e": "🅴", "f": "🅵",
    "g": "🅶", "h": "🅷", "i": "🅸", "j": "🅹", "k": "🅺", "l": "🅻",
    "m": "🅼", "n": "🅽", "o": "🅾", "p": "🅿", "q": "🆀", "r": "🆁",
    "s": "🆂", "t": "🆃", "u": "🆄", "v": "🆅", "w": "🆆", "x": "🆇",
    "y": "🆈", "z": "🆉"
}

# --- Definição do Comando ---
@tree.command(name="nome", description="Muda seu nome de acordo com as normas da firma")
async def comando_nome(
    interaction: discord.Interaction,
    nome: str,
    pessoa: Optional[discord.Member] = None
):
    # Normaliza o texto
    apelido_normalizado = "".join(
        [c.lower() for c in nome if c.isalpha()]
    )

    # Checa tamanho
    if len(apelido_normalizado) == 0:
        await interaction.response.send_message(
            "⁉️ Ok, e o nome?",
            ephemeral=True
        )
        return
    if len(apelido_normalizado) > 8:
        await interaction.response.send_message(
            "❌ Calma aí patrão, o nome não pode ter mais de 8 letras!",
            ephemeral=True
        )
        return

    # Converte para emojis
    apelido_emojis = "".join(mapa_emojis.get(c, "") for c in apelido_normalizado)

    # Decide quem vai ter o apelido alterado
    membro = interaction.user
    if pessoa:
        # se tentou passar alguém, checa se é admin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Calma aí patrão, você só pode mudar seu próprio nome!",
                ephemeral=True
            )
            return
        membro = pessoa

    # Tenta aplicar
    try:
        await membro.edit(nick=apelido_emojis)
        if membro == interaction.user:
            msg = f"✅ Nome mudado: `{apelido_emojis}`"
        else:
            msg = f"✅ Nome de {membro.mention} mudado: `{apelido_emojis}`"

        await interaction.response.send_message(msg, ephemeral=True)

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Esse cara é especial demais! Não posso mudar o nome dele",
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"⚠️ Fi, deu bosta aqui: {e}",
            ephemeral=True
        )

@tree.command(name="angelo", description="Permite que você cite o nome do mestre")
@app_commands.describe(texto="Coloque '...' pra poder falar 'angelo'")
async def comando_angelo(interaction: discord.Interaction, texto: Optional[str]):
    texto = texto or ""

    if "..." in texto:
        texto = texto.replace("...", "angelo")

    resposta = texto.strip() or "angelo"
    await interaction.response.send_message(resposta)

# --- Inicia o Bot ---
TOKEN = os.environ['TOKEN']

nest_asyncio.apply()
async def main():
    await client.run(TOKEN)

asyncio.run(main())
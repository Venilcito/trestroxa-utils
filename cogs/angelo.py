from typing import Optional
import discord
from discord import app_commands

def setup(bot):
    @bot.tree.command(name="angelo", description="Permite que você cite o nome do mestre")
    @app_commands.describe(texto="Escreva '...' e eu troco pra 'angelo'")
    async def comando_angelo(interaction: discord.Interaction, texto: Optional[str] = None):
        # print(f"/angelo acionado por {interaction.user}")

        texto = texto or ""

        if "..." in texto:
            texto = texto.replace("...", "angelo")

        resposta = texto.strip() or "angelo"
        await interaction.response.send_message(resposta)
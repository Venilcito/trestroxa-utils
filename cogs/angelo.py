from typing import Optional
import discord
from discord import app_commands
import datetime
from database import load_imunes

def setup(bot):
    @bot.tree.command(name="angelo", description="Permite que você cite o nome do mestre")
    @app_commands.describe(texto="Escreva angelo a vontade")
    async def comando_angelo(interaction: discord.Interaction, texto: Optional[str] = None):
        # print(f"/angelo acionado por {interaction.user}")

        texto = texto or ""
        texto_strip = texto.strip()


        resposta = texto_strip or "angelo"
        angelos = texto.lower().count("angelo")

        if texto_strip == "":
            minutos = 1
        else:
            minutos = angelos
        
        membro = interaction.user
        imunes = load_imunes()
        
        try:
            if minutos > 0 and membro.id not in imunes:
                duracao = datetime.timedelta(minutes=minutos)
                await membro.timeout(duracao, reason="angelo")
            
            await interaction.response.send_message(resposta)
        
        except Exception as e:
            await interaction.response.send_message(f"fi deu merda: {e}", ephemeral=True)
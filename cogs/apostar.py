import discord
from discord import app_commands
import datetime
import random

def setup(bot):
    vicio = {}

    @bot.tree.command(name="apostar", description="A casa sempre ganha")
    @app_commands.describe(minutos="Minutos pra apostar")
    async def comando_aposta(interaction: discord.Interaction, minutos: int):
        # print(f"/aposta acionado por {interaction.user}")

        agora = datetime.datetime.now(datetime.timezone.utc)
        iduser = interaction.user.id

        if iduser not in vicio:
            vicio[iduser] = []

        vicio[iduser] = [
            t for t in vicio[iduser]
            if (agora - t).total_seconds() < 60
        ]

        vicio[iduser].append(agora)

        if len(vicio[iduser]) >= 10:
            duracao = datetime.timedelta(days=1)
            await interaction.user.timeout(duracao, reason= "Consumido pelo vício em apostas")
            vicio[iduser].clear()
    
            await interaction.response.send_message(f"⛔ {interaction.user.mention} foi diagnosticado com **vício em apostas...**\n"
                                                    f"*Está em estado de recuperação por **1 dia**. Melhoras!*")
            return


        if random.randint(1, 100) < 20:
            await interaction.response.send_message(f"🎉 {interaction.user.mention} acabou de ficar {minutos} minutos de castigo! 🎊")
            duracao = datetime.timedelta(minutes=minutos)
            await interaction.user.timeout(duracao, reason="Tentou a sorte")

        else:
            await interaction.response.send_message(f"Dessa vez você se safou...")
import discord
from discord import app_commands
import datetime
import random

def setup(bot):
    vicio = {}

    @bot.tree.command(name="apostar", description="A casa sempre ganha")
    @app_commands.describe(minutos="Minutos pra apostar")
    async def comando_aposta(interaction: discord.Interaction, minutos: int):
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
    
            await interaction.response.send_message(
                f"⛔ {interaction.user.mention} foi diagnosticado com **vício em apostas...**\n"
                f"*Está em estado de recuperação por **1 dia**. Melhoras!*"
            )
            return

        if random.randint(1, 100) < 20:
            MAX_MINUTOS = (28 * 24 * 60) - 5
            minutos_reais = min(minutos, MAX_MINUTOS)
            
            if minutos_reais >= 1440:
                dias = minutos_reais // 1440
                resto_minutos = minutos_reais % 1440
                horas = resto_minutos // 60
                mins = resto_minutos % 60
                
                tempo_str = f"**{dias} dia(s)**"
                if horas > 0: tempo_str += f", **{horas} hora(s)**"
                if mins > 0: tempo_str += f" e **{mins} minuto(s)**"
                
            elif minutos_reais >= 60:
                horas = minutos_reais // 60
                mins = minutos_reais % 60
                tempo_str = f"**{horas} hora(s)**"
                if mins > 0: tempo_str += f" e **{mins} minuto(s)**"
                
            elif minutos > 0:
                tempo_str = f"**{minutos_reais} minuto(s)**"

            else:
                tempo_str = MAX_MINUTOS

            aviso_extra = ""
            if minutos > MAX_MINUTOS or minutos <= 0:
                aviso_extra = f"\n\n-# {minutos} minutos? Bonitinho"

            msg = f"🎉 {interaction.user.mention} acabou de ficar {tempo_str} de castigo! 🎊{aviso_extra}"
            
            duracao = datetime.timedelta(minutes=minutos_reais)
            await interaction.user.timeout(duracao, reason="Tentou a sorte")

        else:
            msg = f"Dessa vez você se safou..."

        await interaction.response.send_message(msg)
from typing import Optional
import discord
from discord import app_commands
import datetime

def setup(bot):
    votacoes = {}
    abusos = set()

    @bot.tree.command(name="censurar", description="Cala a boca de alguém indesejado")
    @app_commands.describe(pessoa="O alvo da censura", minutos="Tempo da censura (máx 10)")
    async def comando_censurar(interaction: discord.Interaction, pessoa: discord.Member, minutos: Optional[int] = None):
        # print(f"/censurar acionado por {interaction.user}")
        
        autor = interaction.user
        tempo = minutos or 1

        if tempo > 10:
            if autor.id in abusos:
                await interaction.response.send_message(
                    f"## ⚠️ {autor.mention} NÃO aprendeu sua lição! ⚠️\n"
                    f"Foi oficialmente **AUTO-CENSURADO POR {tempo} MINUTOS!**"
                )
                try:
                    await autor.timeout(discord.utils.utcnow() + datetime.timedelta(minutes=tempo))
                except Exception:
                    await interaction.response.send_message("# ❌ PARE COM ISSO!", ephemeral=True)
                abusos.discard(autor.id)
                return
            else:
                abusos.add(autor.id)
                await interaction.response.send_message(f"❌ Calma fi, falei que é só até **10 minutos!**", ephemeral=True)
                return

        primeiro_voto = False
        if pessoa.id not in votacoes:
            votacoes[pessoa.id] = {"alvo": pessoa, "votos": set(), "tempo": tempo}
            primeiro_voto = True

        votacoes[pessoa.id]["votos"].add(autor.id)
        votos = len(votacoes[pessoa.id]["votos"])

        if primeiro_voto:
            await interaction.response.send_message(
                f"## ‼️ {autor.mention} NÃO AGUENTA MAIS {pessoa.mention} ‼️\n"
                f"> `{votos}/3 votos` para **CENSURAR por {tempo} minuto(s)!**"
            )
        else:
            await interaction.response.send_message(f"> `{votos}/3 votos` para **CENSURAR {pessoa.mention}!**")

        if votos >= 3:
            alvo = votacoes[pessoa.id]["alvo"]
            tempo = votacoes[pessoa.id]["tempo"]
            try:
                await alvo.timeout(discord.utils.utcnow() + datetime.timedelta(minutes=tempo))
                await interaction.channel.send(
                    f"## 🙌 A voz do povo é a voz de Deus! 🙌\n"
                    f"{alvo.mention} foi **CENSURADO por {tempo} minuto(s)!**"
                )
            except discord.Forbidden:
                await interaction.response.send_message("❌ Infelizmente não tenho permissão pra censurar esse cara", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"❌ Eita que deu merda: {e}", ephemeral=True)
            del votacoes[pessoa.id]
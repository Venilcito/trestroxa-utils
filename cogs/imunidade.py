import discord
from discord import app_commands
from database import load_imunes, save_imunes

def setup(bot):
    @bot.tree.command(name="imunidade", description="Torna pessoas imunes à maldição do mestre")
    @app_commands.describe(pessoa="Nome para abençoar / amaldiçoar")
    async def comando_imunidade(interaction: discord.Interaction, pessoa: discord.Member):
        # print(f"/imunidade acionado por {interaction.user}")

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Achou mesmo né", ephemeral=True)
            return
        
        imunes = load_imunes()

        if pessoa.id in imunes:
            imunes.remove(pessoa.id)
            msg = f"🥶 Imunidade de {pessoa.mention} removida!"
        else:
            imunes.append(pessoa.id)
            msg = f"🙌 Imunidade concedida a {pessoa.mention}!"
        
        save_imunes(imunes)
        await interaction.response.send_message(msg, ephemeral=True)
from typing import Optional
import discord
from discord import app_commands

def setup(bot):
    mapa_emojis = {
        "a": "🅰", "b": "🅱", "c": "🅲", "d": "🅳", "e": "🅴", "f": "🅵",
        "g": "🅶", "h": "🅷", "i": "🅸", "j": "🅹", "k": "🅺", "l": "🅻",
        "m": "🅼", "n": "🅽", "o": "🅾", "p": "🅿", "q": "🆀", "r": "🆁",
        "s": "🆂", "t": "🆃", "u": "🆄", "v": "🆅", "w": "🆆", "x": "🆇",
        "y": "🆈", "z": "🆉"
    }
    
    @bot.tree.command(name="nome", description="Muda seu nome de acordo com as normas da firma")
    @app_commands.describe(nome="Seu novo nome (até 8 letras)", pessoa="Alvo do renomeio (só admins)")
    async def comando_nome(interaction: discord.Interaction, nome: str, pessoa: Optional[discord.Member] = None):
        # print(f"/nome acionado por {interaction.user}")
        
        apelido_normalizado = "".join([c.lower() for c in nome if c.isalpha()])

        if len(apelido_normalizado) == 0:
            await interaction.response.send_message("⁉️ Ok, e o nome?", ephemeral=True); return
        if len(apelido_normalizado) > 8:
            await interaction.response.send_message("⁉️ Calma aí patrão! Tá querendo uma frase?", ephemeral=True); return

        apelido_emojis = "".join(mapa_emojis.get(c, "") for c in apelido_normalizado)

        membro = interaction.user
        if pessoa:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ Calma aí patrão, **você** só pode mudar seu próprio nome!", ephemeral=True); return
            membro = pessoa

        try:
            await membro.edit(nick=apelido_emojis)
            msg = f"✅ Nome mudado: `{apelido_emojis}`" if membro == interaction.user else f"✅ Nome de {membro.mention} mudado: `{apelido_emojis}`"
            await interaction.response.send_message(msg, ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Esse cara é especial demais! Não posso mudar o nome dele.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Fi, deu bosta aqui: {e}", ephemeral=True)

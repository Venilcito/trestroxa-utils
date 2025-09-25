from typing import Optional
import discord
from discord import app_commands

def setup(bot):
    @bot.tree.command(name="limpar_desde", description="Apaga mensagens desde uma específica (máx 100)")
    @app_commands.describe(id_mensagem="ID da primeira mensagem a ser apagada", pessoa="Só mensagens de TAL pessoa")
    async def comando_limpar_desde(interaction: discord.Interaction, id_mensagem: str, pessoa: Optional[discord.Member] = None):
        # print(f"/limpar_desde acionado por {interaction.user}")

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Calma aí patrão, você **não pode** usar esse comando!", ephemeral=True)
            return

        try:
            alvo = await interaction.channel.fetch_message(int(id_mensagem))
        except Exception:
            await interaction.response.send_message("❌ ID esquisito ein... Não consegui achar", ephemeral=True)
            return

        def check(msg: discord.Message):
            return pessoa is None or msg.author == pessoa

        await interaction.response.defer(ephemeral=True)

        msgs = []
        async for msg in interaction.channel.history(limit=99, after=alvo):
            if check(msg):
                msgs.append(msg)
        msgs.append(alvo)

        await interaction.channel.delete_messages(msgs)
        if len(msgs) == 100:
            await interaction.followup.send("⁉️ Limite de **100 mensagens** atingido! Falam coisa pra caralho ein...", ephemeral=True)
        else:
            await interaction.followup.send(f"🧹 Pronto. Ninguém mais vai ler aquelas **{len(msgs)} mensagens**", ephemeral=True)
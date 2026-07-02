from typing import Optional
import discord
from discord import app_commands

def setup(bot):
    lista_cores = [1384672131127971971, 1384672355359654058, 1384672440688578630, 1384672556413489234, 1384676175493861458, 1384672992956649572, 1384673068999381112, 1384673189921165383, 1384673259261399041, 1384673461187776652, 1384673553068196041, 1384673627726676129, 1384676316955283456, 1384673820979236874, 1384671972046405652]

    @bot.tree.command(name="cor", description="Muda a linda cor do seu nome")
    @app_commands.choices(cor=[
        app_commands.Choice(name="🔴 Vermelho", value="1384672131127971971"),
        app_commands.Choice(name="🟠 Laranja", value="1384672355359654058"),
        app_commands.Choice(name="🟡 Amarelo", value="1384672440688578630"),
        app_commands.Choice(name="🟢 Verde Claro", value="1384672556413489234"),
        app_commands.Choice(name="🌊 Verde Água", value="1384676175493861458"),
        app_commands.Choice(name="🪖 Verde Escuro", value="1384672992956649572"),
        app_commands.Choice(name="🔵 Azul Claro", value="1384673068999381112"),
        app_commands.Choice(name="☑️ Azul Escuro", value="1384673189921165383"),
        app_commands.Choice(name="🟣 Roxo", value="1384673259261399041"),
        app_commands.Choice(name="🩷 Rosa", value="1384673461187776652"),
        app_commands.Choice(name="🟤 Marrom", value="1384673553068196041"),
        app_commands.Choice(name="⚫ Preto", value="1384673627726676129"),
        app_commands.Choice(name="🩶 Cinza", value="1384676316955283456"),
        app_commands.Choice(name="⚪ Branco", value="1384673820979236874"),
        app_commands.Choice(name="🏳️‍🌈 LGBT", value="1384671972046405652")
    ])

    @app_commands.describe(cor="Sua nova cor", pessoa="Alvo do coloramento (só admins)")
    async def comando_nome(interaction: discord.Interaction, cor: app_commands.Choice[str], pessoa: Optional[discord.Member] = None):
        # print(f"/cor acionado por {interaction.user}")
        
        membro = interaction.user
        if pessoa:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ Achou mesmo né", ephemeral=True); return
            membro = pessoa

        color = interaction.guild.get_role(int(cor.value))
        if color is None:
            await interaction.response.send_message("❌ Nem existe essa cor", ephemeral=True); return
        
        cargos = membro.roles
        if color in cargos:
            await membro.remove_roles(color)
            msg = f"✅ Você agora está sem cores" if membro == interaction.user else f"✅ Cor de {membro.mention} removida"
            await interaction.response.send_message(msg, ephemeral=True)
            return

        try:
            for role in cargos:
                if role.id in lista_cores:
                    cargos.remove(role)
                    break

            cargos.append(color)
            await membro.edit(roles=cargos)
            msg = f"✅ Cor alterada: {color.mention}" if membro == interaction.user else f"✅ Cor de {membro.mention} alterada: {color.mention}"
        except discord.Forbidden:
            msg = "❌ Poder demais! Não posso mudar a cor."
        except Exception as e:
            msg = f"⚠️ Fi deu bosta: {e}"

        await interaction.response.send_message(msg, ephemeral=True)
import discord
from discord import app_commands
import troxa

letra_group = app_commands.Group(name="letra", description="Adiciona / remove um caractere na lista do ANGELO!")

def setup(bot):
    @letra_group.command(name="add", description="Adiciona um caractere na lista do ANGELO!")
    @app_commands.describe(caractere="Novo caractere pra lista", letra="Letra original do nome")
    async def comando_add(interaction: discord.Interaction, caractere: str, letra: str):
        # print(f"/letra add acionado por {interaction.user}")

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Achou mesmo né", ephemeral=True)
            return
        
        letra = letra.lower()
        subst = troxa.load_substituicoes()

        if letra not in subst:
            await interaction.response.send_message(f"`{letra}`???? Você é imbecil por acaso?", ephemeral=True)
            return
        
        atual = subst[letra]
        if caractere in atual:
            await interaction.response.send_message(f"Esse já tá incluso, amigão...", ephemeral=True)
            return
        
        subst[letra].append(caractere)
        troxa.save_substituicoes(subst)

        await interaction.response.send_message(f"`{caractere}` adicionado na lista `{letra}`!", ephemeral=True)
    

    @letra_group.command(name="rem", description="Remove um caractere na lista do ANGELO!")
    @app_commands.describe(caractere="Caractere pra remover")
    async def comando_rem(interaction: discord.Interaction, caractere: str):
        # print(f"/letra rem acionado por {interaction.user}")

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Achou mesmo né", ephemeral=True)
            return

        subst = troxa.load_substituicoes()
        letras_encontradas = [letra for letra, lista in subst.items() if caractere in lista]

        if not letras_encontradas:
            await interaction.response.send_message("Esse nem tá aí, amigão...", ephemeral=True)
            return
        
        letra = letras_encontradas[0]
        subst[letra].remove(caractere)
        troxa.save_substituicoes(subst)

        await interaction.response.send_message(f"`{caractere}` removido da lista `{letra}`!", ephemeral=True)
    
    bot.tree.add_command(letra_group)
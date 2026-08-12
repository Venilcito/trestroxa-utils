import json
import os
import re
import datetime

# ---------- imunes ----------
IMUNES_PATH = 'data/imunes.json'

def load_imunes():
    if not os.path.exists(IMUNES_PATH):
        return []
        
    with open(IMUNES_PATH, 'r') as f:
        return json.load(f)


def save_imunes(imunes):
    with open(IMUNES_PATH, 'w') as f:
        json.dump(imunes, f)


# ---------- letras ----------
SUBST_PATH = 'data/substituicoes.json'

def load_substituicoes():
    if not os.path.exists(SUBST_PATH):
        return {}

    with open(SUBST_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_substituicoes(dados):
    with open(SUBST_PATH, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


# ---------- DETECTOR DE ANGELOS!!!!!! ----------
def cria_regex_com_grupos(palavra: str) -> str:
    substituicoes = load_substituicoes()
    regex = ''

    for letra in palavra:
        lista = substituicoes.get(letra)

        if not lista:
            regex += re.escape(letra)
        else:
            grupo = '(?:' + '|'.join(re.escape(x) for x in lista) + ')'
            regex += f'({grupo})'

        regex += '.*?'
    return regex

def marca_angelo(texto: str) -> str | None:
    substituicoes = load_substituicoes()
    regex = ''

    for letra in 'angelo':
        lista = substituicoes.get(letra)
        if not lista:
            return None
        
        grupo = '(?:' + '|'.join(re.escape(x) for x in lista) + ')'
        regex += f'({grupo}).*?'

    padrao = re.compile(regex, re.DOTALL)
    match = padrao.search(texto)
    if not match:
        return None

    last_index = 0
    grupos = list(match.groups())

    resultado = '"'
    for grupo in grupos:
        busca = grupo
        idx = texto.find(busca, last_index)

        if idx == -1:
            idx = last_index

        resultado += texto[last_index:idx]

        if 0 <= idx < len(texto):
            resultado += f' **{texto[idx].upper()}** '
            last_index = idx + 1
        else:
            last_index = idx

    rest = texto[last_index:last_index + 30]
    if last_index + 30 < len(texto):
        resultado += f'{rest}..."'
    else:
        resultado += f'{rest}"'
    return resultado

async def detect_angelo(message):
    imunes = load_imunes()
    if message.author.bot or message.author.id in imunes:
        return
    
    # print("mensagem recebida!")
    content = message.content or ""
    padrao_angelo = re.compile(cria_regex_com_grupos("angelo"), re.DOTALL)
    
    try:
        match_angelo = padrao_angelo.search(content)
    except Exception:
        return
    
    if match_angelo:
        result = marca_angelo(content) or (content[:60] + ('...' if len(content) > 60 else ''))
        formatado = result.replace('\n', '\n> ')

        try:
            await message.reply(f'Pera aí... **ANGELO????**\n'
                                f'> {formatado} \n'
                                f'-# COMO OUSA citar o nome do mestre EM VÃO?! **Tá de castigo!**')
        except Exception as e:
            pass

        if message.guild:
            membro = message.author

            try:
                duracao = datetime.timedelta(seconds=60)
                await membro.timeout(duracao, reason="angelo")
            except Exception as e:
                pass
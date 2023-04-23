from PIL import Image
from io import BytesIO
import base64

def getChampionTileImg(champ_name):
    return './champions/tiles/' + champ_name + '_0.jpg'

def get_thumbnail(path: str) -> Image:
    img = Image.open(path)
    img.thumbnail((60, 60))
    return img

def image_to_base64(img_path: str) -> str:
    img = get_thumbnail(img_path)
    with BytesIO() as buffer:
        img.save(buffer, 'png') # or 'jpeg'
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(img_path: str) -> str:
    return f'<img src="data:image/png;base64,{image_to_base64(img_path)}">'

def convert_df(input_df):
     return input_df.to_html(escape=False, formatters=dict(thumbnail=image_formatter))

def getChampionNameById(id):
    if id == 1:
        return "Annie"
    elif id == 2:
        return "Olaf"
    elif id == 3:
        return "Galio"
    elif id == 4:
        return "TwistedFate"
    elif id == 5:
        return "XinZhao"
    elif id == 6:
        return "Urgot"
    elif id == 7:
        return "LeBlanc"
    elif id == 8:
        return "Vladimir"
    elif id == 9:
        return "Fiddlesticks"
    elif id == 10:
        return "Kayle"
    elif id == 11:
        return "Master Yi"
    elif id == 12:
        return "Alistar"
    elif id == 13:
        return "Ryze"
    elif id == 14:
        return "Sion"
    elif id == 15:
        return "Sivir"
    elif id == 16:
        return "Soraka"
    elif id == 17:
        return "Teemo"
    elif id == 18:
        return "Tristana"
    elif id == 19:
        return "Warwick"
    elif id == 20:
        return "Nunu"
    elif id == 21:
        return "MissFortune"
    elif id == 22:
        return "Ashe"
    elif id == 23:
        return "Tryndamere"
    elif id == 24:
        return "Jax"
    elif id == 25:
        return "Morgana"
    elif id == 26:
        return "Zilean"
    elif id == 27:
        return "Singed"
    elif id == 28:
        return "Evelynn"
    elif id == 29:
        return "Twitch"
    elif id == 30:
        return "Karthus"
    elif id == 31:
        return "Cho'Gath"
    elif id == 32:
        return "Amumu"
    elif id == 33:
        return "Rammus"
    elif id == 34:
        return "Anivia"
    elif id == 35:
        return "Shaco"
    elif id == 36:
        return "Dr.Mundo"
    elif id == 37:
        return "Sona"
    elif id == 38:
        return "Kassadin"
    elif id == 39:
        return "Irelia"
    elif id == 40:
        return "Janna"
    elif id == 41:
        return "Gangplank"
    elif id == 42:
        return "Corki"
    elif id == 43:
        return "Karma"
    elif id == 44:
        return "Taric"
    elif id == 45:
        return "Veigar"
    elif id == 48:
        return "Trundle"
    elif id == 50:
        return "Swain"
    elif id == 51:
        return "Caitlyn"
    elif id == 53:
        return "Blitzcrank"
    elif id == 54:
        return "Malphite"
    elif id == 55:
        return "Katarina"
    elif id == 56:
        return "Nocturne"
    elif id == 57:
        return "Maokai"
    elif id == 58:
        return "Renekton"
    elif id == 59:
        return "JarvanIV"
    elif id == 60:
        return "Elise"
    elif id == 61:
        return "Orianna"
    elif id == 62:
        return "Wukong"
    elif id == 63:
        return "Brand"
    elif id == 64:
        return "LeeSin"
    elif id == 67:
        return "Vayne"
    elif id == 68:
        return "Rumble"
    elif id == 69:
        return "Cassiopeia"
    elif id == 72:
        return "Skarner"
    elif id == 74:
        return "Heimerdinger"
    elif id == 75:
        return "Nasus"
    elif id == 76:
        return "Nidalee"
    elif id == 77:
        return "Udyr"
    elif id == 78:
        return "Poppy"
    elif id == 79:
        return "Gragas"
    elif id == 80:
        return "Pantheon"
    elif id == 81:
        return "Ezreal"
    elif id == 82:
        return "Mordekaiser"
    elif id == 83:
        return "Yorick"
    elif id == 84:
        return "Akali"
    elif id == 85:
        return "Kennen"
    elif id == 86:
        return "Garen"
    elif id == 89:
        return "Leona"
    elif id == 90:
        return "Malzahar"
    elif id == 91:
        return "Talon"
    elif id == 92:
        return "Riven"
    elif id == 96:
        return "Kog'Maw"
    elif id == 98:
        return "Shen"
    elif id == 99:
        return "Lux"
    elif id == 101:
        return "Xerath"
    elif id == 102:
        return "Shyvana"
    elif id == 103:
        return "Ahri"
    elif id == 104:
        return "Graves"
    elif id == 105:
        return "Fizz"
    elif id == 106:
        return "Volibear"
    elif id == 107:
        return "Rengar"
    elif id == 110:
        return "Varus"
    elif id == 111:
        return "Nautilus"
    elif id == 112:
        return "Viktor"
    elif id == 113:
        return "Sejuani"
    elif id == 114:
        return "Fiora"
    elif id == 115:
        return "Ziggs"
    elif id == 117:
        return "Lulu"
    elif id == 119:
        return "Draven"
    elif id == 120:
        return "Hecarim"
    elif id == 121:
        return "Kha'Zix"
    elif id == 122:
        return "Darius"
    elif id == 126:
        return "Jayce"
    elif id == 127:
        return "Lissandra"
    elif id == 131:
        return "Diana"
    elif id == 133:
        return "Quinn"
    elif id == 134:
        return "Syndra"
    elif id == 136:
        return "AurelionSol"
    elif id == 141:
        return "Kayn"
    elif id == 142:
        return "Zoe"
    elif id == 143:
        return "Zyra"
    elif id == 145:
        return "Kai'sa"
    elif id == 147:
        return "Seraphine"
    elif id == 150:
        return "Gnar"
    elif id == 154:
        return "Zac"
    elif id == 157:
        return "Yasuo"
    elif id == 161:
        return "Vel'Koz"
    elif id == 163:
        return "Taliyah"
    elif id == 164:
        return "Camille"
    elif id == 200:#Bel'Veth
        return "Camille"
    elif id == 201:
        return "Braum"
    elif id == 202:
        return "Jhin"
    elif id == 203:
        return "Kindred"
    elif id == 221:
        return "Zeri"
    elif id == 222:
        return "Jinx"
    elif id == 223:
        return "TahmKench"
    elif id == 234:
        return "Viego"
    elif id == 235:
        return "Senna"
    elif id == 236:
        return "Lucian"
    elif id == 238:
        return "Zed"
    elif id == 240:
        return "Kled"
    elif id == 245:
        return "Ekko"
    elif id == 246:
        return "Qiyana"
    elif id == 254:
        return "Vi"
    elif id == 266:
        return "Aatrox"
    elif id == 267:
        return "Nami"
    elif id == 268:
        return "Azir"
    elif id == 350:
        return "Yuumi"
    elif id == 360:
        return "Samira"
    elif id == 412:
        return "Thresh"
    elif id == 420:
        return "Illaoi"
    elif id == 421:
        return "Rek'Sai"
    elif id == 427:
        return "Ivern"
    elif id == 429:
        return "Kalista"
    elif id == 432:
        return "Bard"
    elif id == 497:
        return "Rakan"
    elif id == 498:
        return "Xayah"
    elif id == 516:
        return "Ornn"
    elif id == 517:
        return "Sylas"
    elif id == 518:
        return "Neeko"
    elif id == 523:
        return "Aphelios"
    elif id == 526:#Rell
        return "Rell"
    elif id == 555:
        return "Pyke"
    elif id == 711:
        return "Vex"
    elif id == 777:
        return "Yone"
    elif id == 875:
        return "Sett"
    elif id == 876:
        return "Lillia"
    elif id == 887:
        return "Gwen"
    elif id == 888:
        return "Renata"
    elif id == 895:#Nilah
        return "Gwen"
    elif id == 897:#Ksante
        return "Gwen"
    elif id == 902:#milio
        return "Gwen"
    else:
        return "Gwen"
from discord.ext import commands
import discord
import random

class Secret(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🔧 FRASES
    # =========================
    def _obtener_frases(self):
        return [
            "💀 ¡NO ME HABLES, YO NO SOPORTO BIEN LA PÉRDIDA! ¡Tengo 0 tickets!",
            "🧠 Yo soy la única que sabe donde sabe...",
            "🚬 ¿Por qué soy tan \"Leonardo Farkas lo pierde todo\"?",
            "🎬 Ara, te aplaudo con el cul...",
            "⚡ Se ve así porque tuvo que rezar",
            "🍷 ¿Ella está bien? ¿No la pegaron mal? ¿Ésto ustedes lo consideran sano?",
            "🫡 Chicos se me pegó el PC",
            "🐉 \"¿Alguien levantan\"? ¿Leviatan?",
            "❤️ ¡Ah bueno! ¡Están tal para cual! ¡\"Robo en ban\" y \"Alguien levantan\"!",
            "🤢 Amiga esto parece un pan sin cocer",
            "🔪 ¡¡AAARGH!!, ¡me quiero cortar una teta!",
            "😕 ¿Qué es ésto? \"Presiona Espacio para saltar. y luego presiona\"... \n " +
            "- No, las instrucciones están al lado",
            "😏 ¡Es un pepino! Yo identifico uno cuando sea",
            "😫 Ya... ¡¡Noooooooooo, por Dios, Consuelo!! Tú y tu...impaciencia",
            "😱 Porque yo me salí, ¡Y PERDÍ TODOS MIS TICKETS!",
            "😋 ¡Colador! ¡Embudo!",
            "🤭 Estoy descuartizando pollito",
            "🥜 ¡Aracely Nuez! De \"Almendra\", pues, de \"Nuez\"",
            "🦴 ...\"Esquelo\"",
            "♫ ¡Sí es! ¡Vivy!",
            "😡 ¡¡Amiga!! ¡¡\"Billar\" es otra cosa!! ¡Es un juego! ¡¡Tu dislexia te hizo leer"
            "\"Brillar\"!!",
            "😠 ¡Amigo! ¡Se escribe con RR! ¡Ésto es una planta marina!",
            "😨 ¡¡¡Nooooooooooooooo!!! ¡¡Ganó Camilo!! ¡¡Triunfó el mal!!",
            "😣 ¿¡Cuál es su problema!? ¿¡Quieres que me haga un backflip!?",
            "😊 Se cancela, no tengo nada este martes, ¡yupi!",
            "🙄 Ah bueno...gracias, \"amiga\". Qué bueno que somos \"amigas\"",
            "🐭 ¡Topo Gigia, es tu frase!",
            "🧴 Para echarnos cloro",
            "💪 ¿¡Por qué cada vez estoy más mamada!?",
            "⚫ ¿Quién es esta negra? Te llamaré \"Grafita\"",
            "👽 ¡Por fin quedó como una lanza!, ¡ya no parece un dildo alienígena!",
            "🤬 ¡Así de chata me tienes! ¡¡ASÍ DE CHATA ME TIENES!!"
        ]

    def _elegir_frase(self):
        return random.choice(self._obtener_frases())

    # =========================
    # 🎨 EMBED
    # =========================
    def _crear_embed_frase(self, frase):
        embed = discord.Embed(
            title="🤫 Secreto del grupo",
            description=frase,
            color=0x8e44ad
        )
        return embed

    # =========================
    # 🤫 COMANDO
    # =========================
    @commands.command(hidden=True)
    async def secreto(self, ctx):
        frase = self._elegir_frase()
        embed = self._crear_embed_frase(frase)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Secret(bot))
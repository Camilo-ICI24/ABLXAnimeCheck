import discord
from discord.ext import commands
from db import cargar, guardar, get_server_data

class Votaciones(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        emoji_map = {"1️⃣":1,"2️⃣":2,"3️⃣":3,"4️⃣":4,"5️⃣":5}
        if str(reaction.emoji) not in emoji_map:
            return

        data = cargar()
        server_data = get_server_data(data, str(reaction.message.guild.id))

        for nombre, info in server_data.items():
            if "mensaje_votacion" in info and reaction.message.id == info["mensaje_votacion"]:

                for key in info["votos"]:
                    if str(user.id) in info["votos"][key]:
                        info["votos"][key].remove(str(user.id))

                voto = emoji_map[str(reaction.emoji)]
                info["votos"][str(voto)].append(str(user.id))

                guardar(data)

                try:
                    await reaction.remove(user)
                except:
                    pass

                break

    @commands.command()
    async def votar(self, ctx, *, nombre):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        if nombre not in server_data:
            return await ctx.send("No existe")

        embed = discord.Embed(title=f"📊 {nombre}", description="1️⃣-5️⃣")

        msg = await ctx.send(embed=embed)

        for e in ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"]:
            await msg.add_reaction(e)

        info = server_data[nombre]
        info["mensaje_votacion"] = msg.id

        if "votos" not in info:
            info["votos"] = {str(i): [] for i in range(1, 6)}

        guardar(data)

    @commands.command()
    async def popular(self, ctx):
        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        ranking = []

        for n,i in server_data.items():
            votos=i.get("votos",{})
            total=sum(int(k)*len(v) for k,v in votos.items())
            cant=sum(len(v) for v in votos.values())
            prom= total/cant if cant else 0
            ranking.append((n,prom))

        ranking.sort(key=lambda x:x[1],reverse=True)

        msg="🏆\n"
        for n,p in ranking:
            msg+=f"{n} ⭐ {p:.2f}\n"

        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(Votaciones(bot))
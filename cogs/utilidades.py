from discord.ext import commands

class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lista(self, ctx):
        from db import cargar, get_server_data

        data = cargar()
        server_data = get_server_data(data, str(ctx.guild.id))

        if not server_data:
            return await ctx.send("📭 No hay animes en emisión 😢")

        mensaje = "📺 **Animes en emisión:**\n\n"

        # ordenar por nombre
        for nombre, info in sorted(server_data.items()):
            cap = info.get("capitulo", "?")
            usuarios = info.get("usuarios", [])

            # menciones bonitas
            menciones = ", ".join([f"<@{uid}>" for uid in usuarios])

            mensaje += f"🎬 **{nombre}**\n"
            mensaje += f"   📖 Capítulo: {cap}\n"

            if menciones:
                mensaje += f"   👥 Viendo: {menciones}\n"

            mensaje += "\n"

        await ctx.send(mensaje)

    @commands.command()
    async def comandos(self, ctx):
        await ctx.send(
            "📜 **Comandos disponibles:**\n\n"
            "🎬 $startanime \"Nombre\" @usuario\n"
            "👥 $unirse Nombre\n"
            "🔍 $verinfo Nombre\n"
            "⏩ $avanzar <capitulo> Nombre\n"
            "📋 $lista\n" "📊 $votar Nombre\n"
            "🏆 $popular\n"
            "✏️ $renombrar \"Nombre actual\" \"Nombre nuevo\"\n"
            "💡 Prefijos: $"
        )

    @commands.command()
    async def guia(self, ctx, comando=None):

        if not comando:
            return await ctx.send(
                "📘 Usa el comando así:\n"
                "`$guia <comando>`\n\n"
                "Ejemplo: `$guia startanime`\n\n"
                "Comandos disponibles:\n"
                "startanime, unirse, verinfo, avanzar, lista, votar, popular, renombrar"
            )

        comando = comando.lower()

        guias = {

            "startanime":
            "*Sintaxis:* `$startanime \"Nombre\" @usuario`\n"
            "→ Inicia un anime nuevo en el server para reaccionar.\n"
            "• El usuario mencionado es quien lo sugirió.\n"
            "• Comienza en capítulo 1 automáticamente.",

            "unirse":
            "*Sintaxis:* `$unirse Nombre`\n"
            "→ Te unes a un anime que otras personas estén reaccionando.\n"
            "• Te agrega a la lista de personas que lo están viendo en ese momento.",

            "verinfo":
            "*Sintaxis:* `$verinfo Nombre`\n"
            "→ Muestra información del anime.\n"
            "• Capítulo actual\n"
            "• Usuarios que lo están viendo",

            "avanzar":
            "*Sintaxis:* `$avanzar <capitulo> Nombre`\n"
            "→ Actualiza el capítulo actual del anime.\n"
            "• Reemplaza el progreso anterior",

            "lista":
            "*Sintaxis:* `$lista`\n"
            "→ Muestra todos los animes que el servidor actual está reaccionando.\n"
            "• Incluye capítulo actual y usuarios que se encuentren en reacción.",

            "votar":
            "*Sintaxis:* `$votar Nombre`\n"
            "→ Crea una votación del anime para todos los miembros del servidor.\n"
            "• Usa reacciones del 1️⃣ al 5️⃣\n"
            "• El voto se actualiza automáticamente",

            "popular":
            "*Sintaxis:* `$popular`\n"
            "→ Muestra ranking de animes.\n"
            "• Basado en promedio de votaciones",

            "renombrar":
            "*Sintaxis:* `$renombrar \"Actual\" \"Nuevo\"`\n"
            "→ Cambia el nombre de un anime.\n"
            "• Mantiene toda la información existente",

            "end":
            "*Sintaxis:* `$end \"Nombre\"`\n"
            "→ Indica la finalización de la reacción de un anime.\n"
            "• Actualiza el estado del anime, señalando que cada participante lo ha visto "
            "enteramente.",

            "progreso":
            "*Sintaxis:* `$progreso \"Nombre\"`\n"
            "→ Muestra qué tan avanzados estan ciertos usuarios en un anime.\n"
            "• Indica quienes están más adelante y más atrás en un anime en particular."
        }

        if comando not in guias:
            return await ctx.send("❌ Este comando no existe")

        await ctx.send(f"📘 **{comando}**\n\n{guias[comando]}")

async def setup(bot):
    await bot.add_cog(Utilidades(bot))
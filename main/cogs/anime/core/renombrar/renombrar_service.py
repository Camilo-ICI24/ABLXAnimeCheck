import discord
import re
from main.db import cargar, get_server_data, guardar
from main.cogs.anime.core.renombrar.renombrar_validaciones import (validar_existencia_actual, 
                                                              validar_colision_nuevo, extraer_nombres)
from main.cogs.anime.core.renombrar.renombrar_embeds import (embed_ya_en_uso, embed_nombres_identicos, 
                                                        embed_ok)


async def ejecutar_renombrar(ctx, args):
    if not args:
        return await ctx.send("⚠️ Debes usar comillas: `$renombrar \"actual\" \"nuevo\"`")

    actual, nuevo, error = extraer_nombres(args)

    if error:
        return await ctx.send(error)

    data = cargar()
    server_data = get_server_data(data, str(ctx.guild.id))

    # ❌ iguales
    if actual.lower() == nuevo.lower():
        embed = embed_nombres_identicos(ctx)
        return await ctx.send(embed=embed)

    # ❌ no existe actual
    if not validar_existencia_actual(server_data, actual):
        return await ctx.send(f"❌ No existe `{actual}`")

    # ❌ nuevo ya existe
    if validar_colision_nuevo(server_data, nuevo):
        embed = embed_ya_en_uso(ctx, nuevo)
        return await ctx.send(embed=embed)

    # 💾 rename
    server_data[nuevo] = server_data.pop(actual)
    guardar(data)

    # ✅ éxito
    embed = embed_ok(ctx, actual, nuevo)
    await ctx.send(embed=embed)

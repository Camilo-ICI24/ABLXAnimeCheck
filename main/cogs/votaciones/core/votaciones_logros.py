from main.cogs.utilidades.core.logros.logros_service import otorgar_logro
from main.cogs.votaciones.core.votaciones_gustos import registrar_voto_gustos, tiene_gustos_caoticos
from main.cogs.votaciones.core.votaciones_votos import total_animes_votados

print("LOADING FILE:", __file__)
print("IMPORTADO:", __name__)

# Procesar logros votación
async def procesar_logros_votacion(ctx, server_data, votos, promedio):
    for uid, voto in votos.items():
        await procesar_logros_usuario_votacion(ctx, server_data, uid, voto, promedio)

# Logros por usuario
async def procesar_logros_usuario_votacion(ctx, server_data, uid, voto, promedio):
    try:
        miembro = await ctx.guild.fetch_member(int(uid))
    except:
        return

    # Logro: "Obra maestra"
    if voto == 5:
        await otorgar_logro(ctx, "obra_maestra", usuario=miembro)

    # Logro: "Hater profesional"
    elif voto == 1:
        await otorgar_logro(ctx, "hater_profesional", usuario=miembro)

    # Logro: "Crítico"
    total_votados = total_animes_votados(server_data, uid)

    if total_votados >= 25:
        await otorgar_logro(ctx, "critico", usuario=miembro)

    # Logro: "Opinión polémica"
    diferencia = abs(voto - promedio)

    if diferencia >= 2:
        await otorgar_logro(ctx, "opinion_polemica", usuario=miembro)

    # Logro: "Gustos caóticos"
    votos_de_hoy = registrar_voto_gustos(ctx.guild.id, uid, voto)

    if tiene_gustos_caoticos(votos_de_hoy):
        await otorgar_logro(ctx, "gustos_caoticos", usuario=miembro)
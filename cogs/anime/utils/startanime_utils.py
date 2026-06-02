def validar_startanime(ctx, args):
    if '"' not in args:
        return '⚠️ Usa: $startanime "Nombre" @usuario'
    if not ctx.message.mentions:
        return '⚠️ Debes mencionar al menos un usuario'
    return None

def extraer_nombre(args):
    return args.split('"')[1].strip()

def ordenar_usuarios(ctx):
    contenido = ctx.message.content
    return sorted(
        ctx.message.mentions,
        key=lambda u: contenido.index(f"<@{u.id}>")
        if f"<@{u.id}>" in contenido else 999999
    )
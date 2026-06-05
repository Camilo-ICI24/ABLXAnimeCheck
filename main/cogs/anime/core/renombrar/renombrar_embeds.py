import discord

def embed_nombres_identicos(ctx):
    return discord.Embed(
        title="⚠️ Nombres idénticos",
        description="No pueden ser iguales.",
        color=discord.Color.red()
    )

def embed_ya_en_uso(ctx, nuevo):
    return discord.Embed(
        title="⚠️ Nombre en uso",
        description=f"`{nuevo}` ya pertenece a otro anime.",
        color=discord.Color.orange()
    )

def embed_ok(ctx, actual, nuevo):
    return discord.Embed(
        title="✅ Renombrado exitoso",
        description=f"`{actual}` → `{nuevo}`",
        color=discord.Color.green()
    )
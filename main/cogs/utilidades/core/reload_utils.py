from pathlib import Path
import json
import os
import unicodedata as ucd


def cargar_ids_autorizados():
    """Carga los IDs autorizados para reload desde:
    1) reload_allowed_ids.txt en la raíz del repo (csv o una por línea)
    2) variable de entorno RELOAD_ALLOWED_IDS (csv)
    3) .env.local con RELOAD_ALLOWED_IDS=...
    Devuelve un set de ints.
    """
    raiz_repo = None
    try:
        raiz_repo = Path(__file__).resolve().parents[4]

    except Exception:
        raiz_repo = None

    source = None
    raw = ""

    # 1) archivo reload_allowed_ids.txt
    if raiz_repo is not None:
        ids_file = raiz_repo / "reload_allowed_ids.txt"
        if ids_file.exists():
            try:
                raw = ids_file.read_text(encoding="utf-8").strip()
                source = f"file:{ids_file}"
            except Exception:
                raw = ""

    # 2) env var
    if not raw:
        raw = os.getenv("RELOAD_ALLOWED_IDS", "").strip()
        if raw:
            source = "env:RELOAD_ALLOWED_IDS"

    # 3) .env.local
    if not raw and raiz_repo is not None:
        try:
            env_file = raiz_repo / ".env.local"
            if env_file.exists():
                for line in env_file.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("RELOAD_ALLOWED_IDS"):
                        parts = line.split("=", 1)
                        if len(parts) == 2:
                            raw = parts[1].strip()
                            source = f"file:{env_file}"
                            break
        except Exception:
            raw = raw or ""

    if not raw:
        print("[CONFIG] No se encontraron RELOAD_ALLOWED_IDS. Lista vacía.")
        return set()

    normalized = raw.replace(",", "\n")
    ids = set()
    for part in normalized.splitlines():
        part = part.strip()
        if not part or part.startswith("#"):
            continue
        try:
            ids.add(int(part))
        except Exception:
            print(f"[CONFIG] Ignorando entrada inválida en RELOAD_ALLOWED_IDS: {part}")
            continue

    print(f"[CONFIG] IDS_AUTORIZADOS cargados desde {source}: {ids}")
    return ids


def normalizar_token(token: str) -> str:
    if not token:
        return ""
    t = token.strip().lower()
    # normalizar acentos
    try:

        t = ucd.normalize("NFKD", t)
        t = "".join(ch for ch in t if not ucd.combining(ch))

    except Exception:
        pass

    return t


def escribir_aviso_reinicio(raiz_repo: Path, aviso: dict, filename: str = ".reload_notice.json"):
    """Escribe el aviso de reinicio de forma atómica en repo_root/filename"""
    try:
        target = raiz_repo / filename
        tmp = raiz_repo / (filename + ".tmp")
        tmp.write_text(json.dumps(aviso), encoding="utf-8")
        # atomic replace
        os.replace(str(tmp), str(target))
        return target
    except Exception:
        # fall back: try direct write
        try:
            target.write_text(json.dumps(aviso), encoding="utf-8")
            return target
        except Exception:
            return None

def es_usuario_autorizado(ctx, ids_autorizados) -> bool:
    try:
        return bool(ctx.author and getattr(ctx.author, "id", None) in ids_autorizados)
    except Exception:
        return False


import discord
import asyncio
import sys


def crear_embed_denegado(owner_mention: str = None, owner_tag: str = None, guild_icon_url: str = None) -> discord.Embed:
    """Devuelve un embed rojo para acceso denegado con contacto opcional."""
    desc_contact = "Solo el desarrollador puede ejecutar este comando."
    if owner_mention:
        desc_contact = f"Contacta a {owner_mention} ({owner_tag})"
    emb = discord.Embed(title="Acceso denegado", description=desc_contact, color=0xFF4444)
    if guild_icon_url:
        try:
            emb.set_thumbnail(url=guild_icon_url)
        except Exception:
            pass
    return emb


async def pedir_confirmacion(bot, ctx, timeout: int, affirmative: set, negative: set) -> str:
    """Envía un prompt y espera respuesta S/N. Devuelve 'AFFIRMATIVE', 'NEGATIVE', 'UNKNOWN' o None si timeout."""
    await ctx.send(f"⚠️ {ctx.author.mention}, ¿confirmas relanzar el bot? Responde `S` para confirmar o `N` para cancelar. Tienes {timeout}s.")

    def _check(msg):
        return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id and bool(msg.content)

    try:
        reply = await bot.wait_for("message", timeout=timeout, check=_check)
    except asyncio.TimeoutError:
        return None

    token = normalizar_token(reply.content)
    if token in negative:
        return "NEGATIVE"
    if token in affirmative:
        return "AFFIRMATIVE"
    return "UNKNOWN"


def ejecutar_execv(who: str):
    """Imprime pasos y ejecuta os.execv para reiniciar el proceso actual.
    Nota: puede lanzar SystemExit si execv falla.
    """
    now = __import__("datetime").datetime.now().isoformat()
    print(f"[RELOAD][PYTHON] Requested by {who} at {now} - shutting down and exec'ing (python main/main.py)")
    print(f"[RELOAD][DOCKER] Requested by {who} at {now} - shutting down containerized process (docker)")
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print(f"[RELOAD][ERROR] execv failed: {e}")
        sys.exit(0)

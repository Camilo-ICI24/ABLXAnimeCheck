from cogs.utilidades.core.secretos.secretos_frases import FRASES_SECRETAS
import random

# =========================
# 🎲 FRASE RANDOM
# =========================
def elegir_frase():
    return random.choice(FRASES_SECRETAS)
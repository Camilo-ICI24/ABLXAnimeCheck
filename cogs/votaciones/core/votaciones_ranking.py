# =========================
# 🧠 RANKING
# =========================
def calcular_promedio(votos):
    votos_limpios = [int(v) for v in votos.values() if isinstance(v, int)]

    if not votos_limpios:
        return None

    total = sum(votos_limpios)
    cantidad = len(votos_limpios)

    return total / cantidad if cantidad > 0 else 0

def calcular_ranking(server_data):
    ranking = []

    for nombre, info in server_data.items():
        votos = info.get("votos", {})
        promedio = calcular_promedio(votos)

        if promedio is None:
            continue

        ranking.append((nombre, promedio, info.get("sugerido_por")))

    return sorted(ranking, key=lambda x: x[1], reverse=True)
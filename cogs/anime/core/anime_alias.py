def agregar_aliases(existentes, nuevos):
    agregados = []

    for alias in nuevos:
        if alias not in existentes:
            existentes.add(alias)
            agregados.append(alias)

    return agregados

def normalizar_aliases(aliases):
    return [a.strip() for a in aliases]
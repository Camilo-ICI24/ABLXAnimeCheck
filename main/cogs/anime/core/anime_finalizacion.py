def servidor_termino_anime(usuarios: dict, episodios_totales: int) -> bool:
    if not usuarios or not episodios_totales:
        return False

    for data in usuarios.values():
        cap = data.get("cap", 1) if isinstance(data, dict) else data

        if cap < episodios_totales:
            return False

    return True
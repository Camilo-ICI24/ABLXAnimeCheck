def obtener_animes_por_usuario(server_data, uid):
    resultados = []

    for nombre, info in server_data.items():
        usuarios = info.get("usuarios", {}) or {}

        if str(uid) in usuarios:
            data = usuarios.get(str(uid))

            if isinstance(data, dict):
                cap_user = data.get("cap", 1)
                visto = bool(data.get("visto", False))

            else:
                cap_user = data
                visto = False

            try:
                cap_sort = int(cap_user)

            except Exception:
                cap_sort = 0

            resultados.append((nombre, info, cap_user, visto, cap_sort))

    resultados.sort(key=lambda x: -x[4])

    return [(n, i, c, v) for (n, i, c, v, _) in resultados]

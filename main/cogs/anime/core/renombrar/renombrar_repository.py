def renombrar_anime(server_data, actual, nuevo):
    server_data[nuevo] = server_data.pop(actual)
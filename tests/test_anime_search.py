from main.cogs.utilidades.core.anime_search import buscar_anime


def crear_server_data():
    return {
        'naruto': {'aliases': ['ナルト', 'naruto_shippuden']},
        'onepiece': {'aliases': ['ワンピース']},
    }


def test_buscar_por_key_exacta():
    datos_server = crear_server_data()
    assert buscar_anime(datos_server, 'naruto') == 'naruto'


def test_buscar_por_alias():
    datos_server = crear_server_data()
    assert buscar_anime(datos_server, 'ナルト') == 'naruto'


def test_busqueda_fuzzy():
    datos_server = crear_server_data()

    # Ligeramente mal escrito, con typo común, pero aún así debería encontrar 'naruto'
    assert buscar_anime(datos_server, 'narut') == 'naruto'

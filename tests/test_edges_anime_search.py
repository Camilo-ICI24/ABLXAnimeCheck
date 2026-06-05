from main.cogs.utilidades.core.anime_search import buscar_anime


def test_buscar_anime_ok():

    # caso normal: búsqueda exacta
    datos_servidor = {'naruto': {'aliases': ['ナルト']}}
    resultado = buscar_anime(datos_servidor, 'naruto')
    assert resultado == 'naruto'


def test_buscar_anime_empty_fallo():

    # caso borde: entrada vacía debería devolver None (no existe)
    datos_servidor = {'naruto': {'aliases': ['ナルト']}}
    resultado = buscar_anime(datos_servidor, '')
    assert resultado is None


def test_buscar_anime_ambiguous_fallo():

    # caso borde: término sin relación no debe producir match fuzzy
    datos_servidor = {'naruto': {'aliases': ['ナルト']}, 'onepiece': {'aliases': []}}
    
    resultado = buscar_anime(datos_servidor, 'xyzq')
    assert resultado is None

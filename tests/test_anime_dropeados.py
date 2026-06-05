from main.cogs.anime.core.anime_dropeados import usuario_dropeo_anime, obtener_dropeados
import json
import main.db as db
import os
import tempfile


def test_usuario_dropeo_anime_y_obtener():
    temp_fd, path = tempfile.mkstemp(prefix='dropeados_', suffix='.json')
    os.close(temp_fd)
    with open(path, 'w', encoding='utf-8') as archivo:
        archivo.write(json.dumps({'g1': {'u1': ['naruto']}}))

    archivo_drop = db.DROPEADOS_FILE
    db.DROPEADOS_FILE = path

    try:
        assert usuario_dropeo_anime('u1', 'naruto', 'g1') is True
        assert usuario_dropeo_anime('u1', 'onepiece', 'g1') is False

        dropeados = obtener_dropeados('u1', 'g1')
        assert dropeados == ['naruto']
        
    finally:
        db.DROPEADOS_FILE = archivo_drop
        os.remove(path)

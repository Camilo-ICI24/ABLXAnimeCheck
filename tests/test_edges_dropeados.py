from main.cogs.anime.core.anime_dropeados import obtener_dropeados
from main.cogs.anime.core.dropeados.dropeados_service import dropear_anime
import json
import main.db as db
import os
import tempfile


def test_dropear_nombre_ok():

    # dropear con nombres válidos debe persistir
    fd, path = tempfile.mkstemp(prefix='dropeados_', suffix='.json')
    os.close(fd)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('{}')

    antiguo = db.DROPEADOS_FILE
    db.DROPEADOS_FILE = path

    try:
        dropear_anime('g1', 'u1', 'naruto')
        datos = json.loads(open(path, 'r', encoding='utf-8').read())
        assert 'g1' in datos and 'u1' in datos['g1']

    finally:
        db.DROPEADOS_FILE = antiguo
        os.remove(path)


def test_dropear_usuario_fallo():

    # caso borde: dropear con user id vacío no debería fallar catastróficamente
    fd, path = tempfile.mkstemp(prefix='dropeados_', suffix='.json')
    os.close(fd)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('{}')

    antiguo = db.DROPEADOS_FILE
    db.DROPEADOS_FILE = path
    try:

        # user vacío -> se almacenará bajo llave vacía
        dropear_anime('g2', '', 'onepiece')
        datos = json.loads(open(path, 'r', encoding='utf-8').read())
        assert '' in datos['g2']

    finally:
        db.DROPEADOS_FILE = antiguo
        os.remove(path)


def test_obtener_dropeados_usuario_fallo():

    # caso borde: pedir dropeados de usuario/servidor inexistente devuelve lista vacía
    fd, path = tempfile.mkstemp(prefix='dropeados_', suffix='.json')
    os.close(fd)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('{}')

    antiguo = db.DROPEADOS_FILE
    db.DROPEADOS_FILE = path

    try:
        resultado = obtener_dropeados('no_user', 'no_guild')
        assert resultado == []
        
    finally:
        db.DROPEADOS_FILE = antiguo
        os.remove(path)

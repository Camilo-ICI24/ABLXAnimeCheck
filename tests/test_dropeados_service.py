from main.cogs.anime.core.dropeados.dropeados_service import dropear_anime
import json
import main.db as db
import os
import tempfile


def test_dropear_appends_and_persists():
    fd, path = tempfile.mkstemp(prefix='dropeados_', suffix='.json')
    os.close(fd)

    with open(path, 'w', encoding='utf-8') as f:
        f.write('{}')

    archivo_drop = db.DROPEADOS_FILE
    db.DROPEADOS_FILE = path
    try:

        # dropear_anime debería crear la estructura y persistir
        dropear_anime('guild1', 'user1', 'naruto')

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert 'guild1' in data
        assert 'user1' in data['guild1']
        assert 'naruto' in data['guild1']['user1']
        
    finally:
        db.DROPEADOS_FILE = archivo_drop
        os.remove(path)

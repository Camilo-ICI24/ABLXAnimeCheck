from main.cogs.utilidades.core.normalizacion import (normalizar, quitar_acentos, limpiar_simbolos, 
                                                     limpiar_espacios)


def test_quitar_acentos():
    assert quitar_acentos("árbol") == "arbol"
    assert quitar_acentos("Ñandú") == "Nandu"


def test_limpiar_simbolos_y_espacios():
    frase = " Hello, World!!  \n"
    assert limpiar_simbolos(frase).strip() == " Hello World  " .strip()
    assert limpiar_espacios("a   b\n c") == "a b c"


def test_normalizar():
    assert normalizar("  Ánimo!!! ") == "animo"
    assert normalizar("TeSt\t") == "test"

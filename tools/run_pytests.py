import importlib.util
import pkgutil
import inspect
import sys
import os

# Asegurar que el directorio raíz del proyecto esté en sys.path para importar módulos de main
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

def correr_tests(modulo):
    mod = importlib.import_module(modulo)
    tests = [getattr(mod, n) for n in dir(mod) if n.startswith('test_')]
    for prueba in tests:
        try:
            prueba()
            print(f"OK: {modulo}.{prueba.__name__}")

        except Exception as e:
            print(f"FALLÓ: {modulo}.{prueba.__name__} -> {e}")
            raise

if __name__ == '__main__':
    
    # Auto-descubrir módulos de test dentro del paquete `tests`
    paquete_tests = importlib.import_module('tests')
    for finder, name, ispkg in pkgutil.iter_modules(paquete_tests.__path__):
        module_name = f"tests.{name}"
        correr_tests(module_name)

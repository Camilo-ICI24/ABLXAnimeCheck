# ABLX Anime Check Bot

Bot de Discord para gestionar animes en comunidad: seguimiento de capítulos, progreso por usuario, votaciones y ranking.

---

## 📑 Índice

- [Características](#características)
- [Comandos principales](#-comandos-principales)
- [Funcionamiento del bot](#funcionamiento-del-bot)
- [Sistema de logros](#sistema-de-logros)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Ejecución del bot](#-ejecución-del-bot)
- [Estado del proyecto](#estado-del-proyecto)
- [Mejoras a futuro](#mejoras-a-futuro)
- [Nota final](#nota-final)

---

## Características

- 🎬 Registro de animes por servidor  
- 👥 Seguimiento de usuarios viendo un anime  
- ⏩ Control de progreso por capítulo  
- ✅ Sistema de “anime visto” por usuario  
- 📊 Votaciones con reacciones (1️⃣ a 5️⃣)  
- 🏆 Ranking automático por popularidad  
- 🏷️ Soporte de aliases (nombres alternativos)  
- 🔍 Búsqueda inteligente (normalización + fuzzy match)  
- 🏅 Sistema de logros otorgados a cada usuario

---

## Comandos principales
- 🎬 $startanime "Nombre" @usuarios
- 👥 $unirse Nombre
- 🔍 $verinfo Nombre
- ⏩ $avanzar <capitulo> Nombre
- 📋 $lista
- 📊 $votar Nombre
- 🏆 $popular 
- 🏷️ $alias "Nombre" "alias1" ... 
- ⚠️ $visto Nombre (obsoleto, mantenido por compatibilidad)
- 🔄 $actualizar Nombre
- ❌ $eliminaranime "Nombre"
- ✏️ $renombrar \"Nombre actual\" \"Nombre nuevo\"
- "⬇️ $dropear Nombre \n"
- "📤 $dropeados\n"
- "🔄 $desdropear Nombre\n"
- 📦 $infobot
- 🏓 $ping
- 🏅 $logros

---

## Funcionamiento del bot

El bot guarda la información por servidor en un archivo JSON (`animes_server.json`), incluyendo:

- Usuarios y su progreso  
- Estado de “visto”  
- Votaciones  
- Metadata del anime (imagen, episodios, etc.)  

Además:
- Integra la API de **Jikan (MyAnimeList)** para obtener datos automáticamente  
- Soporta migración de datos antiguos a nuevos formatos 

El bot permite registrar el avance en la reacción de un anime, ya sea de forma individual o grupal mediante varios comandos disponibles, premiando a los usuarios que logren finalizar una reacción íntegramente. A su vez, permite calificaciones grupales a los animes que se encuentren viendo en el momento mediante un sistema de votación privado, el cual también se almacena para obtener un listado de los animes con mejor recepción en el servidor.

Cuenta también con una opción de dropear un anime en el caso de que la emisión no satisfaga completamente a uno o más miembros de la reacción, pudiendo abandonar la visualización del annime de manera temporal o permanentemente, almacenando una lista de programas abandonados en un JSON asociado (`dropeados_server.json`).

Adicionalmente, cuenta con un sistema de logros en primera fase, la cual es otorgado a cada usuario si cumple con ciertos requisitos definidos. Dichas recompensas pueden ser personalizadas para cada servidor, incluso agregando nuevos logros y tipos de rarezas para mejorar la experiencia de los usuarios.

El bot cuenta con funcionamiento híbrido, pudiendo iniciarse desde el archivo principal ```main.py``` en la consola, o mediante el Docker Compose, utilizando la imagen creada para un funcionamiento permanente, asegurando integridad de los datos almacenados en los archivos JSON durante la ejecución, gracias al uso de volúmenes persistentes.

---

## Sistema de logros

El bot incluye un sistema de logros desbloqueables que recompensa
distintas acciones realizadas por los usuarios:

- Primer capítulo
- Primer maratón
- Speedrunner
- Finalista
- Maratonista
- Sin dormir
- Coleccionista

Los logros se almacenan por servidor y usuario. También es posible modificar, crear y eliminar logros directamente desde el JSON asignado, con el objetivo de entregar una experiencia más única y personalidada para el servidor.

## Estructura del proyecto
```bash
├── cogs
│   ├── anime
│   │   ├── anime.py
│   │   ├── comandos
│   │   │   ├── __init__.py
│   │   │   ├── alias.py
│   │   │   ├── avanzar.py
│   │   │   ├── actualizar.py
│   │   │   ├── eliminaranime.py
│   │   │   ├── progreso.py
│   │   │   ├── renombrar.py
│   │   │   ├── startanime.py
│   │   │   ├── unirse.py
│   │   │   ├── verinfo.py
│   │   │   ├── dropear.py
│   │   │   ├── dropeados.py
│   │   │   ├── desdropear.py
│   │   │   └── visto.py
│   │   ├── core
│   │   │   ├── anime_alias.py
│   │   │   ├── anime_api.py
│   │   │   ├── anime_embeds.py
│   │   │   ├── anime_finalizacion.py
│   │   │   ├── anime_progreso.py
│   │   │   ├── anime_repository.py
│   │   │   ├── anime_service.py
│   │   │   ├── anime_users.py
│   │   │   ├── anime_visto.py
│   │   │   ├── __init__.py
│   │   │   ├── renombrar
│   │   │   │   ├── __init__.py
│   │   │   │   ├── renombrar_embeds.py
│   │   │   │   ├── renombrar_repository.py
│   │   │   │   ├── renombrar_service.py
│   │   │   │   └── renombrar_validaciones.py
│   │   │   ├── actualizar
│   │   │   │   ├── __init__.py
│   │   │   │   └── actualizar_service.py
│   │   ├── __init__.py
│   │   └── utils
│   │       ├── eliminaranime_utils.py
│   │       ├── __init__.py
│   │       └── startanime_utils.py
│   ├── __init__.py
│   ├── utilidades
│   │   ├── comandos
│   │   │   ├── comandos.py
│   │   │   ├── guia.py
│   │   │   ├── ha.py
│   │   │   ├── infobot.py
│   │   │   ├── __init__.py
│   │   │   ├── lista.py
│   │   │   ├── logros.py
│   │   │   ├── ping.py
│   │   │   └── secreto.py
│   │   ├── core
│   │   │   ├── anime_search.py
│   │   │   ├── comandos_texto.py
│   │   │   ├── embeds.py
│   │   │   ├── estadisticas_helpers.py
│   │   │   ├── guia_helpers.py
│   │   │   ├── __init__.py
│   │   │   ├── lista_helpers.py
│   │   │   ├── logros
│   │   │   │   ├── __init__.py
│   │   │   │   ├── logros_cargar.py
│   │   │   │   ├── logros_data.py
│   │   │   │   ├── logros_embeds.py
│   │   │   │   ├── logros_estados.py
│   │   │   │   ├── logros_helpers.py
│   │   │   │   ├── logros_paginacion.py
│   │   │   │   └── logros_service.py
│   │   │   ├── normalizacion.py
│   │   │   ├── paginacion.py
│   │   │   ├── progreso_helpers.py
│   │   │   ├── secretos
│   │   │   │   ├── secretos_frases.py
│   │   │   │   └── secretos_utils.py
│   │   │   └── zona_horaria.py
│   │   ├── estadisticas.py
│   │   ├── __init__.py
│   │   └── utilidades.py
│   └── votaciones
│       ├── comandos
│       │   ├── __init__.py
│       │   ├── popular.py
│       │   └── votar.py
│       ├── core
│       │   ├── __init__.py
│       │   ├── votaciones_api.py
│       │   ├── votaciones_buscar.py
│       │   ├── votaciones_embeds.py
│       │   ├── votaciones_gustos.py
│       │   ├── votaciones_logros.py
│       │   ├── votaciones_ranking.py
│       │   ├── votaciones_reacciones.py
│       │   ├── votaciones_service.py
│       │   └── votaciones_votos.py
│       ├── __init__.py
│       └── votaciones.py
├── data
│   ├── animes_server.json
│   ├── gustos_server.json
│   ├── logros.json
│   ├── logros_server.json
│   ├── rarezas.json
│   └── uso_server.json
├── db.py
├── docker-compose.yml
├── Dockerfile
├── __init__.py
├── main.py
├── README.md
├── requirements.txt
├── tokendiscord.txt
└── tokengithub.txt

```
---

## Requisitos

- Python 3.12+ (ejecución local)
- Docker + Docker Compose (ejecución mediante contenedores)

---

## Ejecución del bot

Este proyecto soporta dos formas de ejecución:

- 🐍 Ejecución local (Python)
- 🐳 Ejecución con Docker (recomendado)

### Ejecución con Python

### 1. Clonar repositorio
```bash
git clone https://github.com/Camilo-ICI24/ABLXAnimeCheck.git
cd ABLXAnimeCheck
```

### 2. Crear ambiente virtual
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar token
Crea un archivo -env o configúralo dentro del código
```bash
DISCORD_TOKEN=token_personal_de_discord
```

---

### Ejecución con Docker

```bash
# Construir y ejecutar
docker compose up --build

# Ejecutar en segundo plano
docker compose up -d

# Detener contenedores
docker compose down

# Ver logs
docker compose logs -f
```
---

## 🧪 Ejecutar tests

Hay dos formas de ejecutar las pruebas unitarias:

- Opción recomendada (pytest):

  1. Instala pytest (preferible dentro de un virtualenv):

     ```bash
     pip install -r requirements.txt   # si incluyes pytest en requirements
     # o solo pytest
     pip install pytest
     ```

  2. Ejecuta todos los tests:

     ```bash
     pytest -q
     ```

  3. Ejecuta un test concreto:

     ```bash
     pytest tests/test_anime_search.py -q
     ```

- Opción alternativa (runner ligero, no requiere pytest):

  - Ejecuta el runner incluido que descubre y ejecuta los tests de forma simple:

    ```bash
    python tools/run_pytests.py
    ```

---

## Estado del proyecto

Versión actual:

v0.6.0 — Donut
v0.6.0 — Donut

> Un sistema suave, dulce y caótico… donde nada queda realmente perdido.
> Un sistema suave, dulce y caótico… donde nada queda realmente perdido.

## Mejoras a futuro

- 🔔 Notificaciones de nuevos capítulos
- 🌐 Base de datos en lugar de JSON
- 🧪 Tests automatizados
- 🏆 Más logros personalizados
- ???

---

## Nota final
He invertido una cantidad de tiempo irracional al desarrollo de este proyecto, pero continúo porque me siento orgulloso de lo que he creado.
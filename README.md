# ABLX Anime Check Bot

Bot de Discord para gestionar animes en comunidad: seguimiento de capítulos, progreso por usuario, votaciones y ranking.

---

## 📑 Índice

- [Características](#características)
- [Comandos principales](#-comandos-principales)
- [Funcionamiento del bot](#funcionamiento-del-bot)
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

## 🚀 Comandos principales
- 🎬 $startanime "Nombre" @usuarios
- 👥 $unirse Nombre
- 🔍 $verinfo Nombre
- ⏩ $avanzar <capitulo> Nombre
- 📋 $lista
- 📊 $votar Nombre
- 🏆 $popular 
- 🏷️ $alias "Nombre" "alias1" ... 
- ✅ $visto "Nombre"
- ❌ $eliminaranime "Nombre"
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

Adicionalmente, cuenta con un sistema de logros en primera fase, la cual es otorgado a cada usuario si cumple con ciertos requisitos definidos. Dichas recompensas pueden ser personalizadas para cada servidor, incluso agregando nuevos logros y tipos de rarezas para mejorar la experiencia de los usuarios.

El bot cuenta con funcionamiento híbrido, pudiendo iniciarse desde el archivo principal ```main.py``` en la consola, o mediante el Docker Compose, utilizando la imagen creada para un funcionamiento permanente, asegurando integridad de los datos almacenados en los archivos JSON durante la ejecución, gracias al uso de volúmenes persistentes.

---

## Estructura del proyecto
```bash
cogs/
├── anime.py
├── secretos.py
├── usobot.py
├── utilidades.py
└── votaciones.py

db.py
logros.py
main.py
requirements.txt
Dockerfile
docker-compose.yml
```
---

## Requisitos

- Python 3.12+ (ejecución local)
- Docker + Docker Compose (ejecución mediante contenedores)

---

## 🚀 Ejecución del bot

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

### 🐳 Ejecución con Docker

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

## Estado del proyecto

Versión actual:

v0.5.0 — Requiem

> El sistema despierta… y los animes no se olvidan.

## Mejoras a futuro

- 📈 Sistema de estadísticas más avanzado
- 🔔 Notificaciones de nuevos capítulos
- 🌐 Base de datos en lugar de JSON
- 🧪 Tests automatizados

---

## Nota final
Le he dedicado casi la mayor parte de mi tiempo libre a este bot.
La verad no sé qué he hecho con mi carrera a estas alturas.
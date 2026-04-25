# ABLX Anime Check Bot

Bot de Discord para gestionar animes en comunidad: seguimiento de capítulos, progreso por usuario, votaciones y ranking.

---

## 📑 Índice

- [Características](#características)
- [Comandos principales](#-comandos-principales)
- [Funcionamiento del bot](#funcionamiento-del-bot)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
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

---

## Estructura del proyecto
```bash
cogs/
├── anime.py
├── utilidades.py
└── votaciones.py

db.py
main.py
requirements.txt
```
---

## Instalación

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

### 5. Ejecutar
```bash
python main.py
```

---

## Estado del proyecto

Versión actual:

v0.4.1 — Aftermath

> Después del milagro… ordenar el caos.

---

## Mejoras a futuro

- 📈 Sistema de estadísticas más avanzado
- 🔔 Notificaciones de nuevos capítulos
- 🌐 Base de datos en lugar de JSON
- 🧪 Tests automatizados

---

## Nota final
Este bot nació como una idea simple…
y terminó convirtiéndose en un sistema bastante sólido.
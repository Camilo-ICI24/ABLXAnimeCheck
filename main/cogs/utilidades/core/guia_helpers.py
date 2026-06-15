def guia_general():
    return (
        "📘 Usa el comando así:\n"
        "`$guia <comando>`\n\n"
        "Ejemplo: `$guia startanime`\n\n"
        "Comandos disponibles:\n"
        "startanime, unirse, verinfo, avanzar, lista, votar, popular, renombrar,  "
        "guia, progreso, eliminaranime"
    )

def obtener_guias():
    return {
        "startanime":
        "*Sintaxis:* $startanime \"Nombre\" @sugeridor @user1 @user2 @user_n\n"
        "→ Inicia un anime nuevo en el server para reaccionar.\n"
        "• El usuario mencionado es quien lo sugirió.\n"
        "• Comienza en capítulo 1 automáticamente.",

        "unirse":
        "*Sintaxis:* $unirse Nombre\n"
        "→ Te unes a un anime que otras personas estén reaccionando.\n"
        "• Te agrega a la lista de personas que lo están viendo en ese momento.",

        "verinfo":
        "*Sintaxis:* $verinfo Nombre\n"
        "→ Muestra información del anime.\n"
        "• Capítulo actual\n"
        "• Usuarios que lo están viendo",

        "avanzar":
        "*Sintaxis:* $avanzar <capitulo> Nombre\n"
        "→ Actualiza el capítulo actual del anime.\n"
        "• Reemplaza el progreso anterior",

        "lista":
        "*Sintaxis:* $lista\n"
        "→ Muestra todos los animes que el servidor actual está reaccionando.\n"
        "• Incluye capítulo actual y usuarios que se encuentren en reacción.",

        "votar":
        "*Sintaxis:* $votar Nombre\n"
        "→ Crea una votación del anime para todos los miembros del servidor.\n"
        "• Usa reacciones del 1️⃣ al 5️⃣\n"
        "• El voto se actualiza automáticamente",

        "popular":
        "*Sintaxis:* $popular\n"
        "→ Muestra ranking de animes.\n"
        "• Basado en promedio de votaciones",

        "renombrar":
        "*Sintaxis:* $renombrar \"Actual\" \"Nuevo\"\n"
        "→ Cambia el nombre de un anime.\n"
        "• Mantiene toda la información existente",

        "infobot":
        "*Sintaxis:* $infobot\n"
        "→ Entrega todos los datos relacionados con el desarrollo actual del bot.\n"
        "• Link del repositorio, versión actual y desarrollador.",

        "guia":
        "*Sintaxis:* $guia \"Comando\"\n"
        "→ Entrega la información relacionada al uso de un comando en particular.\n"
        "• Indica nomenclatura, parámetros y la acción que realiza.",

        "eliminaranime":
        "*Sintaxis:* $eliminaranime \"Nombre\"\n"
        "→ Elimina completamente un anime del servidor.\n"
        "• Borra progreso, usuarios y votos.\n"
        "• No se puede recuperar.",

        "progreso":
        "*Sintaxis:* $progreso \"Nombre\"\n"
        "→ Muestra qué tan avanzados están los usuarios en un anime.\n"
        "• Indica quién va más adelantado o atrasado.",

        "alias":
        "*Sintaxis:* $alias \"Nombre\" \"alias1\" \"alias2\" ...\n"
        "→ Permite agregar nombres alternativos a un anime.\n"
        "• Facilita buscar el anime con diferentes nombres o abreviaciones.\n"
        "• Puedes agregar múltiples aliases en un solo comando.",

        "visto":
        "*Sintaxis:* $visto \"Nombre\"\n"
        "→ Marca el anime como terminado para ti.\n"
        "• Añade un ✅ junto a tu progreso en $lista.\n"
        "• No afecta a otros usuarios.\n"
        "• Puedes seguir avanzando luego si el anime continúa.\n"
        "⚠️ *Deprecado:* El comando $visto está deprecado y puede eliminarse en futuras versiones.\n",

        "ping":
        "*Sintaxis:* $ping\n"
        "→ Muestra la latencia del bot y si se encuentra operativo",

        "logros":
        "*Sintaxis:* $logros @usuario\n"
        "→ Muestra los logros obtenidos por un usuario.\n"
        "• Incluye descripción y fecha de obtención."
        "• Si el usuario no es especificado, muestra tus propios logros.",

        "actualizar":
        "*Sintaxis:* $actualizar \"Nombre\" \"Nuevo nombre\"\n"
        "→ Cambia el nombre de un anime registrado.\n"
        "• Mantiene el progreso, votos y usuarios asociados al anime.\n"
        "• Útil para corregir errores o actualizar a un nombre más común.",

        "dropear":
        "*Sintaxis:* $dropear Nombre\n"
        "→ Marca el anime como abandonado para ti.\n"
        "• Añade un ❌ junto a tu progreso en $lista.\n",

        "dropeados":
        "*Sintaxis:* $dropeados\n"
        "→ Muestra todos los animes que has abandonado.\n"
        "• Lista los animes con el estado de dropeado.",

        "desdropear":
        "*Sintaxis:* $desdropear Nombre\n"
        "→ Elimina el estado de abandonado para un anime.\n"
        "• Quita el ❌ junto a tu progreso en $lista.\n"
        "• Permite volver a avanzar en el anime si lo deseas.",

        "⚠️ relanzar":
        "*Sintaxis:* $relanzar\n"
        "→ Reinicia el bot de forma segura, guardando estado previo y cargando funcionalidades nuevas\n"
        "• Solo usuarios autorizados pueden usarlo\n",

        "secreto":
        "???"
    }

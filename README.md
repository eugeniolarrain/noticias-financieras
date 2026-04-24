# Noticias Financieras Telegram 📰

Bot que envía las 5 noticias más importantes del mundo financiero a Telegram todos los días a las 8:00 AM (hora de Chile).

## Configuración

### 1. Crear bot de Telegram
1. Busca **@BotFather** en Telegram
2. Envía `/newbot` y sigue las instrucciones
3. Guarda el **TOKEN** que te dé

### 2. Obtener tu Chat ID
1. Busca **@userinfobot** en Telegram
2. Envía cualquier mensaje
3. Guarda tu **Chat ID**

### 3. Obtener API Key de GNews
1. Ve a https://gnews.io/
2. Click "Get API Key" (gratis, 100 requests/día)
3. Regístrate y guarda tu API Key

### 4. Configurar secrets en GitHub
En tu repositorio, ve a **Settings → Secrets → Actions → New repository secret**:

| Nombre | Valor |
|--------|-------|
| `TELEGRAM_BOT_TOKEN` | El token de BotFather |
| `TELEGRAM_CHAT_ID` | Tu Chat ID |
| `NEWS_API_KEY` | Tu API Key de NewsAPI |

### 5. Probar que funciona
1. Ve a la pestaña **Actions** en GitHub
2. Click en "Enviar Noticias Financieras"
3. Click en "Run workflow"
4. Deberías recibir un mensaje en Telegram

## Horario

El bot está configurado para ejecutarse a las **8:00 AM hora de Chile**:
- Verano (sept-marzo): 11:00 UTC
- Invierno (abril-agosto): 12:00 UTC

## Archivos

- `main.py` - Script principal
- `requirements.txt` - Dependencias
- `.github/workflows/noticias.yml` - Workflow de GitHub Actions

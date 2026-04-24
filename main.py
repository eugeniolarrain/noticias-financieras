import os
import requests
from datetime import datetime

def obtener_noticias():
    """Obtiene las 5 noticias más importantes de finanzas."""

    api_key = os.environ.get("NEWS_API_KEY")
    if not api_key:
        raise ValueError("NEWS_API_KEY no configurada")

    # Intento 1: Top headlines business US
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": "business",
        "country": "us",
        "pageSize": 10,
        "apiKey": api_key
    }

    print(f"Llamando a NewsAPI: {url}")
    response = requests.get(url, params=params)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")

    if data.get("status") == "ok" and data.get("totalResults", 0) > 0:
        articulos = data.get("articles", [])
        print(f"Encontradas {len(articulos)} noticias")
        return articulos[:5]

    # Intento 2: Buscar por keywords de finanzas
    print("Intentando búsqueda por keywords...")
    url2 = "https://newsapi.org/v2/everything"
    params2 = {
        "q": "stock market OR finance OR economy OR wall street",
        "sortBy": "popularity",
        "language": "en",
        "pageSize": 5,
        "apiKey": api_key
    }

    response2 = requests.get(url2, params=params2)
    data2 = response2.json()
    print(f"Response 2: {data2}")

    if data2.get("status") == "ok":
        return data2.get("articles", [])[:5]

    return []


def enviar_telegram(mensaje):
    """Envía un mensaje a Telegram."""

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise ValueError("Faltan credenciales de Telegram")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensaje,
        "parse_mode": "HTML"
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def main():
    print(f"[{datetime.now()}] Iniciando obtención de noticias...")

    try:
        articulos = obtener_noticias()

        if not articulos:
            enviar_telegram("📰 <b>Noticias Financieras</b>\n\nNo se encontraron noticias hoy. Revisa los logs del workflow.")
            return

        # Construir el mensaje
        fecha = datetime.now().strftime("%d/%m/%Y")
        mensaje = f"📰 <b>Noticias Financieras - {fecha}</b>\n\n"

        for i, articulo in enumerate(articulos, 1):
            titulo = articulo.get("title", "Sin título")
            url = articulo.get("url", "")
            descripcion = articulo.get("description", "")

            # Limitar título a 100 caracteres
            if len(titulo) > 100:
                titulo = titulo[:97] + "..."

            mensaje += f"{i}. <b>{titulo}</b>\n"
            if descripcion:
                mensaje += f"   _{descripcion[:150]}..._\n"
            mensaje += f"   🔗 <a href='{url}'>Leer más</a>\n\n"

        mensaje += "<i>Que tengas un gran día de inversiones! 📈</i>"

        enviar_telegram(mensaje)
        print(f"[{datetime.now()}] Noticias enviadas exitosamente!")

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        enviar_telegram(error_msg)
        print(f"[{datetime.now()}] Error: {e}")
        raise


if __name__ == "__main__":
    main()

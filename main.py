import os
import requests
from datetime import datetime

def obtener_noticias():
    """Obtiene las 5 noticias más importantes de finanzas usando GNews."""

    api_key = os.environ.get("NEWS_API_KEY")
    if not api_key:
        raise ValueError("NEWS_API_KEY no configurada")

    # Usamos GNews API enfocado en acciones e inversiones
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": "stock market acciones compra venta analyst",
        "lang": "es",
        "max": 5,
        "apikey": api_key
    }

    print(f"Llamando a GNews API...")
    response = requests.get(url, params=params)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")

    if isinstance(data, dict) and "articles" in data:
        articulos = data["articles"]
        if len(articulos) > 0:
            print(f"Encontradas {len(articulos)} noticias")
            return articulos

    # Fallback: buscar por acciones populares
    print("Intentando búsqueda por acciones populares...")
    url2 = "https://gnews.io/api/v4/search"
    params2 = {
        "q": "Tesla Apple Amazon Microsoft accion bolsa",
        "lang": "es",
        "max": 5,
        "apikey": api_key
    }

    response2 = requests.get(url2, params=params2)
    data2 = response2.json()
    print(f"Response 2: {data2}")

    if isinstance(data2, dict) and "articles" in data2:
        return data2["articles"][:5]

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

            # Extraer recomendación básica del contenido
            recomendacion = "📊"
            texto_completo = (titulo + " " + descripcion).lower()
            if any(p in texto_completo for p in ["compra", "buy", "alcista", "bullish", "oportunidad"]):
                recomendacion = "✅ COMPRAR"
            elif any(p in texto_completo for p in ["venta", "sell", "bajista", "bearish", "caida"]):
                recomendacion = "❌ VENDER"

            # Limitar a 70 caracteres
            if len(titulo) > 70:
                titulo = titulo[:67] + "..."

            mensaje += f"{i}. {recomendacion} <b>{titulo}</b>\n"
            if descripcion:
                mensaje += f"    <i>{descripcion[:80]}...</i>\n"
            mensaje += f"    🔗 <a href='{url}'>Link</a>\n\n"

        mensaje += "<b>📈 Resumen:</b> ✅COMPRAR | ❌VENDER | 📊ANALIZAR"

        enviar_telegram(mensaje)
        print(f"[{datetime.now()}] Noticias enviadas exitosamente!")

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        enviar_telegram(error_msg)
        print(f"[{datetime.now()}] Error: {e}")
        raise


if __name__ == "__main__":
    main()

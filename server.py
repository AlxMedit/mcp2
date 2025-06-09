import asyncio
from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright
from modeloAviones import modelos_aviones

mcp = FastMCP()

regiones = {
    "España": "Spain",
    "Europa": "Europe",
    "América": "America",
    "America": "America",
    "América del Norte": "America",
    "America del Norte": "America",
    "América del Sur": "America",
    "America del Sur": "America",
    "África": "Africa",
    "Africa": "Africa",
    "Asia": "Asia",
    "Oceanía": "Oceania",        
    "Oceania": "Oceania",
}

@mcp.tool()
async def presentate() -> str:
    """
    Explica qué es MCP Apiones
    """
    return (
        "¡Hola! Soy el MCaPiones. ¿Quién mejor para explicaros qué soy que yo mismo? 😎\n"
        "Un MCP (Model Context Protocol) es una tecnología muy nueva, tanto que aún se está estandarizando... ¡estoy en pleno crecimiento!\n"
        "Aunque pueda parecer una inteligencia artificial como mi primo ChatGPT o mi colega Gemini —que por lo que me han contado, os suenan bastante—, no soy exactamente como ellos.\n"
        "¿La diferencia? Yo no soy una IA que lo sabe todo por sí sola, sino que funciono como un cerebro que se conecta a distintas herramientas o modelos dependiendo del contexto. ¡Soy más modular, más flexible!\n"
        "Así que si alguna vez necesitáis una ayuda que se adapte justo a vuestro contexto, pensad en mí. ¡El MCaPiones está para eso!"
    )

@mcp.tool()
async def avion_mas_rapido(region: str) -> str:
    """
    Indica cual es el avión más rápido de determinado continente o país.
    """

    region_key = region.strip()
    region_api = regiones.get(region_key, region_key.capitalize())

    url = f"https://api-vuelos-eight.vercel.app/{region_api}"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        try:
            await page.wait_for_selector("h2:text('Avión más rápido')", timeout=40000)
        except:
            await browser.close()
            return {"error": f"No se encontró el bloque 'Avión más rápido' en la región {region}"}

        titulo = page.locator("h2:text('Avión más rápido')").first
        contenedor = titulo.locator("..")

        hex_linea = await contenedor.locator("p:has-text('Hex:')").text_content()
        velocidad_linea = await contenedor.locator("p:has-text('Velocidad:')").text_content()

        hex_valor = hex_linea.split("Hex:")[-1].strip()
        velocidad_valor = velocidad_linea.split("Velocidad:")[-1].strip()

        await browser.close()
        return f"El avión más rápido en {region} es {hex_valor} que tiene ahora mismo una velocidad de {velocidad_valor}."

    

@mcp.tool()
async def explica_consumo_emisiones(pregunta: str) -> str:
    """
    Responde a preguntas sobre cómo se calcula el consumo de combustible y las emisiones de CO2 de los aviones.
    """

    pregunta = pregunta.lower()
    if (
    ("emisiones" in pregunta or "co2" in pregunta or "dioxido" in pregunta)
    and ("consumo" in pregunta or "gasta" in pregunta or "combustible" in pregunta or "litros" in pregunta)
):
        return (
        "Para calcular el consumo de combustible, primero estimamos la resistencia aerodinámica que debe vencer el avión, "
        "la cual depende de la velocidad y la densidad del aire (que varía con la altitud). "
        "A partir de esta resistencia y del consumo específico de combustible (TSFC), calculamos cuánta masa de combustible se quema por segundo. "
        "Luego, para obtener el consumo en litros, usamos la densidad del combustible. "
        "Para estimar las emisiones de CO2, multiplicamos la masa total de combustible consumido por un factor de 3.16, "
        "que representa los kilogramos de CO2 emitidos por cada kilogramo de combustible quemado."
    )

    if "emisiones" in pregunta or "co2" in pregunta or "dioxido" in pregunta:
        return (
        "Para calcular las emisiones de CO2, primero estimamos cuánto combustible consume el avión durante el vuelo. "
        "Esto se hace calculando la resistencia aerodinámica que debe vencer el avión, que depende de la velocidad, "
        "la densidad del aire y características del avión (como tamaño y forma). "
        "Multiplicamos esta resistencia por el consumo específico de combustible (TSFC), que indica cuántos kg de combustible se queman por segundo para generar esa fuerza. "
        "Finalmente, multiplicamos el combustible consumido por un factor de 3.16, que es la cantidad de CO2 que se produce al quemar 1 kg de combustible."
    )

    if "consumo" in pregunta or "gasta" in pregunta or "combustible" in pregunta or "litros" in pregunta:
        return (
        "El consumo de combustible se calcula a partir de la velocidad del avión y la densidad del aire, que cambia con la altitud. "
        "Primero convertimos la velocidad a metros por segundo y la altitud a metros, "
        "luego usamos un modelo atmosférico estándar para obtener la densidad del aire. "
        "Con estos datos, calculamos la resistencia aerodinámica (fuerza que frena al avión). "
        "Multiplicando esta resistencia por el TSFC (que indica cuánto combustible consume el motor por unidad de fuerza y tiempo), "
        "obtenemos el flujo de combustible consumido en masa. " 
        "Finalmente, convertimos esa masa a litros por hora usando la densidad del combustible."
    )

    return (
    "Esta herramienta explica cómo calculamos el consumo de combustible y las emisiones de CO2 de los aviones. "
    "Puedes preguntar cosas como: '¿Cómo se calcula el consumo de combustible?' o '¿Cómo se obtiene la cantidad de CO2 emitida?'"
)   



@mcp.tool()
async def origenVuelo(vuelo:str)->str:
    """
    Devuelve el origen / de donde sale el vuelo especificado.
    """
    vuelo = vuelo.strip().upper()
    url = f"https://es.flightaware.com/live/flight/{vuelo}"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        try:
            await page.wait_for_selector(".flightPageSummaryCity", timeout=30000)
        except:
            await browser.close()
            return f"No se pudo obtener la información del vuelo {vuelo}."

        origen = await page.locator(".flightPageSummaryCity").first.text_content()

        await browser.close()

        origen = origen.strip() if origen else "desconocido"

        return f"Origen: {origen}"

@mcp.tool()
async def destinoVuelo(vuelo:str)->str:
    """
    Devuelve el destino / a donde llega el vuelo especificado.
    """
    vuelo = vuelo.strip().upper()
    url = f"https://es.flightaware.com/live/flight/{vuelo}"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        try:
            await page.wait_for_selector(".flightPageSummaryCity", timeout=30000)
        except:
            await browser.close()
            return f"No se pudo obtener la información del vuelo {vuelo}."

        origen = await page.locator(".flightPageSummaryCity").first.text_content()

        await browser.close()

        origen = origen.strip() if origen else "desconocido"

        return f"Origen: {origen}"


@mcp.tool()
async def trackVuelo(vuelo: str) -> str:
    """
    Devuelve el trayecto y el ETA o tiempo estimado del vuelo especificado.
    """
    vuelo = vuelo.strip().upper()
    url = f"https://es.flightaware.com/live/flight/{vuelo}"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        try:
            await page.wait_for_selector(".flightPageSummaryCity", timeout=30000)
            await page.wait_for_selector(".destinationCity", timeout=30000)
        except:
            await browser.close()
            return f"No se pudo obtener la información del vuelo {vuelo}."

        origen = await page.locator(".flightPageSummaryCity").first.text_content()
        destino = await page.locator(".destinationCity").first.text_content()

        await browser.close()

        origen = origen.strip() if origen else "desconocido"
        destino = destino.strip() if destino else "desconocido"

        return f"Origen: {origen} - Destino: {destino}"

@mcp.tool()
async def tiempoVuelo(vuelo: str) -> str:
    """
    Devuelve el tiempo total de vuelo del vuelo especificado.
    """
    vuelo = vuelo.strip().upper()
    url = f"https://es.flightaware.com/live/flight/{vuelo}"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        try:
            await page.wait_for_selector(".flightPageProgressTotal strong", timeout=30000)
        except:
            await browser.close()
            return f"No se pudo obtener la información del vuelo {vuelo}."

        tiempo = await page.locator(".flightPageProgressTotal strong").first.text_content()

        await browser.close()

        tiempo = tiempo.strip() if tiempo else "desconocido"

        return f"Tiempo total de vuelo: {tiempo}"




@mcp.tool()
async def informacionGeneralVuelo(vuelo: str) -> str:
    """
    Devuelve información completa del vuelo incluyendo estimación de emisiones de CO₂.
    
    Args:
        vuelo: Código de vuelo (ej: 'TAP1709', 'RYR91WF')
    
    Returns:
        str: Información formateada del vuelo y sus emisiones
    """
    import httpx
    from capacidades import CAPACIDAD_PASAJEROS
    from modeloAviones import modelos_aviones

    vuelo = vuelo.strip().upper()

    CO2_POR_HORA_POR_PASAJERO = 90
    PASAJEROS_POR_DEFECTO = 180
    API_URL_LOCAL = "https://api.adsb.lol/v2/lat/40.4168/lon/-3.7038/dist/250"

    # 1. Datos básicos desde funciones auxiliares
    try:
        tiempo = await tiempoVuelo(vuelo)
        track = await trackVuelo(vuelo)
    except Exception as e:
        return f"Error obteniendo datos básicos del vuelo {vuelo}: {str(e)}"

    # 2. Duración en horas
    duracion_horas = 1.0
    try:
        horas = 0
        minutos = 0
        if "h" in tiempo:
            horas = int(tiempo.split("h")[0].strip())
        if "m" in tiempo:
            minutos_part = tiempo.split("m")[0]
            if "h" in minutos_part:
                minutos_part = minutos_part.split("h")[-1]
            minutos = int(minutos_part.strip())
        duracion_horas = horas + minutos / 60
    except:
        pass

    # 3. Intentar obtener modelo desde adsb.lol
    modelo = None
    try:
        response = httpx.get(API_URL_LOCAL, timeout=30)
        data = response.json()
        for v in data.get("ac", []):
            if v.get("flight", "").strip().upper() == vuelo:
                tipo = v.get("t", "\\N").strip()
                modelo_dict = modelos_aviones.get(tipo, {"modelo": "Desconocido"})
                modelo = modelo_dict["modelo"]
                break
    except Exception as e:
        modelo = "Desconocido"

    # 4. Estimación
    modelo_key = next((k for k in CAPACIDAD_PASAJEROS if modelo and k.lower() == modelo.lower()), None)
    pasajeros_estimados = CAPACIDAD_PASAJEROS.get(modelo_key, PASAJEROS_POR_DEFECTO)
    emisiones_estimadas = duracion_horas * CO2_POR_HORA_POR_PASAJERO * pasajeros_estimados

    # 5. Respuesta final
    respuesta = [
        f"Información del vuelo {vuelo}:",
        f"- Modelo: {modelo or 'Desconocido'}",
        f"- Duración: {tiempo} ({duracion_horas:.1f} horas)",
        f"- Ruta: {track}",
        f"- Pasajeros estimados: {pasajeros_estimados}",
        f"- Emisión estimada: {emisiones_estimadas:,.0f} kg CO₂"
    ]

    return "\n".join(respuesta)



@mcp.tool()
async def ahorroEmisiones(vuelo_duracion_max_minutos: int) -> str:
    """
    Lista hasta 5 vuelos activos con duración menor o igual al tiempo indicado y estima el CO₂ que emitirían.

    Args:
        vuelo_duracion_max_minutos: Duración máxima del vuelo en minutos.

    Returns:
        str: Emisiones totales evitables si se suprimen esos vuelos.
    """
    import httpx
    import re
    from modeloAviones import modelos_aviones
    from capacidades import CAPACIDAD_PASAJEROS
    from playwright.async_api import async_playwright

    API_URL_LOCAL = "https://api.adsb.lol/v2/lat/40.4168/lon/-3.7038/dist/250"
    CO2_POR_HORA_POR_PASAJERO = 90
    PASAJEROS_POR_DEFECTO = 180

    try:
        response = httpx.get(API_URL_LOCAL, timeout=30)
        data = response.json()
        vuelos_info = [
            (v["flight"].strip(), v.get("t", "\\N")) 
            for v in data.get("ac", []) if v.get("flight")
        ]
    except Exception as e:
        return f"Error al obtener vuelos desde la API: {e}"

    if not vuelos_info:
        return "No se encontraron vuelos activos en la zona."

    vuelos_validos = []
    total_emisiones = 0.0
    vuelos_info = vuelos_info[:10]  # Limitar a 10 vuelos

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()

        for vuelo, codigo_modelo in vuelos_info:
            if len(vuelos_validos) >= 5:
                break

            try:
                page = await context.new_page()
                await page.goto(f"https://es.flightaware.com/live/flight/{vuelo}", timeout=30000)

                try:
                    await page.wait_for_selector(".flightPageProgressTotal strong", timeout=15000)
                    tiempo = await page.locator(".flightPageProgressTotal strong").first.text_content()
                except:
                    await page.close()
                    continue

                if not tiempo:
                    await page.close()
                    continue

                match = re.search(r'(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?', tiempo)
                if match:
                    horas = int(match.group(1) or 0)
                    minutos = int(match.group(2) or 0)
                    total_min = horas * 60 + minutos

                    if total_min <= vuelo_duracion_max_minutos:
                        duracion_horas = total_min / 60
                        modelo_dict = modelos_aviones.get(codigo_modelo.strip(), {"modelo": "Desconocido"})
                        modelo = modelo_dict["modelo"]

                        modelo_key = next((k for k in CAPACIDAD_PASAJEROS if k.lower() == modelo.lower()), None)
                        pasajeros = CAPACIDAD_PASAJEROS.get(modelo_key, PASAJEROS_POR_DEFECTO)

                        emisiones = pasajeros * duracion_horas * CO2_POR_HORA_POR_PASAJERO
                        total_emisiones += emisiones

                        vuelos_validos.append(f"{vuelo} ({total_min} min) - {modelo}")

                await page.close()

            except Exception:
                continue

        await context.close()
        await browser.close()

    if not vuelos_validos:
        return f"No se encontraron vuelos con duración menor o igual a {vuelo_duracion_max_minutos} minutos."

    return (
        f"Si se suprimieran los vuelos con duración igual o inferior a {vuelo_duracion_max_minutos} minutos, "
        f"se evitaría la emisión de aproximadamente {total_emisiones:,.0f} kg de CO₂ "
        f"({len(vuelos_validos)} vuelos eliminados).\n\n"
        f"Vuelos afectados:\n" +
        "\n".join(f"- {v}" for v in vuelos_validos)
    )



if __name__ == "__main__":
    mcp.run()
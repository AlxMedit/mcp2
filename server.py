import asyncio
from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright

mcp = FastMCP()

@mcp.tool()
async def avion_mas_rapido(region: str) -> str:
    """
    Indica cual es el avión más rápido de determinado continente o país.
    """
    region_map = {
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

    region_key = region.strip()
    region_api = region_map.get(region_key, region_key.capitalize())

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


if __name__ == "__main__":
    mcp.run()

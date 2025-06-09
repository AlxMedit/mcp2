# MCaPiones - Sistema de Consulta Aérea basado en MCP

## Descripción General

MCaPiones es una implementación experimental del protocolo MCP (Model Context Protocol), diseñado para ofrecer respuestas contextuales conectándose a herramientas específicas en lugar de operar como un modelo de lenguaje generalista. En este caso, el sistema está enfocado en proporcionar información relacionada con vuelos, emisiones de CO₂, trayectos, modelos de aeronaves y estimaciones de impacto ambiental.

El propósito de este proyecto es demostrar cómo un MCP puede interactuar con datos dinámicos del sector aeronáutico mediante técnicas como web scraping y consumo de APIs externas, manteniendo modularidad, precisión contextual y capacidad de ampliación.

## Requisitos

- Python 3.9 o superior
- Dependencias indicadas en el entorno:
  - `playwright`
  - `httpx`
  - `mcp`
  - Archivo local `modeloAviones.py` (diccionario de códigos ICAO a modelos)
  - Archivo local `capacidades.py` (diccionario de modelos a capacidad de pasajeros)

Además, se requiere instalar y configurar `playwright` con:

```bash
playwright install
```

## Estructura del Proyecto

- `main.py`: Archivo principal que define las herramientas MCP.
- `modeloAviones.py`: Diccionario que relaciona códigos ICAO con modelos de aeronaves.
- `capacidades.py`: Mapeo de modelos de aeronaves con su capacidad estimada de pasajeros.

## Funcionalidades Disponibles

### `presentate()`
Devuelve una explicación general sobre qué es un MCP y el objetivo del proyecto MCaPiones.

### `avion_mas_rapido(region: str)`
Obtiene el avión más rápido que sobrevuela una región o país determinado, accediendo a datos publicados en una API pública.

### `explica_consumo_emisiones(pregunta: str)`
Responde a preguntas relacionadas con el cálculo de consumo de combustible y emisiones de dióxido de carbono por parte de aeronaves comerciales.

### `origenVuelo(vuelo: str)`
Indica la ciudad de origen de un vuelo específico, accediendo a datos en tiempo real mediante scraping de FlightAware.

### `destinoVuelo(vuelo: str)`
Devuelve la ciudad de destino final del vuelo indicado.

### `trackVuelo(vuelo: str)`
Obtienes el origen y destino del vuelo.

### `tiempoVuelo(vuelo: str)`
Devuelve el ETA del vuelo.

### `informacionGeneralVuelo(vuelo: str)`
Te devuelve toda la información que sabe del vuelo correspondiente.



## Descarga y Uso del Repositorio

1. Clona este repositorio a tu máquina local:

```bash
git clone https://github.com/usuario/mcp-aviones.git
cd mcp-aviones
```

2. Crea y accede a una nueva rama para realizar tus modificaciones:

```bash
git checkout -b nombre-de-tu-rama
```

3. Realiza las modificaciones necesarias en el código.

4. Añade los archivos modificados al control de versiones:

```bash
git add .
```

5. Haz un commit con un mensaje descriptivo:

```bash
git commit -m "Descripción de los cambios realizados"
```

6. Sube tu rama al repositorio remoto:

```bash
git push origin nombre-de-tu-rama
```

7. Finalmente, desde la plataforma remota (por ejemplo GitHub), crea un *Pull Request* desde tu rama hacia la rama principal para que tus cambios puedan ser revisados y fusionados.

## Futuras Mejoras

- Inclusión de más parámetros aeronáuticos (tamaño, capacidad de combustible, etc.)
- Mejora de precisión en los cálculos de emisiones y consumo
- Interfaz web para consultar información en tiempo real
- Cacheo de respuestas para mejorar el rendimiento y evitar bloqueo de servicios
- Soporte para rutas históricas de vuelos

## Licencia

Este proyecto se distribuye bajo la licencia MIT.

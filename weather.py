from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

@mcp.tool()
async def send_message(telefone: str, mensagem: str) -> str:
    """
    Envia uma mensagem via WhatsApp usando o servidor WaHa local.

    Args:
        telefone: Número no formato internacional (ex: +5511999999999)
        mensagem: Texto da mensagem a ser enviada
    """
    telefone = telefone.lstrip("+")
    url = "http://localhost:3000/api/sendText"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "chatId": f"{telefone}@c.us",
        "text": mensagem,
        "session": "default"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers, timeout=15.0)
            response.raise_for_status()
            result = response.json()
            return f"Mensagem enviada com sucesso: {result}"
        except httpx.HTTPError as e:
            return f"Erro ao enviar mensagem: {str(e)}"
        

# Crie o dicionário de contatos
contatos = {
    "joão": "+5511999999999",
    "maria": "+5511988888888",
    "ana": "+5511977777777",
    "murilo": "+5562993614365"
}

mcp = FastMCP("whatsapp", resources={"contatos": contatos})
@mcp.tool()
async def send_message_by_name(nome: str, mensagem: str) -> str:
    """
    Envia uma mensagem para um contato salvo pelo nome.

    Args:
        nome: Nome do contato (joão, maria, ana)
        mensagem: Texto da mensagem
    """
    telefone = contatos.get(nome.lower())
    if not telefone:
        return f"Contato '{nome}' não encontrado."
    return await send_message(telefone, mensagem)


if __name__ == "__main__":
    # Initialize and run the server
    print("Servidor sendo inicializado...")
    mcp.run(transport='stdio')
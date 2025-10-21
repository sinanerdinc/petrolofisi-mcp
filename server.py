import json
from utils import scrape_website
from fastmcp import FastMCP

mcp = FastMCP(name="Petrol Ofisi MCP")
BASE_PRICE_URL = "https://www.petrolofisi.com.tr/akaryakit-fiyatlari"

@mcp.tool()
def get_prices():
    """
    Returns the prices for gasoline, diesel, and autogas.The prices are transformed by appending "TL"
    to indicate Turkish Lira as the unit.
    """
    selectors = {
        'city': {'selector': '.price-row td:first-child', 'attribute': None},
        'gasoline': {'selector': '.price-row td:nth-child(2) .with-tax', 'attribute': None},
        'diesel': {'selector': '.price-row td:nth-child(3) .with-tax', 'attribute': None},
        'autogas': {'selector': '.price-row td:nth-child(7) .with-tax', 'attribute': None}
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        result = scrape_website(BASE_PRICE_URL, selectors, headers)
        data = json.loads(result)

        mapped = [
            {
                "city": city,
                "gasoline": gasoline + " TL",
                "diesel": diesel + " TL",
                "autogas": autogas + " TL"
            }
            for city, gasoline, diesel, autogas in zip(
                data["city"], data["gasoline"], data["diesel"], data["autogas"]
            )
        ]

        json_output = json.dumps(mapped, ensure_ascii=False, indent=2)
        return json_output
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run()

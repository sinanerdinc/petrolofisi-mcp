# Petrolofisi MCP
Petrol Ofisi Mcp Server provides up-to-date fuel prices across Turkey on a city-by-city basis

```
https://petrolofisi.fastmcp.app/mcp
```

## Example Config
```
"mcpServers": {
    "petrolofisi": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://petrolofisi.fastmcp.app/mcp"
      ]
    }
  }
```


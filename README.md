# Weather MCP Server

A simple Model Context Protocol (MCP) server that provides weather information and demonstrates the core concepts of building MCP servers.

## Features

This MCP server demonstrates:
- **Resources**: Weather data for different locations (New York, London, Tokyo)
- **Tools**: Functions to get current weather and forecasts
- **Prompts**: Templates for weather reports and comparisons

## Installation

1. Install the required dependencies:
```bash
pip3 install -r requirements.txt
```

2. (Optional) Create a `.env` file for configuration:
```bash
WEATHER_API_KEY=your_weather_api_key_here
SERVER_NAME=weather-mcp-server
SERVER_VERSION=1.0.0
LOG_LEVEL=INFO
```

## Running the Server

Run the server directly:
```bash
python3 weather_mcp_server.py
```

## Available Resources

The server provides weather resources for:
- `weather://new_york` - Weather for New York, NY
- `weather://london` - Weather for London, UK  
- `weather://tokyo` - Weather for Tokyo, Japan

## Available Tools

1. **get_weather**: Get current weather for any location
   - Parameters: `location` (string, required)

2. **get_weather_forecast**: Get weather forecast for a location
   - Parameters: `location` (string, required), `days` (integer, 1-7, default: 3)

## Available Prompts

1. **weather_report**: Generate a detailed weather report
   - Parameters: `location` (string, required)

2. **weather_comparison**: Compare weather between two locations
   - Parameters: `location1` (string, required), `location2` (string, required)

## Testing the Server

You can test the server using the MCP inspector tool or integrate it with an MCP-compatible client.

## Example Usage

This is a mock implementation that uses sample data. In a real-world scenario, you would:
1. Replace the mock data with actual weather API calls
2. Add authentication and error handling
3. Implement caching for better performance
4. Add more detailed weather information

## MCP Protocol Overview

This server implements the Model Context Protocol, which consists of:

- **Resources**: Static or dynamic data sources that can be read
- **Tools**: Functions that can be called to perform actions
- **Prompts**: Template messages for LLM interactions

The server communicates via JSON-RPC over stdio, making it easy to integrate with various MCP clients.

## Extending the Server

To add new functionality:

1. **Add new tools**: Define new functions in the `handle_call_tool` method
2. **Add new resources**: Update the `handle_list_resources` and `handle_read_resource` methods
3. **Add new prompts**: Update the `handle_list_prompts` and `handle_get_prompt` methods

## Dependencies

- `mcp>=1.0.0`: Model Context Protocol SDK
- `httpx>=0.25.0`: HTTP client for API calls
- `python-dotenv>=1.0.0`: Environment variable loading 
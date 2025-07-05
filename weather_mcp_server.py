#!/usr/bin/env python3
"""
Weather MCP Server

A simple MCP server that provides weather information using a mock weather API.
This demonstrates the core concepts of building an MCP server:
- Resources: Weather data for different locations
- Tools: Functions to get weather information
- Prompts: Templates for weather-related queries
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
import httpx
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    Prompt,
    TextContent,
    ImageContent,
    EmbeddedResource,
    CallToolResult,
    ListResourcesResult,
    ListToolsResult,
    ListPromptsResult,
    ReadResourceResult,
    GetPromptResult,
)
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherMCPServer:
    """Weather MCP Server implementation"""
    
    def __init__(self):
        self.server = Server("weather-mcp-server")
        self.weather_api_key = os.getenv("WEATHER_API_KEY", "demo_key")
        self.mock_weather_data = {
            "new_york": {
                "location": "New York, NY",
                "temperature": 72,
                "humidity": 65,
                "conditions": "Partly cloudy",
                "wind_speed": 8,
                "last_updated": "2024-01-15T14:30:00Z"
            },
            "london": {
                "location": "London, UK",
                "temperature": 18,
                "humidity": 78,
                "conditions": "Overcast",
                "wind_speed": 12,
                "last_updated": "2024-01-15T14:30:00Z"
            },
            "tokyo": {
                "location": "Tokyo, Japan",
                "temperature": 25,
                "humidity": 60,
                "conditions": "Clear",
                "wind_speed": 5,
                "last_updated": "2024-01-15T14:30:00Z"
            }
        }
        
        # Setup MCP server handlers
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all the MCP server handlers"""
        
        @self.server.list_resources()
        async def handle_list_resources() -> ListResourcesResult:
            """List available weather resources"""
            resources = []
            for city_key, data in self.mock_weather_data.items():
                resources.append(
                    Resource(
                        uri=f"weather://{city_key}",
                        name=f"Weather for {data['location']}",
                        description=f"Current weather conditions in {data['location']}",
                        mimeType="application/json",
                    )
                )
            return ListResourcesResult(resources=resources)
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> ReadResourceResult:
            """Read a specific weather resource"""
            if not uri.startswith("weather://"):
                raise ValueError(f"Unknown resource URI: {uri}")
            
            city_key = uri.replace("weather://", "")
            if city_key not in self.mock_weather_data:
                raise ValueError(f"Unknown city: {city_key}")
            
            weather_data = self.mock_weather_data[city_key]
            return ReadResourceResult(
                contents=[
                    TextContent(
                        type="text",
                        text=json.dumps(weather_data, indent=2)
                    )
                ]
            )
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """List available weather tools"""
            tools = [
                Tool(
                    name="get_weather",
                    description="Get current weather information for a specified location",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city or location to get weather for"
                            }
                        },
                        "required": ["location"]
                    }
                ),
                Tool(
                    name="get_weather_forecast",
                    description="Get weather forecast for a specified location",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city or location to get forecast for"
                            },
                            "days": {
                                "type": "integer",
                                "description": "Number of days to forecast (1-7)",
                                "default": 3
                            }
                        },
                        "required": ["location"]
                    }
                )
            ]
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls"""
            if name == "get_weather":
                return await self.get_weather(arguments.get("location", ""))
            elif name == "get_weather_forecast":
                return await self.get_weather_forecast(
                    arguments.get("location", ""),
                    arguments.get("days", 3)
                )
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        @self.server.list_prompts()
        async def handle_list_prompts() -> ListPromptsResult:
            """List available weather prompts"""
            prompts = [
                Prompt(
                    name="weather_report",
                    description="Generate a weather report for a location",
                    arguments=[
                        {
                            "name": "location",
                            "description": "The location to generate a weather report for",
                            "required": True
                        }
                    ]
                ),
                Prompt(
                    name="weather_comparison",
                    description="Compare weather between two locations",
                    arguments=[
                        {
                            "name": "location1",
                            "description": "First location to compare",
                            "required": True
                        },
                        {
                            "name": "location2",
                            "description": "Second location to compare",
                            "required": True
                        }
                    ]
                )
            ]
            return ListPromptsResult(prompts=prompts)
        
        @self.server.get_prompt()
        async def handle_get_prompt(name: str, arguments: Dict[str, str]) -> GetPromptResult:
            """Get a specific prompt"""
            if name == "weather_report":
                location = arguments.get("location", "")
                weather_data = await self.get_weather_data(location)
                prompt_text = f"""
Please provide a detailed weather report for {location} based on the following data:

{json.dumps(weather_data, indent=2)}

Include:
- Current temperature and conditions
- Humidity and wind information
- Any recommendations for outdoor activities
- Comparison to seasonal averages if possible
"""
                return GetPromptResult(
                    description=f"Weather report for {location}",
                    messages=[
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": prompt_text
                            }
                        }
                    ]
                )
            elif name == "weather_comparison":
                location1 = arguments.get("location1", "")
                location2 = arguments.get("location2", "")
                weather1 = await self.get_weather_data(location1)
                weather2 = await self.get_weather_data(location2)
                
                prompt_text = f"""
Compare the weather conditions between {location1} and {location2}:

{location1} Weather:
{json.dumps(weather1, indent=2)}

{location2} Weather:
{json.dumps(weather2, indent=2)}

Please provide a comparison highlighting:
- Temperature differences
- Weather conditions
- Which location might be better for outdoor activities
- Any notable differences in humidity or wind
"""
                return GetPromptResult(
                    description=f"Weather comparison between {location1} and {location2}",
                    messages=[
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": prompt_text
                            }
                        }
                    ]
                )
            else:
                raise ValueError(f"Unknown prompt: {name}")

    async def get_weather(self, location: str) -> CallToolResult:
        """Get weather for a specific location"""
        try:
            weather_data = await self.get_weather_data(location)
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps(weather_data, indent=2)
                    )
                ]
            )
        except Exception as e:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Error getting weather for {location}: {str(e)}"
                    )
                ],
                isError=True
            )

    async def get_weather_forecast(self, location: str, days: int) -> CallToolResult:
        """Get weather forecast for a specific location"""
        try:
            # Generate mock forecast data
            base_weather = await self.get_weather_data(location)
            forecast = []
            
            for i in range(days):
                day_weather = base_weather.copy()
                # Add some variation to the forecast
                day_weather["temperature"] += (i * 2) - 2
                day_weather["date"] = f"2024-01-{16 + i}"
                forecast.append(day_weather)
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps({
                            "location": location,
                            "forecast_days": days,
                            "forecast": forecast
                        }, indent=2)
                    )
                ]
            )
        except Exception as e:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Error getting forecast for {location}: {str(e)}"
                    )
                ],
                isError=True
            )

    async def get_weather_data(self, location: str) -> Dict[str, Any]:
        """Get weather data for a location (mock implementation)"""
        location_key = location.lower().replace(" ", "_").replace(",", "")
        
        # Try to find in mock data first
        for key, data in self.mock_weather_data.items():
            if key in location_key or location_key in key:
                return data
        
        # If not found, return generic data
        return {
            "location": location,
            "temperature": 20,
            "humidity": 70,
            "conditions": "Unknown",
            "wind_speed": 10,
            "last_updated": datetime.now().isoformat()
        }

async def main():
    """Run the weather MCP server"""
    weather_server = WeatherMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await weather_server.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="weather-mcp-server",
                server_version="1.0.0",
                capabilities=weather_server.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main()) 
#!/usr/bin/env python3
"""
Simple MCP Server - Standalone Version

A simplified MCP server that demonstrates core concepts without external dependencies.
This version uses only Python's standard library and includes a basic JSON-RPC implementation.
"""

import json
import sys
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleMCPServer:
    """A simple MCP server implementation using only standard library"""
    
    def __init__(self):
        self.server_name = "simple-weather-mcp-server"
        self.server_version = "1.0.0"
        self.capabilities = {
            "resources": {},
            "tools": {},
            "prompts": {},
            "logging": {}
        }
        
        # Mock weather data
        self.weather_data = {
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
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC requests"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            logger.info(f"Handling request: {method}")
            
            if method == "initialize":
                return self.handle_initialize(request_id, params)
            elif method == "resources/list":
                return self.handle_list_resources(request_id)
            elif method == "resources/read":
                return self.handle_read_resource(request_id, params)
            elif method == "tools/list":
                return self.handle_list_tools(request_id)
            elif method == "tools/call":
                return self.handle_call_tool(request_id, params)
            elif method == "prompts/list":
                return self.handle_list_prompts(request_id)
            elif method == "prompts/get":
                return self.handle_get_prompt(request_id, params)
            else:
                return self.error_response(request_id, -32601, f"Method not found: {method}")
                
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return self.error_response(request.get("id"), -32603, str(e))
    
    def handle_initialize(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": self.capabilities,
                "serverInfo": {
                    "name": self.server_name,
                    "version": self.server_version
                }
            }
        }
    
    def handle_list_resources(self, request_id: Any) -> Dict[str, Any]:
        """List available resources"""
        resources = []
        for city_key, data in self.weather_data.items():
            resources.append({
                "uri": f"weather://{city_key}",
                "name": f"Weather for {data['location']}",
                "description": f"Current weather conditions in {data['location']}",
                "mimeType": "application/json"
            })
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "resources": resources
            }
        }
    
    def handle_read_resource(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read a specific resource"""
        uri = params.get("uri", "")
        
        if not uri.startswith("weather://"):
            return self.error_response(request_id, -32602, f"Unknown resource URI: {uri}")
        
        city_key = uri.replace("weather://", "")
        if city_key not in self.weather_data:
            return self.error_response(request_id, -32602, f"Unknown city: {city_key}")
        
        weather_data = self.weather_data[city_key]
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "contents": [
                    {
                        "type": "text",
                        "text": json.dumps(weather_data, indent=2)
                    }
                ]
            }
        }
    
    def handle_list_tools(self, request_id: Any) -> Dict[str, Any]:
        """List available tools"""
        tools = [
            {
                "name": "get_weather",
                "description": "Get current weather information for a specified location",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city or location to get weather for"
                        }
                    },
                    "required": ["location"]
                }
            },
            {
                "name": "get_weather_forecast",
                "description": "Get weather forecast for a specified location",
                "inputSchema": {
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
            }
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools
            }
        }
    
    def handle_call_tool(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool calls"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "get_weather":
                return self.get_weather(request_id, arguments.get("location", ""))
            elif tool_name == "get_weather_forecast":
                return self.get_weather_forecast(
                    request_id, 
                    arguments.get("location", ""),
                    arguments.get("days", 3)
                )
            else:
                return self.error_response(request_id, -32602, f"Unknown tool: {tool_name}")
                
        except Exception as e:
            return self.error_response(request_id, -32603, f"Tool execution failed: {str(e)}")
    
    def handle_list_prompts(self, request_id: Any) -> Dict[str, Any]:
        """List available prompts"""
        prompts = [
            {
                "name": "weather_report",
                "description": "Generate a weather report for a location",
                "arguments": [
                    {
                        "name": "location",
                        "description": "The location to generate a weather report for",
                        "required": True
                    }
                ]
            },
            {
                "name": "weather_comparison",
                "description": "Compare weather between two locations",
                "arguments": [
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
            }
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "prompts": prompts
            }
        }
    
    def handle_get_prompt(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get a specific prompt"""
        prompt_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if prompt_name == "weather_report":
            location = arguments.get("location", "")
            weather_data = self.get_weather_data(location)
            prompt_text = f"""
Please provide a detailed weather report for {location} based on the following data:

{json.dumps(weather_data, indent=2)}

Include:
- Current temperature and conditions
- Humidity and wind information
- Any recommendations for outdoor activities
- Comparison to seasonal averages if possible
"""
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "description": f"Weather report for {location}",
                    "messages": [
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": prompt_text
                            }
                        }
                    ]
                }
            }
        elif prompt_name == "weather_comparison":
            location1 = arguments.get("location1", "")
            location2 = arguments.get("location2", "")
            weather1 = self.get_weather_data(location1)
            weather2 = self.get_weather_data(location2)
            
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
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "description": f"Weather comparison between {location1} and {location2}",
                    "messages": [
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": prompt_text
                            }
                        }
                    ]
                }
            }
        else:
            return self.error_response(request_id, -32602, f"Unknown prompt: {prompt_name}")
    
    def get_weather(self, request_id: Any, location: str) -> Dict[str, Any]:
        """Get weather for a specific location"""
        weather_data = self.get_weather_data(location)
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(weather_data, indent=2)
                    }
                ]
            }
        }
    
    def get_weather_forecast(self, request_id: Any, location: str, days: int) -> Dict[str, Any]:
        """Get weather forecast for a specific location"""
        base_weather = self.get_weather_data(location)
        forecast = []
        
        for i in range(days):
            day_weather = base_weather.copy()
            # Add some variation to the forecast
            day_weather["temperature"] += (i * 2) - 2
            day_weather["date"] = f"2024-01-{16 + i}"
            forecast.append(day_weather)
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "location": location,
                            "forecast_days": days,
                            "forecast": forecast
                        }, indent=2)
                    }
                ]
            }
        }
    
    def get_weather_data(self, location: str) -> Dict[str, Any]:
        """Get weather data for a location"""
        location_key = location.lower().replace(" ", "_").replace(",", "")
        
        # Try to find in mock data first
        for key, data in self.weather_data.items():
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
    
    def error_response(self, request_id: Any, code: int, message: str) -> Dict[str, Any]:
        """Generate an error response"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }

def main():
    """Main function - run the MCP server"""
    server = SimpleMCPServer()
    
    print(f"[INFO] Starting {server.server_name} v{server.server_version}")
    print("[INFO] Server is ready to accept requests on stdin/stdout")
    
    # In a real MCP server, this would handle JSON-RPC over stdio
    # For demonstration, let's show some example interactions
    
    # Example 1: List resources
    print("\n" + "="*50)
    print("EXAMPLE 1: List Resources")
    print("="*50)
    request = {"jsonrpc": "2.0", "id": 1, "method": "resources/list"}
    response = server.handle_request(request)
    print(f"Request: {json.dumps(request, indent=2)}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    # Example 2: Read a resource
    print("\n" + "="*50)
    print("EXAMPLE 2: Read Resource")
    print("="*50)
    request = {"jsonrpc": "2.0", "id": 2, "method": "resources/read", "params": {"uri": "weather://tokyo"}}
    response = server.handle_request(request)
    print(f"Request: {json.dumps(request, indent=2)}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    # Example 3: List tools
    print("\n" + "="*50)
    print("EXAMPLE 3: List Tools")
    print("="*50)
    request = {"jsonrpc": "2.0", "id": 3, "method": "tools/list"}
    response = server.handle_request(request)
    print(f"Request: {json.dumps(request, indent=2)}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    # Example 4: Call a tool
    print("\n" + "="*50)
    print("EXAMPLE 4: Call Weather Tool")
    print("="*50)
    request = {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_weather", "arguments": {"location": "New York"}}}
    response = server.handle_request(request)
    print(f"Request: {json.dumps(request, indent=2)}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    # Example 5: Get a prompt
    print("\n" + "="*50)
    print("EXAMPLE 5: Get Weather Report Prompt")
    print("="*50)
    request = {"jsonrpc": "2.0", "id": 5, "method": "prompts/get", "params": {"name": "weather_report", "arguments": {"location": "London"}}}
    response = server.handle_request(request)
    print(f"Request: {json.dumps(request, indent=2)}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    print("\n" + "="*50)
    print("MCP Server Demonstration Complete!")
    print("="*50)
    print("\nThis demonstrates the core MCP concepts:")
    print("1. Resources - Static data that can be read (weather data)")
    print("2. Tools - Functions that can be called (get_weather, get_weather_forecast)")
    print("3. Prompts - Templates for LLM interactions (weather_report, weather_comparison)")
    print("4. JSON-RPC communication - Standard protocol for client-server communication")

if __name__ == "__main__":
    main() 
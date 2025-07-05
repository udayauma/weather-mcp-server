#!/usr/bin/env python3
"""
Demo script for the Weather MCP Server

This script demonstrates the weather MCP server functionality
and shows how it can be used.
"""

import asyncio
import json
from weather_mcp_server import WeatherMCPServer

async def demo_weather_server():
    """Demonstrate the weather MCP server functionality"""
    print("🌦️  Weather MCP Server Demo")
    print("=" * 50)
    
    # Create server instance
    server = WeatherMCPServer()
    
    print("\n✅ Server initialized successfully!")
    print(f"   Server name: {server.server.name}")
    print(f"   Mock weather data for: {list(server.mock_weather_data.keys())}")
    
    # Test 1: Get Weather Tool
    print("\n🌤️  Testing Weather Tool...")
    try:
        weather_result = await server.get_weather("New York")
        print("✅ Weather tool response:")
        weather_data = json.loads(weather_result.content[0].text)
        print(f"   📍 Location: {weather_data['location']}")
        print(f"   🌡️  Temperature: {weather_data['temperature']}°")
        print(f"   ☁️  Conditions: {weather_data['conditions']}")
        print(f"   💨 Wind Speed: {weather_data['wind_speed']} mph")
        print(f"   💧 Humidity: {weather_data['humidity']}%")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Get Forecast Tool
    print("\n📊 Testing Forecast Tool...")
    try:
        forecast_result = await server.get_weather_forecast("London", 3)
        print("✅ Forecast tool response:")
        forecast_data = json.loads(forecast_result.content[0].text)
        print(f"   📍 Location: {forecast_data['location']}")
        print(f"   📅 Forecast for {forecast_data['forecast_days']} days:")
        for day in forecast_data['forecast']:
            print(f"     {day['date']}: {day['temperature']}°, {day['conditions']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Test different locations
    print("\n🗺️  Testing Different Locations...")
    locations = ["Tokyo", "Paris", "Sydney", "Unknown City"]
    
    for location in locations:
        try:
            weather_result = await server.get_weather(location)
            weather_data = json.loads(weather_result.content[0].text)
            print(f"   📍 {location}: {weather_data['temperature']}°, {weather_data['conditions']}")
        except Exception as e:
            print(f"   ❌ {location}: Error - {e}")
    
    # Test 4: Show server capabilities
    print("\n🔧 MCP Server Capabilities:")
    print(f"   ✅ Resources: Available")
    print(f"   ✅ Tools: Available") 
    print(f"   ✅ Prompts: Available")
    print(f"   ✅ Logging: Available")
    
    print("\n📋 Available Resources:")
    for city_key, data in server.mock_weather_data.items():
        print(f"   🌍 weather://{city_key} - {data['location']}")
    
    print("\n🔧 Available Tools:")
    print("   🌤️  get_weather(location) - Get current weather")
    print("   📊 get_weather_forecast(location, days) - Get forecast")
    
    print("\n📝 Available Prompts:")
    print("   📄 weather_report(location) - Generate weather report")
    print("   📊 weather_comparison(location1, location2) - Compare weather")
    
    print("\n" + "=" * 50)
    print("🎉 Demo Complete!")
    print("=" * 50)
    
    print(f"""
🚀 Your MCP Server is Ready!

📖 How to use:
1. The server implements the Model Context Protocol
2. It provides weather data through Resources, Tools, and Prompts
3. Use the mcp_config.json file to configure MCP clients
4. The server communicates via JSON-RPC over stdin/stdout

🔗 Integration Examples:
- Claude Desktop: Add to your MCP configuration
- VS Code: Use with MCP-compatible extensions
- Custom clients: Connect via JSON-RPC protocol

📁 Files created:
- weather_mcp_server.py (main server)
- mcp_config.json (client configuration)
- requirements.txt (dependencies)
- README.md (documentation)

🌟 Next Steps:
1. Configure your MCP client with mcp_config.json
2. Replace mock data with real weather API calls
3. Add more cities and weather features
4. Extend with additional tools and prompts
""")

if __name__ == "__main__":
    asyncio.run(demo_weather_server()) 
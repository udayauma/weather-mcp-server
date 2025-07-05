#!/usr/bin/env python3
"""
Test script for the Weather MCP Server

This script demonstrates how to test the MCP server functionality
by simulating client requests and verifying responses.
"""

import asyncio
import json
from weather_mcp_server import WeatherMCPServer

async def test_weather_server():
    """Test the weather MCP server functionality"""
    print("Testing Weather MCP Server")
    print("=" * 40)
    
    # Create server instance
    server = WeatherMCPServer()
    
    # Test 1: List Resources
    print("\n[*] Testing Resources...")
    try:
        resources_result = await server.server._list_resources_handler()
        print(f"[OK] Found {len(resources_result.resources)} resources:")
        for resource in resources_result.resources:
            print(f"   - {resource.name} ({resource.uri})")
    except Exception as e:
        print(f"[ERROR] Error listing resources: {e}")
    
    # Test 2: List Tools
    print("\n[*] Testing Tools...")
    try:
        tools_result = await server.server._list_tools_handler()
        print(f"[OK] Found {len(tools_result.tools)} tools:")
        for tool in tools_result.tools:
            print(f"   - {tool.name}: {tool.description}")
    except Exception as e:
        print(f"[ERROR] Error listing tools: {e}")
    
    # Test 3: List Prompts
    print("\n[*] Testing Prompts...")
    try:
        prompts_result = await server.server._list_prompts_handler()
        print(f"[OK] Found {len(prompts_result.prompts)} prompts:")
        for prompt in prompts_result.prompts:
            print(f"   - {prompt.name}: {prompt.description}")
    except Exception as e:
        print(f"[ERROR] Error listing prompts: {e}")
    
    # Test 4: Call Weather Tool
    print("\n[*] Testing Weather Tool...")
    try:
        weather_result = await server.get_weather("New York")
        print("[OK] Weather tool response:")
        print(f"   {weather_result.content[0].text}")
    except Exception as e:
        print(f"[ERROR] Error calling weather tool: {e}")
    
    # Test 5: Call Forecast Tool
    print("\n[*] Testing Forecast Tool...")
    try:
        forecast_result = await server.get_weather_forecast("London", 3)
        print("[OK] Forecast tool response:")
        # Parse and display forecast data nicely
        forecast_data = json.loads(forecast_result.content[0].text)
        print(f"   Location: {forecast_data['location']}")
        print(f"   Forecast for {forecast_data['forecast_days']} days:")
        for day in forecast_data['forecast']:
            print(f"     {day['date']}: {day['temperature']}°, {day['conditions']}")
    except Exception as e:
        print(f"[ERROR] Error calling forecast tool: {e}")
    
    # Test 6: Read Resource
    print("\n[*] Testing Resource Reading...")
    try:
        resource_result = await server.server._read_resource_handler("weather://tokyo")
        print("[OK] Resource reading successful:")
        print(f"   {resource_result.contents[0].text}")
    except Exception as e:
        print(f"[ERROR] Error reading resource: {e}")
    
    # Test 7: Get Prompt
    print("\n[*] Testing Prompt Generation...")
    try:
        prompt_result = await server.server._get_prompt_handler("weather_report", {"location": "Tokyo"})
        print("[OK] Prompt generation successful:")
        print(f"   Description: {prompt_result.description}")
        print(f"   Content: {prompt_result.messages[0]['content']['text'][:100]}...")
    except Exception as e:
        print(f"[ERROR] Error generating prompt: {e}")
    
    print("\n[SUCCESS] Server testing completed!")
    print("=" * 40)

if __name__ == "__main__":
    asyncio.run(test_weather_server()) 
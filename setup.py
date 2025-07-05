#!/usr/bin/env python3
"""
Setup script for Weather MCP Server

This script helps you get started with the Weather MCP Server by:
1. Installing dependencies
2. Running tests
3. Providing usage examples
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n[*] {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[OK] {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("Weather MCP Server Setup")
    print("=" * 40)
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        print(f"[ERROR] Python 3.8+ required. Current version: {python_version.major}.{python_version.minor}")
        sys.exit(1)
    
    print(f"[OK] Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Install dependencies
    if not run_command("pip3 install -r requirements.txt", "Installing dependencies"):
        print("[ERROR] Failed to install dependencies. Please check your pip installation.")
        sys.exit(1)
    
    # Run tests
    if not run_command("python3 test_server.py", "Running server tests"):
        print("[ERROR] Server tests failed. Please check the error messages above.")
        sys.exit(1)
    
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        print("\n[*] Creating .env file...")
        with open(".env", "w") as f:
            f.write("WEATHER_API_KEY=demo_key\n")
            f.write("SERVER_NAME=weather-mcp-server\n")
            f.write("SERVER_VERSION=1.0.0\n")
            f.write("LOG_LEVEL=INFO\n")
        print("[OK] .env file created")
    
    # Success message
    print("\n[SUCCESS] Setup completed successfully!")
    print("=" * 40)
    print("\nNext steps:")
    print("1. Run the server: python weather_mcp_server.py")
    print("2. Test the server: python test_server.py")
    print("3. Check the README.md for more information")
    print("4. Use mcp_config.json to configure MCP clients")
    
    print("\nAvailable features:")
    print("- Weather resources for New York, London, Tokyo")
    print("- Tools: get_weather, get_weather_forecast")
    print("- Prompts: weather_report, weather_comparison")

if __name__ == "__main__":
    main() 
#!/bin/bash

# Get IP address of the machine using alternative methods
if command -v ip &> /dev/null; then
    IP_ADDRESS=$(ip -4 addr show | grep -oP '(?<=inet\s)[\d.]+' | grep -v "127.0.0.1" | head -n 1)
elif command -v ifconfig &> /dev/null; then
    IP_ADDRESS=$(ifconfig | grep -oP '(?<=inet\s)[\d.]+' | grep -v "127.0.0.1" | head -n 1)
else
    # Fallback to a simple method that might work on some systems
    IP_ADDRESS=$(ping -c 1 -t 1 google.com 2>/dev/null | grep -oP '(?<=from\s)[\d.]+' | head -n 1)
    # If that fails too, use a placeholder
    if [ -z "$IP_ADDRESS" ]; then
        IP_ADDRESS="YOUR_IP_ADDRESS"
    fi
fi

echo "Starting MkDocs server on http://$IP_ADDRESS:8001"
echo "Documentation will be available on your local network"
echo "Press Ctrl+C to stop the server"

# Check if in a virtual environment, if not, try to activate one
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d ".venv" ]; then
        echo "Activating virtual environment..."
        source .venv/bin/activate
    else
        echo "Warning: No virtual environment active. Make sure mkdocs and mkdocs-material are installed."
    fi
fi

# Check if mkdocs is installed
if ! command -v mkdocs &> /dev/null; then
    echo "Error: mkdocs is not installed or not in PATH"
    echo "Please install with: pip install mkdocs mkdocs-material"
    exit 1
fi

# Check if new directory structure exists
if [ ! -d "docs/getting-started" ] || [ ! -d "docs/tasks" ] || [ ! -d "docs/workflows" ]; then
    echo "Warning: Documentation structure appears incomplete."
    echo "Expected directories: docs/getting-started/, docs/tasks/, docs/workflows/"
fi

# Build the documentation first to catch any errors
echo "Building documentation..."
mkdocs build --clean

if [ $? -ne 0 ]; then
    echo "Error: Documentation build failed. Please fix errors and try again."
    exit 1
fi

echo "Build successful! Starting server..."

# Serve the documentation on all interfaces
mkdocs serve --dev-addr 0.0.0.0:8001

# Show a message when the server stops
echo "Server stopped"

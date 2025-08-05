#!/bin/bash

# Application Version Checker Installation Script
# This script sets up the environment and installs dependencies

set -e

echo "=========================================="
echo "Application Version Checker Installation"
echo "=========================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed. Please install pip first."
    echo "On Ubuntu/Debian: sudo apt install python3-pip"
    echo "On CentOS/RHEL/Fedora: sudo yum install python3-pip or sudo dnf install python3-pip"
    exit 1
fi

echo "✓ pip found"

# Function to install dependencies
install_dependencies() {
    echo "Installing Python dependencies..."
    
    # Try different installation methods
    if python3 -m pip install --user requests packaging 2>/dev/null; then
        echo "✓ Dependencies installed using pip --user"
        return 0
    elif pip3 install --user requests packaging 2>/dev/null; then
        echo "✓ Dependencies installed using pip3 --user"
        return 0
    elif python3 -m venv venv && source venv/bin/activate && pip install requests packaging; then
        echo "✓ Dependencies installed in virtual environment"
        echo "Note: Use 'source venv/bin/activate' before running the application"
        return 0
    else
        echo "Warning: Could not install dependencies with pip"
        echo "Trying system package manager..."
        
        # Try system package manager
        if command -v apt &> /dev/null; then
            echo "Attempting to install via apt..."
            if sudo apt update && sudo apt install -y python3-requests python3-packaging; then
                echo "✓ Dependencies installed via apt"
                return 0
            fi
        elif command -v yum &> /dev/null; then
            echo "Attempting to install via yum..."
            if sudo yum install -y python3-requests python3-packaging; then
                echo "✓ Dependencies installed via yum"
                return 0
            fi
        elif command -v dnf &> /dev/null; then
            echo "Attempting to install via dnf..."
            if sudo dnf install -y python3-requests python3-packaging; then
                echo "✓ Dependencies installed via dnf"
                return 0
            fi
        fi
        
        echo "Error: Could not install dependencies"
        echo "Please install manually:"
        echo "  pip install requests packaging"
        echo "or use your system package manager"
        return 1
    fi
}

# Make scripts executable
echo "Making scripts executable..."
chmod +x app_version_checker.py
chmod +x test_app.py
echo "✓ Scripts are now executable"

# Install dependencies
if install_dependencies; then
    echo ""
    echo "=========================================="
    echo "Installation completed successfully!"
    echo "=========================================="
    echo ""
    echo "Usage examples:"
    echo "  ./app_version_checker.py                    # Check all packages"
    echo "  ./app_version_checker.py --help             # Show help"
    echo "  ./app_version_checker.py --verbose          # Verbose output"
    echo "  ./app_version_checker.py --format json      # JSON output"
    echo "  ./app_version_checker.py --managers apt pip # Check specific managers"
    echo ""
    echo "Test the installation:"
    echo "  ./test_app.py                               # Run test suite"
    echo ""
    
    # Test if dependencies work
    if python3 -c "import requests, packaging" 2>/dev/null; then
        echo "✓ Dependencies are working correctly"
        echo ""
        echo "You can now run the application version checker!"
    else
        echo "⚠ Warning: Dependencies may not be properly installed"
        echo "Try running the test script first: ./test_app.py"
    fi
else
    echo ""
    echo "=========================================="
    echo "Installation incomplete"
    echo "=========================================="
    echo ""
    echo "The basic scripts are ready, but dependencies need to be installed manually."
    echo "You can still run the test script: ./test_app.py"
    echo ""
    echo "To install dependencies manually:"
    echo "  pip install requests packaging"
    echo ""
    exit 1
fi
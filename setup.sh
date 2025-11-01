#!/bin/bash
# FPL Optimizer Setup Script

echo "=================================="
echo "FPL Optimizer Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"
echo ""

# Create virtual environment (optional but recommended)
read -p "Create virtual environment? (recommended) [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Virtual environment created and activated!"
    echo ""
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Installation complete!"
    echo ""
    echo "=================================="
    echo "Quick Start"
    echo "=================================="
    echo ""
    echo "1. Find your FPL Team ID:"
    echo "   - Go to fantasy.premierleague.com"
    echo "   - Look at the URL: /entry/YOUR_TEAM_ID/"
    echo ""
    echo "2. Run your first analysis:"
    echo "   python main.py --team-id YOUR_TEAM_ID --all"
    echo ""
    echo "3. Or see examples:"
    echo "   python example_usage.py"
    echo ""
    echo "4. For more help:"
    echo "   python main.py --help"
    echo "   cat QUICK_START.md"
    echo ""
    echo "=================================="
    echo "Ready to optimize your FPL team!"
    echo "=================================="
    echo ""
else
    echo ""
    echo "✗ Installation failed!"
    echo "Please check the error messages above."
    exit 1
fi


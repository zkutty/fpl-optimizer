#!/bin/bash
# Deployment readiness check script

echo "🔍 Checking if your app is ready for deployment..."
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check counter
checks_passed=0
checks_failed=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        ((checks_passed++))
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing"
        ((checks_failed++))
        return 1
    fi
}

# Function to check if git is initialized
check_git() {
    if [ -d ".git" ]; then
        echo -e "${GREEN}✓${NC} Git repository initialized"
        ((checks_passed++))
    else
        echo -e "${YELLOW}!${NC} Git not initialized (run: git init)"
        ((checks_failed++))
    fi
}

# Check required files
echo "📋 Checking required files..."
check_file "app.py"
check_file "requirements.txt"
check_file "Procfile"
check_file "runtime.txt"
check_file ".gitignore"

echo ""
echo "🔧 Checking configuration files..."
check_file "render.yaml"
check_file "railway.json"

echo ""
echo "🐳 Checking Docker files (optional)..."
check_file "Dockerfile"
check_file "docker-compose.yml"
check_file ".dockerignore"

echo ""
echo "🔐 Checking Git setup..."
check_git

# Check if requirements.txt contains gunicorn
echo ""
echo "📦 Checking dependencies..."
if grep -q "gunicorn" requirements.txt; then
    echo -e "${GREEN}✓${NC} gunicorn in requirements.txt"
    ((checks_passed++))
else
    echo -e "${RED}✗${NC} gunicorn missing from requirements.txt"
    ((checks_failed++))
fi

# Check Python files for syntax errors
echo ""
echo "🐍 Checking Python syntax..."
if python3 -m py_compile app.py 2>/dev/null; then
    echo -e "${GREEN}✓${NC} app.py syntax is valid"
    ((checks_passed++))
else
    echo -e "${RED}✗${NC} app.py has syntax errors"
    ((checks_failed++))
fi

# Check if PORT is used in app.py
echo ""
echo "🌐 Checking port configuration..."
if grep -q "PORT" app.py; then
    echo -e "${GREEN}✓${NC} Port configuration found"
    ((checks_passed++))
else
    echo -e "${YELLOW}!${NC} PORT environment variable not used (might cause issues)"
fi

# Summary
echo ""
echo "================================"
echo "📊 Results:"
echo -e "${GREEN}Passed: $checks_passed${NC}"
echo -e "${RED}Failed: $checks_failed${NC}"
echo "================================"
echo ""

if [ $checks_failed -eq 0 ]; then
    echo -e "${GREEN}✅ Your app is ready for deployment!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. git add ."
    echo "2. git commit -m 'Ready for deployment'"
    echo "3. git push origin main"
    echo "4. Follow DEPLOY_RENDER.md for deployment"
    exit 0
else
    echo -e "${RED}⚠️  Please fix the issues above before deploying${NC}"
    echo ""
    echo "Need help? Check DEPLOYMENT.md for troubleshooting"
    exit 1
fi


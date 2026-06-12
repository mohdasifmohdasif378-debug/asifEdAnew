#!/bin/bash

# AsifEdA - Quick Deployment Script
# This script sets up and runs the competitive exam AI system

set -e

echo "🎓 AsifEdA - Competitive Exam AI Brain"
echo "========================================"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not installed."
    exit 1
fi

echo "✅ Docker is installed"
echo ""

# Check for API key
echo "🔑 API Key Setup (Optional but Recommended)"
echo "==========================================="
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo ""
    echo "⚠️  No ANTHROPIC_API_KEY found"
    echo "Without API key: AI uses local fallback (limited responses)"
    echo "With API key: Full Claude Haiku AI power for exam questions"
    echo ""
    read -p "Enter your Anthropic API key (or press Enter to skip): " api_key
    if [ ! -z "$api_key" ]; then
        export ANTHROPIC_API_KEY=$api_key
        echo "✅ API key set!"
    fi
else
    echo "✅ ANTHROPIC_API_KEY already configured"
fi

echo ""
echo "🔐 Security Setup"
echo "================="
if [ ! -f ".env" ]; then
    echo "Creating .env file with random secret..."
    SECRET=$(openssl rand -hex 32 2>/dev/null || python3 -c "import secrets; print(secrets.token_hex(16))")
    cat > .env << EOF
SECRET_KEY=$SECRET
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
FRONTEND_ORIGINS=http://localhost:3001,http://127.0.0.1:3001,http://localhost:8001,http://127.0.0.1:8001
DATABASE_URL=sqlite:///./data/asifeda.db
EOF
    echo "✅ .env created with secure settings"
else
    echo "✅ .env already exists"
fi

echo ""
echo "🐳 Building and Starting Containers"
echo "===================================="
docker-compose build --no-cache 2>&1 | tail -5
echo ""
docker-compose up -d

# Wait for services
echo ""
echo "⏳ Waiting for services to start..."
sleep 5

# Check health
echo ""
echo "🏥 Health Check"
echo "==============="
if curl -s http://localhost:8001/api/health | grep -q "healthy"; then
    echo "✅ Backend is healthy"
else
    echo "⚠️  Backend might still be starting..."
fi

echo ""
echo "✨ Deployment Complete!"
echo "======================="
echo ""
echo "🌐 Access Points:"
echo "   Frontend:  http://localhost:3001"
echo "   Backend:   http://localhost:8001/api"
echo "   Health:    http://localhost:8001/api/health"
echo ""
echo "📱 From other devices:"
echo "   Get your IP: hostname -I"
echo "   Then use: http://<YOUR_IP>:3001"
echo ""
echo "📚 First Steps:"
echo "   1. Open http://localhost:3001"
echo "   2. Register/Login"
echo "   3. Ask about: UPSC, SSC, NDA, or Banking"
echo ""
echo "📖 For more info, see: DEPLOYMENT_GUIDE.md"
echo ""
echo "🛑 To stop: docker-compose down"
echo "🔄 To restart: docker-compose restart"
echo ""

#!/bin/bash
# Rebuild Full Development Environment (Mac/Linux)

echo "================================"
echo "Rebuilding Jobstock Full Dev Environment"
echo "================================"
echo ""
echo "This will:"
echo "  1. Stop current container"
echo "  2. Rebuild Docker image"
echo "  3. Start fresh container"
echo ""
echo "Use this when:"
echo "  - You updated requirements.txt"
echo "  - You need to install new Python packages"
echo ""
read -p "Continue? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "🛑 Stopping current container..."
docker-compose -f docker-compose.fulldev.yml down

echo ""
echo "🔨 Rebuilding Docker image (this may take 2-3 minutes)..."
docker-compose -f docker-compose.fulldev.yml build --no-cache

echo ""
echo "🚀 Starting fresh container..."
docker-compose -f docker-compose.fulldev.yml up -d

if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "✅ Rebuild Complete!"
    echo "================================"
    echo ""
    echo "🌐 Server running at: http://localhost:8000"
else
    echo ""
    echo "❌ Error during rebuild"
    echo "Run './logs_fulldev.sh' to see error details"
    exit 1
fi

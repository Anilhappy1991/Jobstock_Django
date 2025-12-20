#!/bin/bash
# Start Full Development Environment (Mac/Linux)

echo "================================"
echo "Starting Jobstock Full Dev Environment"
echo "================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running!"
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""
echo "🔨 Building and starting container..."
echo "   First time: 2-3 minutes"
echo "   Subsequent starts: 5-10 seconds"
echo ""

# Build and start container
docker-compose -f docker-compose.fulldev.yml up --build -d

if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "✅ Server Started Successfully!"
    echo "================================"
    echo ""
    echo "🌐 Access at: http://localhost:8000"
    echo ""
    echo "📝 To stop server:"
    echo "   ./stop_fulldev.sh"
    echo ""
    echo "📋 To view logs:"
    echo "   ./logs_fulldev.sh"
    echo ""
    echo "Opening browser in 3 seconds..."
    sleep 3
    
    # Open browser based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac
        open http://localhost:8000
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        xdg-open http://localhost:8000 2>/dev/null || echo "Please open: http://localhost:8000"
    fi
else
    echo ""
    echo "❌ Error: Failed to start server"
    echo "Run './logs_fulldev.sh' to see error details"
    exit 1
fi

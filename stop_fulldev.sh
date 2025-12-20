#!/bin/bash
# Stop Full Development Environment (Mac/Linux)

echo "Stopping Jobstock Full Dev Environment..."
docker-compose -f docker-compose.fulldev.yml down

if [ $? -eq 0 ]; then
    echo "✅ Server stopped successfully!"
else
    echo "❌ Error stopping server"
    exit 1
fi

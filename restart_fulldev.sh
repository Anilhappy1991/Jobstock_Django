#!/bin/bash
# Restart Full Development Environment (Mac/Linux)

echo "Restarting Jobstock Full Dev Environment..."
docker-compose -f docker-compose.fulldev.yml restart

if [ $? -eq 0 ]; then
    echo "✅ Server restarted successfully!"
    echo "🌐 Access at: http://localhost:8000"
else
    echo "❌ Error restarting server"
    exit 1
fi

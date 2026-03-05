#!/bin/bash

# Start PersonAI in GitHub Codespaces

echo "🚀 Starting PersonAI..."

# Check if .env exists, if not create from example
if [ ! -f .env ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your API keys!"
fi

# Start backend
echo "🔧 Starting backend on port 8080..."
python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend on port 5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ PersonAI is running!"
echo ""
echo "📍 Backend API: Port 8080 (forwarded)"
echo "📍 Frontend: Port 5173 (forwarded)"
echo ""
echo "🔗 GitHub will automatically forward these ports"
echo "   Click the 'Ports' tab to see the URLs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait

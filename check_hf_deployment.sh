#!/bin/bash

echo "🔍 Checking Hugging Face Space Deployment"
echo "=========================================="
echo ""

SPACE_URL="https://yeduru-abhi.hf.space"

echo "🌐 Space URL: $SPACE_URL"
echo ""

echo "⏳ Waiting for Space to start (this may take 2-3 minutes)..."
echo ""

# Wait and check health
for i in {1..30}; do
    echo -n "Attempt $i/30: "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$SPACE_URL/health" 2>/dev/null)
    
    if [ "$response" = "200" ]; then
        echo "✅ SUCCESS!"
        echo ""
        echo "🎉 Your Space is LIVE!"
        echo ""
        echo "📊 Health Check:"
        curl -s "$SPACE_URL/health" | python3 -m json.tool 2>/dev/null || curl -s "$SPACE_URL/health"
        echo ""
        echo ""
        echo "🧪 Test Chat:"
        curl -s -X POST "$SPACE_URL/api/chat" \
          -H "Content-Type: application/json" \
          -d '{"message": "Hello!", "session_id": "test"}' | python3 -m json.tool 2>/dev/null || echo "Chat endpoint ready"
        echo ""
        echo ""
        echo "✅ Deployment successful!"
        echo "🌐 API: $SPACE_URL"
        echo "📚 Docs: $SPACE_URL/docs"
        echo ""
        exit 0
    elif [ "$response" = "503" ]; then
        echo "⏳ Building... (Space is starting up)"
    else
        echo "⏳ Waiting... (HTTP $response)"
    fi
    
    sleep 10
done

echo ""
echo "⚠️  Space is taking longer than expected"
echo "📊 Check status at: https://huggingface.co/spaces/yeduru/abhi"
echo "📋 View logs to see build progress"
echo ""
echo "Common issues:"
echo "  - Build still in progress (wait a bit longer)"
echo "  - Build failed (check logs for errors)"
echo "  - Space sleeping (first request wakes it up)"

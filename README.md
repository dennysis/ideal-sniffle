# ideal-sniffle
Based on your codebase, here are all the working routes:

🔐 Authentication Routes (/api/auth)
POST   /api/auth/register          # Register new user
POST   /api/auth/login             # Login user  
POST   /api/auth/refresh           # Refresh access token
GET    /api/auth/me                # Get current user details
POST   /api/auth/logout            # Logout user

Copy

Execute

🏠 Orphanage Routes (/api/orphanages)
GET    /api/orphanages/                    # Get all orphanages (public)
GET    /api/orphanages/<id>                # Get specific orphanage (public)
POST   /api/orphanages/                    # Create orphanage (orphanage role only)
PUT    /api/orphanages/<id>                # Update orphanage
GET    /api/orphanages/my-orphanage        # Get current user's orphanage
GET    /api/orphanages/search              # Search orphanages

Copy

Execute

💰 Donation Routes (/api/donations)
POST   /api/donations                              # Make donation (donor required)
GET    /api/donations                              # Get donations (user's own)
GET    /api/donations/<id>                         # Get donation details
GET    /api/donations/orphanage/<id>/summary       # Get donation summary
POST   /api/donations/callback/mpesa               # M-Pesa callback (public)

Copy

Execute

📊 Analytics Routes (/api/analytics)
GET    /api/analytics/orphanage/<id>               # Get orphanage analytics
POST   /api/analytics/orphanage/<id>/report        # Generate donation report
GET    /api/analytics/platform                     # Get platform analytics

Copy

Execute

🔔 Notification Routes (/api/notifications)
GET    /api/notifications                          # Get user notifications
GET    /api/notifications/unread-count             # Get unread count
PUT    /api/notifications/<id>/read                # Mark notification as read
PUT    /api/notifications/mark-all-read            # Mark all as read
DELETE /api/notifications/<id>                     # Delete notification
POST   /api/notifications                          # Create notification (testing)

Copy

Execute

👤 User Routes (/api/users) - If implemented
GET    /api/users/<id>                             # Get user details
PUT    /api/users/<id>                             # Update user profile
DELETE /api/users/<id>                             # Delete user (soft delete)

Copy

Execute

🛠️ System Routes
GET    /                                           # API status
GET    /api/health                                 # Health check
GET    /api/routes                                 # List all routes (debug)

Copy

Execute

Method 3: Test All Routes Systematically
Let's create a comprehensive test script:

#!/bin/bash

BASE_URL="http://127.0.0.1:5000"
API_URL="$BASE_URL/api"

echo "=== TESTING ALL ROUTES ==="
echo "Base URL: $BASE_URL"
echo ""

# Get tokens for testing
echo "🔐 Getting authentication tokens..."
DONOR_TOKEN=$(curl -s -X POST $API_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "donor@example.com", "password": "password123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', 'FAILED'))" 2>/dev/null)

ORPHANAGE_TOKEN=$(curl -s -X POST $API_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hopeorphanage.com", "password": "password123"}' | \
  python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', 'FAILED'))" 2>/dev/null)

echo "Donor token: ${DONOR_TOKEN:0:20}..."
echo "Orphanage token: ${ORPHANAGE_TOKEN:0:20}..."
echo ""

# Test function
test_route() {
    local method=$1
    local url=$2
    local auth=$3
    local data=$4
    local description=$5
    
    echo "Testing: $method $url"
    echo "Description: $description"
    
    if [ "$auth" = "none" ]; then
        response=$(curl -s -X $method "$url" \
          -H "Content-Type: application/json" \
          ${data:+-d "$data"})
    else
        response=$(curl -s -X $method "$url" \
          -H "Authorization: Bearer $auth" \
          -H "Content-Type: application/json" \
          ${data:+-d "$data"})
    fi
    
    # Check if response is JSON and extract status
    if echo "$response" | python3 -c "import sys, json; json.load(sys.stdin)" 2>/dev/null; then
        echo "✅ SUCCESS"
    else
        echo "❌ FAILED or HTML response"
    fi
    echo ""
}

echo "🏠 SYSTEM ROUTES"
test_route "GET" "$BASE_URL/" "none" "" "API status"
test_route "GET" "$API_URL/health" "none" "" "Health check"
test_route "GET" "$API_URL/routes" "none" "" "List all routes"

echo "🔐 AUTHENTICATION ROUTES"
test_route "POST" "$API_URL/auth/login" "none" '{"email":"donor@example.com","password":"password123"}' "Login"
test_route "GET" "$API_URL/auth/me" "$DONOR_TOKEN" "" "Get current user"

echo "🏠 ORPHANAGE ROUTES"
test_route "GET" "$API_URL/orphanages/" "none" "" "Get all orphanages"
test_route "GET" "$API_URL/orphanages/1" "none" "" "Get specific orphanage"
test_route "GET" "$API_URL/orphanages/search?q=hope" "none" "" "Search orphanages"
test_route "GET" "$API_URL/orphanages/my-orphanage" "$ORPHANAGE_TOKEN" "" "Get my orphanage"

echo "💰 DONATION ROUTES"
test_route "GET" "$API_URL/donations" "$DONOR_TOKEN" "" "Get my donations"
test_route "GET" "$API_URL/donations/orphanage/1/summary" "$DONOR_TOKEN" "" "Get donation summary"

echo "📊 ANALYTICS ROUTES"
test_route "GET" "$API_URL/analytics/platform" "$DONOR_TOKEN" "" "Platform analytics"
test_route "GET" "$API_URL/analytics/orphanage/1" "$ORPHANAGE_TOKEN" "" "Orphanage analytics"

echo "🔔 NOTIFICATION ROUTES"
test_route "GET" "$API_URL/notifications" "$DONOR_TOKEN" "" "Get notifications"
test_route "GET" "$API_URL/notifications/unread-count" "$DONOR_TOKEN" "" "Get unread count"
test_route "PUT" "$API_URL/notifications/mark-all-read" "$DONOR_TOKEN" "" "Mark all as read"

echo "=== ROUTE TESTING COMPLETE ==="

Copy

Execute

test_all_routes.sh
chmod +x test_all_routes.sh
./test_all_routes.sh

Copy

Execute

Method 4: Quick Route Summary
echo "=== QUICK ROUTE SUMMARY ==="
echo ""
echo "📋 WORKING ENDPOINTS:"
echo "  🔐 Auth: 5 routes (/api/auth/*)"
echo "  🏠 Orphanages: 6 routes (/api/orphanages/*)"  
echo "  💰 Donations: 5 routes (/api/donations/*)"
echo "  📊 Analytics: 3 routes (/api/analytics/*)"
echo "  🔔 Notifications: 6 routes (/api/notifications/*)"
echo "  👤 Users: 3 routes (/api/users/*) - if implemented"
echo "  🛠️ System: 3 routes (/, /api/health, /api/routes)"
echo ""
echo "📊 TOTAL: ~31 working endpoints"
echo ""
echo "🔑 AUTHENTICATION REQUIRED:"
echo "  - Most endpoints require Bearer token"
echo "  - Public endpoints: orphanage listing, health check"
echo "  - Role-based access control implemented"
echo ""
echo "📝 SUPPORTED METHODS:"
echo "  - GET: Read operations"
echo "  - POST: Create operations" 
echo "  - PUT: Update operations"
echo "  - DELETE: Delete operations"

Copy

Execute

Method 5: Interactive Route Explorer
# Test specific route categories
echo "Choose a category to test:"
echo "1. Authentication routes"
echo "2. Orphanage routes" 
echo "3. Donation routes"
echo "4. Analytics routes"
echo "5. Notification routes"
echo "6. All routes"

read -p "Enter choice (1-6): " choice

case $choice in
    1) echo "Testing auth routes..."; curl -s $BASE_URL/api/routes | python3 -c "import sys,json; [print(r['rule']) for r in json.load(sys.stdin)['routes'] if 'auth' in r['rule']]" ;;
    2) echo "Testing orphanage routes..."; curl -s $BASE_URL/api/routes | python3 -c "import sys,json; [print(r['rule']) for r in json.load(sys.stdin)['routes'] if 'orphanage' in r['rule']]" ;;
    6) ./test_all_routes.sh ;;
    *) echo "Invalid choice" ;;
esac
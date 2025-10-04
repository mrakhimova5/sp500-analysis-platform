#!/bin/bash

# 🔄 Update Frontend API URL for Render Deployment
# Run this script after you deploy to Render and get your app URL

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     Update Frontend URL for Render Deployment           ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Prompt for Render URL
echo "📋 After deploying to Render, you'll get a URL like:"
echo "   https://sp500-analysis.onrender.com"
echo ""
read -p "🌐 Enter your Render app URL (without trailing slash): " RENDER_URL

# Validate URL
if [[ ! $RENDER_URL =~ ^https:// ]]; then
    echo "❌ Error: URL must start with https://"
    exit 1
fi

# Remove trailing slash if present
RENDER_URL="${RENDER_URL%/}"

echo ""
echo "🔍 Current URL in frontend.html:"
grep "const API_URL" frontend.html

echo ""
echo "📝 Updating to: $RENDER_URL"

# Create backup
cp frontend.html frontend.html.backup
echo "✅ Backup created: frontend.html.backup"

# Update the URL using sed (macOS compatible)
sed -i '' "s|const API_URL = '.*';|const API_URL = '$RENDER_URL';|g" frontend.html

echo ""
echo "🔍 New URL in frontend.html:"
grep "const API_URL" frontend.html

echo ""
echo "✅ Frontend URL updated successfully!"
echo ""
echo "📤 Next steps:"
echo "   1. Review the change:"
echo "      git diff frontend.html"
echo ""
echo "   2. Commit and push:"
echo "      git add frontend.html"
echo "      git commit -m \"Update API URL to Render\""
echo "      git push origin main"
echo ""
echo "   3. Wait 1-2 minutes for Render to auto-deploy"
echo ""
echo "   4. Test your app at: $RENDER_URL"
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  🎉 Deployment Complete! Your app is live for FREE!      ║"
echo "╚══════════════════════════════════════════════════════════╝"

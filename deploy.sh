#!/bin/bash
# MoKangMedical Homepage Deploy Script
# Usage: ./deploy.sh
# 
# What it does:
# 1. Runs build.py to generate index.html from data.json + github_stats.json
# 2. Uploads index.html to GitHub via API (bypasses git push proxy issues)
#
# To add/update projects:
#   1. Edit data.json (add project to the right segment's "projects" array)
#   2. Run: python3 build.py
#   3. Run: ./deploy.sh
#
# To refresh GitHub stats:
#   Run: python3 fetch_stats.py

set -e
cd "$(dirname "$0")"

echo "=== MoKangMedical Homepage Deploy ==="
echo ""

# Step 1: Build
echo "[1/2] Building index.html..."
python3 build.py
echo ""

# Step 2: Deploy via GitHub API
echo "[2/2] Deploying to GitHub Pages..."
python3 deploy_api.py
echo ""

echo "=== Done! ==="
echo "Live at: https://mokangmedical.github.io/opc-homepage/"

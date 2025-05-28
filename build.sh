#!/bin/bash

# Print status message
echo "Starting Personal Health Assistant project build..."

# Build frontend
echo "========== Building Frontend Application =========="
cd frontier-app
npm install
npm run build
cd ..
echo "Frontend build completed!"

# Build backend
echo "========== Building Backend Application =========="
pip install -r requirements.txt wheel
echo "Backend dependencies installed!"

# Copy built frontend files to backend static directory
echo "========== Integrating Frontend and Backend =========="
mkdir -p backapp/static
cp -r frontier-app/dist/* backapp/static/
echo "Frontend static files copied to backend static directory"

# Build wheel package
echo "========== Building Backend Wheel Package =========="
python setup.py bdist_wheel
echo "Backend wheel package built successfully! Available in dist/ directory"

echo "Build completed! 🎉"
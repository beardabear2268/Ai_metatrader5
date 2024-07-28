#!/bin/bash

# Step 1: Create and activate a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 2: Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Compile the C++ files into shared libraries
echo "Compiling C++ files..."
g++ -shared -fPIC -o src/libtrade_execution.so src/trade_execution.cpp
g++ -shared -fPIC -o src/libindicators.so src/indicators.cpp

# Step 4: Install Julia dependencies
echo "Installing Julia dependencies..."
julia -e 'using Pkg; Pkg.add(["CSV", "DataFrames", "ScikitLearn", "Random"])'

# Step 5: Install Go dependencies
echo "Installing Go dependencies..."
go get -u gonum.org/v1/gonum/...

# Step 6: Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install @tensorflow/tfjs-node csv-parser

echo "Setup complete."

# Deactivate virtual environment
deactivate
#!/bin/bash

# Compile the C++ files into shared libraries
g++ -shared -o src/libtrade_execution.so src/trade_execution.cpp -fPIC
g++ -shared -o src/libindicators.so src/indicators.cpp -fPIC

echo "Compilation complete."
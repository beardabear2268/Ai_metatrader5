#!/bin/bash

# Compile the C++ files
g++ -shared -o src/libtrade_execution.so src/trade_execution.cpp
g++ -shared -o src/libindicators.so src/indicators.cpp

echo "Compilation complete."
#include "trade_execution.h"
#include <iostream>
#include <cstdlib>

TradeExecution::TradeExecution() {}

double TradeExecution::simulate_trade(double lot_size, const std::string& symbol, double price, double stop_loss, double take_profit) {
    // Simulated profit calculation logic
    double profit = (rand() % 20 - 10); // Random profit between -10 and +10
    return profit;
}

void TradeExecution::execute_trade(const std::string& symbol, double lot_size, double price, double stop_loss, double take_profit) {
    double profit = simulate_trade(lot_size, symbol, price, stop_loss, take_profit);
    TradeResult result = {profit, "Trade executed", symbol, lot_size, price};
    trade_results.push_back(result);
}

void TradeExecution::log_trade_results() {
    for (const auto& result : trade_results) {
        std::cout << "Symbol: " << result.symbol << ", Profit: " << result.profit
                  << ", Lot Size: " << result.lot_size << ", Price: " << result.price
                  << ", Comment: " << result.comment << std::endl;
    }
}
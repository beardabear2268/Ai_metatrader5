#ifndef TRADE_EXECUTION_H
#define TRADE_EXECUTION_H

#include <string>
#include <vector>

struct TradeResult {
    double profit;
    std::string comment;
    std::string symbol;
    double lot_size;
    double price;
};

class TradeExecution {
public:
    TradeExecution();
    void execute_trade(const std::string& symbol, double lot_size, double price, double stop_loss, double take_profit);
    void log_trade_results();

private:
    std::vector<TradeResult> trade_results;
    double simulate_trade(double lot_size, const std::string& symbol, double price, double stop_loss, double take_profit);
};

#endif // TRADE_EXECUTION_H
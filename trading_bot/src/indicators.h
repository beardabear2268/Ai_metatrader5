#ifndef INDICATORS_H
#define INDICATORS_H

#include <vector>

class Indicators {
public:
    Indicators();
    double calculate_sma(const std::vector<double>& prices, int period);
    double calculate_ema(const std::vector<double>& prices, int period);
    double calculate_rsi(const std::vector<double>& prices, int period);

private:
    double calculate_sma_tail(const std::vector<double>& prices, int start, int end);
};

#endif // INDICATORS_H
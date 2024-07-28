#include "indicators.h"
#include <numeric>
#include <algorithm>

Indicators::Indicators() {}

double Indicators::calculate_sma(const std::vector<double>& prices, int period) {
    if (prices.size() < period) return 0.0;
    double sum = std::accumulate(prices.end() - period, prices.end(), 0.0);
    return sum / period;
}

double Indicators::calculate_ema(const std::vector<double>& prices, int period) {
    if (prices.size() < period) return 0.0;
    // Exponential Moving Average (EMA) calculation
    double k = 2.0 / (period + 1);
    double ema = prices[0];
    for (size_t i = 1; i < prices.size(); ++i) {
        ema = prices[i] * k + ema * (1 - k);
    }
    return ema;
}

double Indicators::calculate_rsi(const std::vector<double>& prices, int period) {
    if (prices.size() < period) return 0.0;
    std::vector<double> gains, losses;
    for (size_t i = 1; i < prices.size(); ++i) {
        double change = prices[i] - prices[i - 1];
        if (change > 0) {
            gains.push_back(change);
            losses.push_back(0.0);
        } else {
            gains.push_back(0.0);
            losses.push_back(-change);
        }
    }

    double avg_gain = calculate_sma_tail(gains, 0, period);
    double avg_loss = calculate_sma_tail(losses, 0, period);
    if (avg_loss == 0) return 100.0;
    double rs = avg_gain / avg_loss;
    return 100 - (100 / (1 + rs));
}

double Indicators::calculate_sma_tail(const std::vector<double>& prices, int start, int end) {
    double sum = std::accumulate(prices.begin() + start, prices.begin() + end, 0.0);
    return sum / (end - start);
}
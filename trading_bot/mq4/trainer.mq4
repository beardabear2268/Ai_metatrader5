//+------------------------------------------------------------------+
//|                                                     trainer.mq4  |
//|                   Copyright 2023, MetaQuotes Software Corp.      |
//|                                       https://www.metaquotes.net |
//+------------------------------------------------------------------+
#property strict

// Input parameters
input int FastEMA = 12;
input int SlowEMA = 26;
input double InitialBalance = 10000.0;

// Global variables
int fastEmaHandle, slowEmaHandle;
double previousFastEMA, previousSlowEMA;
double balance;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- Create handles for the EMA indicators
   fastEmaHandle = iMA(_Symbol, PERIOD_M15, FastEMA, 0, MODE_EMA, PRICE_CLOSE);
   slowEmaHandle = iMA(_Symbol, PERIOD_M15, SlowEMA, 0, MODE_EMA, PRICE_CLOSE);
   
   if (fastEmaHandle < 0 || slowEmaHandle < 0)
     {
      Print("Failed to create indicator handles");
      return INIT_FAILED;
     }

//--- Initial balance for backtesting
   balance = InitialBalance;

//--- Copy the initial values of the EMAs
   previousFastEMA = iCustom(NULL, 0, "fastEmaHandle", 0, 1);
   previousSlowEMA = iCustom(NULL, 0, "slowEmaHandle", 0, 1);

//--- Expert initialization done
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   IndicatorRelease(fastEmaHandle);
   IndicatorRelease(slowEmaHandle);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   // Retrieve the current EMA values
   double currentFastEMA = iCustom(NULL, 0, "fastEmaHandle", 0, 0);
   double currentSlowEMA = iCustom(NULL, 0, "slowEmaHandle", 0, 0);

//--- Trading logic: EMA crossover (fast above slow -> buy, fast below slow -> sell)
   static double openPrice = 0.0;
   if (previousFastEMA < previousSlowEMA && currentFastEMA > currentSlowEMA)
     {
      if (openPrice == 0) // No open position
        {
         openPrice = Ask;
         balance -= Ask * 0.1; // Example cost of buying 0.1 lots
         Print("Simulated BUY order at ", Ask);
        }
     }
   else if (previousFastEMA > previousSlowEMA && currentFastEMA < currentSlowEMA)
     {
      if (openPrice > 0) // Close position
        {
         balance += Bid * 0.1; // Example revenue of selling 0.1 lots
         Print("Simulated SELL order at ", Bid);
         openPrice = 0;
        }
     }

//--- Update previous EMA values
   previousFastEMA = currentFastEMA;
   previousSlowEMA = currentSlowEMA;
  }

//+------------------------------------------------------------------+


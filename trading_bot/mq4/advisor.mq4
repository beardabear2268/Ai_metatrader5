//+------------------------------------------------------------------+
//|                                                      advisor.mq4  |
//|                   Copyright 2023, MetaQuotes Software Corp.      |
//|                                       https://www.metaquotes.net |
//+------------------------------------------------------------------+
#property strict

// Input parameters
input int FastEMA = 12;
input int SlowEMA = 26;
input double LotSize = 0.1;

// Global variables
int fastEmaHandle, slowEmaHandle;
double previousFastEMA, previousSlowEMA;

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

//--- Copy the initial values of the EMAs
   previousFastEMA = iCustom(NULL, 0, "fastEmaHandle", 0, 1);
   previousSlowEMA = iCustom(NULL, 0, "slowEmaHandle", 0, 1);

//--- Set timer to check trading conditions on every new bar
   EventSetTimer(60);

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
   EventKillTimer();
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   // No trading on tick events, use timer
  }
//+------------------------------------------------------------------+
//| Timer event function                                             |
//+------------------------------------------------------------------+
void OnTimer()
  {
   // Retrieve the current EMA values
   double currentFastEMA = iCustom(NULL, 0, "fastEmaHandle", 0, 0);
   double currentSlowEMA = iCustom(NULL, 0, "slowEmaHandle", 0, 0);

//--- Trading logic: EMA crossover (fast above slow -> buy, fast below slow -> sell)
   if (previousFastEMA < previousSlowEMA && currentFastEMA > currentSlowEMA)
     {
      if (OrderSelect(0, SELECT_BY_POS) && OrderType()==OP_SELL) 
        {
         CloseOrder(OrderTicket());
        }
      OpenOrder(OP_BUY);
     }
   else if (previousFastEMA > previousSlowEMA && currentFastEMA < currentSlowEMA)
     {
      if (OrderSelect(0, SELECT_BY_POS) && OrderType()==OP_BUY) 
        {
         CloseOrder(OrderTicket());
        }
      OpenOrder(OP_SELL);
     }

//--- Update previous EMA values
   previousFastEMA = currentFastEMA;
   previousSlowEMA = currentSlowEMA;
  }
//+------------------------------------------------------------------+
//| Function to open orders                                          |
//+------------------------------------------------------------------+
bool OpenOrder(int orderType)
  {
   double ask = MarketInfo(_Symbol, MODE_ASK);
   double bid = MarketInfo(_Symbol, MODE_BID);
   double price = orderType == OP_BUY ? ask : bid;
   double sl = orderType == OP_BUY ? price - 200 * Point : price + 200 * Point;
   double tp = orderType == OP_BUY ? price + 200 * Point : price - 200 * Point;

   int order = OrderSend(
                 _Symbol,               // symbol
                 orderType,             // Buy or Sell
                 LotSize,               // Lot size
                 price,                 // Opening price
                 2,                     // Slippage (in points)
                 sl,                    // Stop loss price
                 tp,                    // Take profit price
                 "",                    // Order comment
                 MAGIC_NUMBER,          // Magic number
                 0,                     // Order expiration
                 clrNONE);              // Arrow color

   if(order < 0)
     {
      Print("Order failed to send with error code:", GetLastError());
      return false;
     }
   
   Print("Order successfully opened with ticket #", order);
   return true;
  }
//+------------------------------------------------------------------+
//| Function to close orders                                         |
//+------------------------------------------------------------------+
bool CloseOrder(int orderTicket)
  {
   double closePrice = OrderType() == OP_BUY ? Bid : Ask;

   while(OrderClose(orderTicket, OrderLots(), closePrice, 2, clrNONE) == false)
     {
      Print("Order close failed with error code: ", GetLastError(), ". Trying again...");
     }
   
   Print("Order successfully closed with ticket #", orderTicket);
   return true;
  }
//+------------------------------------------------------------------+

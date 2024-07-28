//+------------------------------------------------------------------+
//|                                                 data_parser.mq4  |
//|                   Copyright 2023, MetaQuotes Software Corp.      |
//|                                       https://www.metaquotes.net |
//+------------------------------------------------------------------+
#property strict

// Input parameters
extern string OutputFile = "TradeData.csv";

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- Open the output file
   int fileHandle = FileOpen(OutputFile, FILE_WRITE|FILE_CSV);

//--- Write the header to the CSV file
   if(fileHandle != INVALID_HANDLE)
     {
      FileWrite(fileHandle, "Date,Time,Open,High,Low,Close,Volume");
      FileClose(fileHandle);
     }
   else
     {
      Print("Failed to open the CSV file for writing.");
      return INIT_FAILED;
     }

//--- Export OHLC data at the start
   ExportOHLCData(OutputFile); 

//--- Expert initialization done
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   // Nothing to deinitialize
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   // Nothing to execute every tick
  }
//+------------------------------------------------------------------+
//| Export OHLC data to CSV                                          |
//+------------------------------------------------------------------+
void ExportOHLCData(string filename)
  {
   int fileHandle = FileOpen(filename, FILE_WRITE|FILE_CSV|FILE_READ);

   if(fileHandle != INVALID_HANDLE)
     {
      for (int i = 0; i < Bars; i++)
        {
         datetime date = Time[i];
         double open = Open[i];
         double high = High[i];
         double low = Low[i];
         double close = Close[i];
         long volume = Volume[i];
         
         // Write data to CSV
         FileWrite(fileHandle, TimeToString(date, TIME_DATE), TimeToString(date, TIME_MINUTES), open, high, low, close, volume);
        }
      FileClose(fileHandle);
      Print("OHLC data exported to ", filename);
     }
   else
     {
      Print("Failed to open the CSV file for writing.");
     }
  }
//+------------------------------------------------------------------+

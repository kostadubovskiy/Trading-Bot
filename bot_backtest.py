import alpaca_trade_api as tradeapi
import numpy as np
import time

SEC_KEY = 'YG9WZrEPSOxVlNFPX1BtUlKxWVYEPAFXRyedzlxP'
PUB_KEY = 'PK6PKOSLZUK4KXMI2RIC'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)


symb = "SPY"
pos_held = False
hours_to_test = 5

print("Checking Price")

market_data = api.get_barset(symb, 'minute', limit=(60 * hours_to_test)) # Get one bar object for each of the past 5 minutes

close_list = [] # This array will store all the closing prices from the last 5 minutes
for bar in market_data[symb]:
    close_list.append(bar.c) # bar.c is the closing price of that bar's time interval

print("Open: " + str(close_list[0]))
print("Close: " + str(close_list[60 * hours_to_test - 1]))

close_list = np.array(close_list, dtype=np.float64) # Convert to numpy array
startBal = 2000 # Start out with $2000
balance = startBal
buys = 0
sells = 0

for i in range(4, 60 * hours_to_test): # Start four minutes in, so that MA can be calculated
    ma = np.mean(close_list[i-4:i+1])
    last_price = close_list[i]

    print("Moving average: " + str(ma))
    print("Last Price: " + str(last_price))

    if ma + 0.1 < last_price and not pos_held: # If MA is more than 10cents under price, and we haven't already bought
        print("Buy")
        balance -= last_price
        pos_held = True
        buys += 1
    elif ma - 0.1 > last_price and pos_held: # If MA is more than 10cents above price, and we already bought
        print("Sell")
        balance += last_price
        pos_held = False
        sells += 1
    print("Balance: " +  str(balance))
    time.sleep(0.01)


print("")
print("Buys: " + str(buys))
print("Sells: " + str(sells))

if buys > sells:
    balance += close_list[60 * hours_to_test - 1]

print("Final Balance: " + str(balance))

print("Profit if held: " + str(close_list[60 * hours_to_test - 1] - close_list[0]))
print("Profit from algorithm: " + str(balance - startBal))

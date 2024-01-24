# CryptoBot
A Python Bot that trades Cryptocurrencies based off of custom indicators. 
The main running programme is in Crypto_scanner.

Key variables:
- take-profit: what percentage should each sell price be above the buy price
- stop-loss: At what percentage drop from the buy price do you consider it a loss
- refresh-time: Time interval to consider each spike

Other important variables are documented in the code, these are just the most important ones.

The logic is as follows:
- Monitor all existing Cryptocurrencies of your desired pair 24/7.
- If a price spike is detected. Run your custom indicator script (my script is already included but you can change it if desired)
- Purchase the cryptocurrency and create a stop loss order (risk-management)
- Log when the sell order is executed and determine profit.

- All the best, become a millionaire with this script and buy me a coffee when you do!

  
(Designed by Iloke Alusala)

# CryptoBot

<p align="center">
  <img src="https://img.icons8.com/?size=512&id=55494&format=png" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">CRYPTOBOT</h1>
</p>
<p align="center">
	<!-- Shields.io badges not used with skill icons. --><p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<a href="https://skillicons.dev">
		<img src="https://skillicons.dev/icons?i=md,py&theme=light">
	</a></p>

<br><!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary><br>

- [ Overview](#-overview)
- [ Features](#-features)
- [ Repository Structure](#-repository-structure)
- [ Modules](#-modules)
- [ Getting Started](#-getting-started)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Tests](#-tests)
- [ Contributing](#-contributing)
- [ License](#-license)
</details>
<hr>

##  Overview

<code>The cryptobot is a sophisticated trading bot designed to automate cryptocurrency trading activities. It leverages various algorithms and strategies to analyze market trends, execute trades, and manage assets, all without human intervention. One last thing is that I have excluded the file responsible for generating the custom indicators as it is propriatory, but this boilerplate should still be of extensive value</code>

---

##  Features

<code>Automated Trading: The cryptobot executes trades automatically based on predefined trading strategies. It constantly monitors market conditions and reacts swiftly to changes, allowing for timely and efficient trading.

Data Analysis: It utilizes historical and real-time market data to analyze trends, identify patterns, and make informed trading decisions. This includes candlestick data analysis, technical indicators, and machine learning algorithms to predict market movements.

Risk Management: The bot incorporates risk management protocols to minimize potential losses and maximize profits. This includes setting stop-loss orders, position sizing, and portfolio diversification strategies to mitigate risks.

Backtesting: Before deploying new strategies, the cryptobot conducts extensive backtesting to assess their effectiveness. This involves simulating trades using historical data to evaluate performance and refine strategies accordingly.

Customization: Users can customize trading parameters, such as trading pairs, timeframes, and risk tolerance levels, to align with their investment goals and preferences. Additionally, the bot supports the integration of custom trading strategies and indicators.

Reporting and Analytics: The cryptobot provides comprehensive reporting and analytics tools to track performance, monitor trade history, and analyze profitability metrics. This enables users to gain insights into their trading activities and make data-driven decisions.

Security: Security is paramount in cryptocurrency trading, and the cryptobot prioritizes the safety of user funds and data. It employs industry-standard encryption protocols, secure API integrations, and multi-factor authentication to safeguard accounts and transactions.</code>

---

##  Repository Structure

```sh
└── CryptoBot/
    ├── BacktesterBot.py
    ├── Crypto_Scanner.py
    ├── DataCollectCandleStick.py
    ├── README.md
    ├── cleanLogs.py
    └── mailSender.py
```

---

##  Modules

<details closed><summary>DataCollectCandleStick</summary>

| File                                                                                                          | Summary                         |
| ---                                                                                                           | ---                             |
| [DataCollectCandleStick.py](https://github.com/Iloke-Alusala/CryptoBot/blob/master/DataCollectCandleStick.py) | The `candlestick_data.py` script in this package facilitates the retrieval of historical CandleStick data from the Binance API. It offers methods to fetch data at different granularities and store it in pandas DataFrame format. The package aims to simplify the process of collecting and storing historical market data for further analysis and visualization.

## Features

- Retrieve CandleStick data for various trading pairs and time intervals.
- Store data in pandas DataFrame format for easy manipulation and analysis.
- Support for fetching compressed and uncompressed data.
- Flexible timestamp formatting for different analysis requirements.

## Usage

To utilize this package, follow these steps:

1. Import the package: `from candlestick_data import *`
2. Initialize a Binance client using your API keys.
3. Call the desired function to fetch CandleStick data, providing the required parameters (symbol pair, time interval, start time, end time).
4. Retrieve the data as a pandas DataFrame for further processing.

</details>

<details closed><summary>cleanLogs</summary>

| File                                                                                                          | Summary                         |
| ---                                                                                                           | ---                             |
| [cleanLogs.py](https://github.com/Iloke-Alusala/CryptoBot/blob/master/cleanLogs.py)                           | <code>► INSERT-TEXT-HERE</code> |

</details>

<details closed><summary>Crypto_Scanner</summary>

| File                                                                                                          | Summary                         |
| ---                                                                                                           | ---                             |
| [Crypto_Scanner.py](https://github.com/Iloke-Alusala/CryptoBot/blob/master/Crypto_Scanner.py)                 | The provided script (`log_analysis.py`) processes a log file (`CryptoLogging(Day4).txt`) containing trading data. It identifies unique trading blocks within the log file and stores them in a set, removing duplicates. The script utilizes marker delimiters to distinguish between different types of trading blocks.

## Features

- Extraction of unique trading blocks from a log file.
- Detection of specific markers to delineate trading blocks.
- Storage of unique trading blocks in a set for further analysis.

## Usage

To use this script, follow these steps:

1. Ensure that the log file (`CryptoLogging(Day4).txt`) is located in the same directory as the script.
2. Run the script using Python.
3. The script will analyze the log file and print out the unique trading blocks found within.
</details>

<details closed><summary>BacktesterBot</summary>

| File                                                                                                          | Summary                         |
| ---                                                                                                           | ---                             |
| [BacktesterBot.py](https://github.com/Iloke-Alusala/CryptoBot/blob/master/BacktesterBot.py)                   | The `cryptobot_price_data.py` script is designed to simplify the process of collecting and managing price data for cryptocurrencies. It provides functions to fetch historical price data, split the data based on currency pairs, and align the dataframes to ensure consistency for analysis. Additionally, the script offers functionalities to save the data to CSV files for future reference.

## Features

- Fetch historical price data for cryptocurrencies using the Yahoo Finance API.
- Split the dataframes based on currency pairs for individual analysis.
- Align the dataframes to ensure consistent lengths for comparative analysis.
- Save the processed data to CSV files for easy storage and retrieval.

## Usage

To utilize this script, follow these steps:

1. Import the necessary modules and packages: `import pandas as pd`, `import yfinance as yf`, etc.
2. Call the desired functions to fetch and process the price data as needed.
3. Save the processed data to CSV files for future reference or analysis.

</details>

<details closed><summary>mailSender</summary>

| File                                                                                                          | Summary                         |
| ---                                                                                                           | ---                             |
| [mailSender.py](https://github.com/Iloke-Alusala/CryptoBot/blob/master/mailSender.py)                         | A simple Python script to send emails using Gmail SMTP server.

## Installation

No installation required.

## Usage

1. Replace `gmail_address` and `app_password` with your Gmail email address and [App Password](https://support.google.com/accounts/answer/185833) respectively.

2. Set the `to_email`, `subject`, and `message` variables in the `send_email` function call to the desired values.

3. Run the script.

</details>

---

##  Getting Started

**System Requirements:**

* **Python**: `version 3.11.0`

###  Installation

<h4>From <code>source</code></h4>

> 1. Clone the CryptoBot repository:
>
> ```console
> $ git clone https://github.com/Iloke-Alusala/CryptoBot
> ```
>
> 2. Change to the project directory:
> ```console
> $ cd CryptoBot
> ```
>
> 3. Install the dependencies:
> ```console
> $ pip install -r requirements.txt
> ```

###  Usage

<h4>From <code>source</code></h4>

> Run CryptoBot using the command below:
> ```console
> $ python main.py
> ```

###  Tests

> Run the test suite using the command below:
> ```console
> $ pytest
> ```

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/Iloke-Alusala/CryptoBot/issues)**: Submit bugs found or log feature requests for the `CryptoBot` project.
- **[Submit Pull Requests](https://github.com/Iloke-Alusala/CryptoBot/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/Iloke-Alusala/CryptoBot/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/Iloke-Alusala/CryptoBot
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="center">
   <a href="https://github.com{/Iloke-Alusala/CryptoBot/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Iloke-Alusala/CryptoBot">
   </a>
</p>
</details>

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Extra Info...

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

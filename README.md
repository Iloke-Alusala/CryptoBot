# CryptoBot

<p align="center">
  <img src="https://img.icons8.com/?size=512&id=55494&format=png" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">CRYPTOBOT</h1>
</p>
<p align="center">
    <em><code>► INSERT-TEXT-HERE</code></em>
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
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)
</details>
<hr>

##  Overview

<code>► INSERT-TEXT-HERE</code>

---

##  Features

<code>► INSERT-TEXT-HERE</code>

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

<details closed><summary>.</summary>

| File                                                                                                          | Summary                         |
| ---                                                                                                           | ---                             |
| [DataCollectCandleStick.py](https://github.com/Iloke-Alusala/CryptoBot/blob/master/DataCollectCandleStick.py) | <code>► INSERT-TEXT-HERE</code> |
| [cleanLogs.py](https://github.com/Iloke-Alusala/CryptoBot/blob/master/cleanLogs.py)                           | <code>► INSERT-TEXT-HERE</code> |
| [Crypto_Scanner.py](https://github.com/Iloke-Alusala/CryptoBot/blob/master/Crypto_Scanner.py)                 | <code>► INSERT-TEXT-HERE</code> |
| [BacktesterBot.py](https://github.com/Iloke-Alusala/CryptoBot/blob/master/BacktesterBot.py)                   | <code>► INSERT-TEXT-HERE</code> |
| [mailSender.py](https://github.com/Iloke-Alusala/CryptoBot/blob/master/mailSender.py)                         | <code>► INSERT-TEXT-HERE</code> |

</details>

---

##  Getting Started

**System Requirements:**

* **Python**: `version x.y.z`

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

##  Project Roadmap

- [X] `► INSERT-TASK-1`
- [ ] `► INSERT-TASK-2`
- [ ] `► ...`

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

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-overview)

---


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

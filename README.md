# Ethereum Transaction Fee Mechanisms - User Behavior Research

This repository contains the code and methodology for researching the impact of Ethereum's transaction fee mechanisms on user behavior and decision-making.

## Project Overview

The primary goal of this research is to understand the effects of Ethereum's transaction fee mechanisms, particularly EIP-1559, on user behavior and decision-making. We are focusing on two major aspects of user behavior:

1. **Transaction Frequency**: How frequently users make transactions under different fee mechanisms.
2. **Strategic Behavior**: How users strategically adjust their behaviors, such as timing of transactions and gas price settings, under different fee mechanisms.

## Data Collection

We collect transaction-level data from the Ethereum blockchain for a specified observation period. Our observation period spans from three months prior to the implementation of EIP-1559 to three months post EIP-1559. Each transaction record contains information including but not limited to transaction timestamp, gas price, transaction fee, sender's address, transaction status, and transaction type.

Apart from the transaction data, we also gather other relevant data such as Ether price, network congestion level, Layer 2 solution availability, and EIP-1559 implementation status.

## Data Analysis

We conduct both statistical and machine learning analysis on the collected data. Our models incorporate a range of variables, taking into account user-specific factors, network-wide factors, and market-wide factors. Our methodology includes constructing and analyzing learning curves and examining strategic behaviors.

## Files

* `transaction_data_collection.py`: This script contains the code for collecting Ethereum transaction data.
* `data_preprocessing.py`: This script handles data cleaning, variable derivation, and dataset preparation.
* `model_building.py`: This script contains the code for building and running our statistical models and machine learning algorithms.

## Contact

For any further questions or suggestions, please feel free to reach out to [Aysajan Eziz](aeziz@ivey.ca).

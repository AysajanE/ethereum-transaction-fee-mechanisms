import os
import time
import traceback
import csv
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, as_completed

import pandas as pd
from web3 import Web3

from block_processing import process_block, calculate_burned_fee, calculate_uncle_and_inclusion_reward, setup_web3

# Use Infura API endpoint
infura_url = os.getenv("INFURA_MAINNET_URL")

if not infura_url:
    raise ValueError("INFURA_URL is not set in the environment variables")

web3 = setup_web3(infura_url)

# # Use Ethereum node on local machine
# node_url = 'http://localhost:8545'
# web3 = Web3(Web3.HTTPProvider(node_url))

# Check if the connection is successful
if not web3.is_connected():
    print("Failed to connect to the Ethereum node")

# Constants
MAX_WORKERS = 10  # Number of worker threads for concurrent execution.
BUFFER_SIZE = 100000

# # Trial run
# block_ranges = [
#     (12000000, 12000100),  # First run
#     (12000101, 12000200),  # Second run
#     (12000201, 12000300),  # Third run
#     (12000301, 12000400),  # Fourth run
#     # Add more ranges as needed
# ]

# The block number at 2021-02-05 is 11794239
# The block number at 2022-02-05 is 14143963
block_ranges = [
    (11794239, 12000000),  # First run
    (12000001, 12250000),  # Second run
    (12250001, 12500000),  # Third run
    (12500001, 12750000),  # Fourth run
    (12750001, 13000000),  # Fifth run
    (13000001, 13250000),  # Sixth run
    (13250001, 13500000),  # Seventh run
    (13500001, 13750000),  # Eighth run
    (13750001, 14000000),  # Ninth run
    (14000001, 14143963),  # Tenth run
    # Add more ranges as needed
]


# Manually set the current range index each time you run the script
current_range_index = 0  # Set to 0 for first run, 1 for second run, etc.

def process_blocks(start_block, end_block, filename):
    """
    This function processes a range of blocks using ProcessPoolExecutor for concurrency, and writes the results to a file periodically.

    Args:
        start_block (int): The number of the first block to process.
        end_block (int): The number of the last block to process.
        filename (str): The name of the file to write the results to.

    Returns:
        None
    """
    blocks = list(range(start_block, end_block+1))
    buffer = []

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures_to_blocks = {executor.submit(process_block, block): block for block in blocks}
        for future in as_completed(futures_to_blocks):
            try:
                result = future.result()
                if result is not None:
                    buffer.append(result)
                    if len(buffer) >= BUFFER_SIZE:
                        df = pd.DataFrame(buffer)
                        df.to_csv(filename, mode='a', index=False)
                        buffer = []
            except Exception as e:
                print(f"Error processing block {futures_to_blocks[future]}: {str(e)}")
                print(traceback.format_exc())
        if buffer:  # write remaining data in buffer
            df = pd.DataFrame(buffer)
            df.to_csv(filename, mode='a', index=False)

def main():
    """
    Main function where processing logic should go.
    """
    for start_block, end_block in block_ranges:
        # Generate unique filename for each run
        filename = f"../data/eth_net_supply_{start_block}_{end_block}.csv"
        print(f"Processing from block {start_block} to {end_block}")
        # Call the function to process the blocks
        process_blocks(start_block, end_block, filename)
        time.sleep(10)  # Add delay if needed

if __name__ == "__main__":
    main()

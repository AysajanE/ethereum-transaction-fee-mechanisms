import os
from web3 import Web3
from web3.exceptions import BlockNotFound

# Constants
EIP_1559_BLOCK = 12965000  # Block number where EIP-1559 is implemented.
STATIC_REWARD = 2e18  # Static reward since Constantinople.

def setup_web3(endpoint):
    """
    Initialize a Web3 instance with the given endpoint.
    
    Args:
        endpoint (str): The HTTP provider endpoint to connect to.
    
    Returns:
        Web3: A Web3 instance connected to the provided endpoint.
    """
    return Web3(Web3.HTTPProvider(endpoint))

# # Use Infura API endpoint
# infura_url = os.getenv("INFURA_MAINNET_URL")

# if not infura_url:
#     raise ValueError("INFURA_URL is not set in the environment variables")

# web3 = setup_web3(infura_url)

# Use Ethereum node on local machine
node_url = 'http://localhost:8545'
web3 = setup_web3(node_url)

# Check if the connection is successful
if not web3.is_connected():
    print("Failed to connect to the Ethereum node")

def process_block(block_num):
    """
    This function processes a single block identified by its number.
    It retrieves the block details, computes the static reward, uncle reward, and inclusion reward.
    It also calculates the burned fee after EIP-1559.
    
    Args:
        block_num (int): The number of the block to process.
        
    Returns:
        dict: A dictionary containing the block reward details.
        
    Raises:
        Any exceptions raised during block processing are caught and printed.
    """
    try:
        # Get block details
        block = web3.eth.get_block(block_num, True)
        
        # Calculate uncle reward and inclusion reward
        uncle_reward, inclusion_reward = calculate_uncle_and_inclusion_reward(block, block_num)
        
        # Calculate burned fee
        burned_fee, base_fee_per_gas, gas_used = calculate_burned_fee(block, block_num)

        # Compute net supply increase
        net_supply_increase = STATIC_REWARD + uncle_reward + inclusion_reward - burned_fee

        return {
            'block_number': block_num,
            'static_reward': STATIC_REWARD,
            'uncle_reward': uncle_reward,
            'inclusion_reward': inclusion_reward,
            'base_fee': base_fee_per_gas,
            'gas_used': gas_used,
            'burned_fee': burned_fee,
            'net_supply_increase': net_supply_increase
        }
    except Exception as e:
        print(f"Error processing block {block_num}: {str(e)}")
        return None

def calculate_uncle_and_inclusion_reward(block, block_num):
    """
    This function calculates the uncle reward and the inclusion reward for a given block.
    
    Args:
        block (dict): The block details.
        block_num (int): The number of the block to process.
        
    Returns:
        tuple: A tuple containing uncle_reward and inclusion_reward.
    """
    uncle_reward = 0
    inclusion_reward = 0
    for i in range(len(block['uncles'])):
        uncle_block = web3.eth.get_uncle_by_block(block_num, i)
        uncle_age = block['number'] - int(uncle_block['number'], 16)
        uncle_reward += ((8 - uncle_age) / 8) * STATIC_REWARD
        inclusion_reward += STATIC_REWARD / 32
    return uncle_reward, inclusion_reward

def calculate_burned_fee(block, block_num):
    """
    This function calculates the burned fee for a given block after EIP-1559.
    
    Args:
        block (dict): The block details.
        block_num (int): The number of the block to process.
        
    Returns:
        tuple: A tuple containing burned_fee, base_fee_per_gas, and gas_used.
    """
    burned_fee = 0
    base_fee_per_gas = 0
    gas_used = block['gasUsed']
    if block_num >= EIP_1559_BLOCK:
        base_fee_per_gas = block['baseFeePerGas']
        burned_fee = base_fee_per_gas * gas_used
    return burned_fee, base_fee_per_gas, gas_used

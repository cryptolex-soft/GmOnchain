from web3 import Web3
from config import GAS_ZIP_CALLDATA, NETWORKS

def create_calldata(chain_name: str) -> str:
    return GAS_ZIP_CALLDATA.get(chain_name, {}).get("calldata", "0x")


def send_gas_zip_transaction(private_key: str, value_eth: float, from_chain_name: str, to_chain_name: str):
    if from_chain_name not in NETWORKS:
        print(f"[{from_chain_name}] ❌ Unknown network")
        return

    chain_data = NETWORKS[from_chain_name]
    rpc = chain_data["rpc"]
    chain_id = chain_data["chain_id"]

    w3 = Web3(Web3.HTTPProvider(rpc))
    account = w3.eth.account.from_key(private_key)
    sender_address = account.address

    value_wei = w3.to_wei(value_eth, "ether")

    # Получаем цену газа
    try:
        latest_block = w3.eth.get_block('latest')
        base_fee = latest_block.get('baseFeePerGas', w3.eth.gas_price)
    except:
        base_fee = w3.eth.gas_price

    max_priority_fee = w3.to_wei(0.1, 'gwei')
    max_fee = int(base_fee * 1.5) + max_priority_fee

    # Статический адрес контракта Gas.Zip
    gas_zip_address = Web3.to_checksum_address("0x391E7C679d29bD940d63be94AD22A25d25b5A604")
    calldata = create_calldata(to_chain_name)

    tx = {
        'from': sender_address,
        'to': gas_zip_address,
        'value': value_wei,
        'gas': 100_000,
        'maxFeePerGas': max_fee,
        'maxPriorityFeePerGas': max_priority_fee,
        'nonce': w3.eth.get_transaction_count(sender_address),
        'data': calldata,
        'chainId': chain_id
    }

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    print(f"[{from_chain_name}] ✅ Bridged to {to_chain_name}: {tx_hash.hex()}")
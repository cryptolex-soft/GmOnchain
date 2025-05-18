import random
import time
from datetime import datetime, timedelta
from gas_zip import send_gas_zip_transaction
from web3 import Web3
from config import NETWORKS, TRANSACTION_VALUE, TX_DELAY, WALLETS_DELAY, MIN_GM_INTERVAL_HOURS
from database import get_wallets, update_gm_timestamp
from eth_account import Account
from utils import get_richest_network

# Новый корректный метод-селектор для onChainGM()
GM_FUNCTION_SELECTOR = "0x5011b71c"


def should_send_gm(wallet, network_name):
    key = f"last_gm_{network_name}"
    last_gm = wallet.get(key)

    if last_gm is None or str(last_gm).strip().lower() in ("none", "null", ""):
        print(f"[{wallet['address']}] ✅ No GM timestamp for {network_name}. Proceeding.")
        return True

    try:
        last_time = datetime.fromisoformat(last_gm)
        now = datetime.utcnow()
        delta = now - last_time

        print(f"[{wallet['address']}] ⏱ {network_name}: last GM = {last_time}, now = {now}, Δ = {delta}")
        return delta > timedelta(hours=MIN_GM_INTERVAL_HOURS)

    except Exception as e:
        print(f"[{wallet['address']}] ⚠️ Failed to parse timestamp '{last_gm}' for {network_name}: {e}")
        return True






def send_gm_transaction(web3, wallet, contract_address):
    account = Account.from_key(wallet["private_key"])
    address = account.address

    nonce = web3.eth.get_transaction_count(address)
    gas_price = max(web3.eth.gas_price, Web3.to_wei(0.5, "gwei"))  # Минимальный порог
    value = Web3.to_wei(TRANSACTION_VALUE, "ether")

    tx = {
        "to": Web3.to_checksum_address(contract_address),
        "value": value,
        "gas": 120_000,
        "gasPrice": gas_price,
        "nonce": nonce,
        "data": GM_FUNCTION_SELECTOR,
        "chainId": web3.eth.chain_id,
    }

    signed_tx = web3.eth.account.sign_transaction(tx, wallet["private_key"])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"[{address}] ✅ GM sent! TX hash: {tx_hash.hex()}")
    return tx_hash.hex()


def run_gm_for_all_wallets():
    wallets = get_wallets()

    for wallet in wallets:
        addr = wallet["address"]
        priv_key = wallet["private_key"]

        print(f"\n=== Running GM for wallet: {addr} ===")

        network_names = list(NETWORKS.keys())
        random.shuffle(network_names)

        for network_name in network_names:
            net = NETWORKS[network_name]
            web3 = Web3(Web3.HTTPProvider(net["rpc"]))
            contract_address = net["contract"]

            # Проверка баланса
            balance_wei = web3.eth.get_balance(addr)
            balance_eth = web3.from_wei(balance_wei, "ether")

            if balance_eth < 0.0003:
                print(f"[{addr}] ⚠️ Low balance in {network_name}: {balance_eth} ETH. Checking for bridge option...")
                richest_chain = get_richest_network(priv_key)
                print(f"[{richest_chain}] is the richest chain")

                if richest_chain and richest_chain != network_name:
                    print(f"[{addr}] 🔄 Bridging from {richest_chain} to {network_name}...")
                    try:
                        send_gas_zip_transaction(priv_key, 0.00035, richest_chain, network_name)
                        print(f"[{addr}] Waiting 30 secs...")
                        time.sleep(30)  # Подождать подтверждение бриджа
                    except Exception as e:
                        print(f"[{addr}] ❌ Bridge failed: {e}")
                        continue
                else:
                    print(f"[{addr}] ⛔ No suitable source chain with enough ETH. Skipping {network_name}.")
                    continue

            if not should_send_gm(wallet, network_name):
                print(f"[{addr}] ⏩ Already GM'd recently on {network_name}. Skipping.")
                continue

            try:
                send_gm_transaction(web3, {"address": addr, "private_key": priv_key}, contract_address)
                update_gm_timestamp(addr, network_name)
                tx_delay = random.randint(*TX_DELAY)
                print(f"[{addr}] ⏱ Sleeping after TX in {network_name} for {tx_delay}s...\n")
                time.sleep(tx_delay)
            except Exception as e:
                print(f"[{addr}] ❌ Error in {network_name}: {e}")

        wallet_delay = random.randint(*WALLETS_DELAY)
        print(f"[{addr}] ⏳ Wallet delay: {wallet_delay}s\n")
        time.sleep(wallet_delay)
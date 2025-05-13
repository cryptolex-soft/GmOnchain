from web3 import Web3
from eth_account import Account
from database import init_db, insert_wallet
from config import NETWORKS

def load_keys_from_file(filename="privatekeys.txt"):
    keys = []
    with open(filename, "r") as f:
        for line in f:
            key = line.strip()
            if key:
                keys.append(key)
    return keys

def import_wallets():
    init_db()
    keys = load_keys_from_file()
    print(f"🔑 Найдено приватных ключей: {len(keys)}")

    for key in keys:
        try:
            acct = Account.from_key(key)
            address = Web3.to_checksum_address(acct.address)
            insert_wallet(address, key)
            print(f"[+] Импортировано: {address}")
        except Exception as e:
            print(f"[!] Ошибка с ключом: {key[:10]}... — {e}")

def get_richest_network(private_key):
    """
    Находит сеть с максимальным ETH-балансом, если он больше 0.0007 ETH
    """
    richest = None
    max_balance = 0

    for net_name, net in NETWORKS.items():
        w3 = Web3(Web3.HTTPProvider(net["rpc"]))
        account = w3.eth.account.from_key(private_key)
        balance = w3.eth.get_balance(account.address)
        balance_eth = w3.from_wei(balance, 'ether')

        if balance_eth > 0.0007 and balance_eth > max_balance:
            max_balance = balance_eth
            richest = net_name

    return richest

if __name__ == "__main__":
    import_wallets()

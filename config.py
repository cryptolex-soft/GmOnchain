class CHAIN_ID:
    BASE = 8453
    OP_MAINNET = 10
    SONEIUM = 1868
    UNICHAIN = 130
    INK = 57073
    MODE_MAINNET = 34443
    LISK = 1133

    @classmethod
    def all(cls):
        return [value for key, value in cls.__dict__.items() if not key.startswith("__") and not callable(value)]




NETWORKS = {
    "optimism": {
        "chain_id": CHAIN_ID.OP_MAINNET,
        "rpc": "https://1rpc.io/op",
        "contract": "0x3bb9FF29748e4C5A78E9434D192dA6619788874b",
    },
    "unichain": {
        "chain_id": CHAIN_ID.UNICHAIN,
        "rpc": "https://unichain-rpc.publicnode.com",
        "contract": "0x1036F884612C15B704307Faf8261FED2285F7B95",
    },
    "soneium": {
        "chain_id": CHAIN_ID.SONEIUM,
        "rpc": "https://soneium.drpc.org",
        "contract": "0x46Fd6738f0129c968bceA6B22cA28f9051de5318"
    },
    "base": {
        "chain_id": CHAIN_ID.BASE,
        "rpc": "https://base.llamarpc.com",
        "contract": "0x5C51D7f25206f2E54221E20b131CF179344e09B4",
    },
    "ink": {
        "chain_id": CHAIN_ID.INK,
        "rpc": "https://ink.drpc.org",
        "contract": "0x0fEa1dE3f1dfDAa0E0CB848aa85625Ce2433689B",
    },
    "mode": {
        "chain_id": CHAIN_ID.MODE_MAINNET,
        "rpc": "https://mode.drpc.org",
        "contract": "0xF991F48855Cc362bCe23B7BBFa077685040110dB",
    },
    "lisk": {
        "chain_id": CHAIN_ID.LISK,
        "rpc": "https://lisk.drpc.org",
        "contract": "0xB8cCfe18bb8eC7E67168A48b17348Eac5637bedd",
    },
}

GAS_ZIP_CALLDATA = {
    "optimism": {
        "calldata": "0x010037",
    },
    "unichain": {
        "calldata": "0x01016a",
    },
    "soneium": {
        "calldata": "0x01019e"
    },
    "base": {
        "calldata": "0x010036",
    },
    "ink": {
        "calldata": "0x010188",
    },
    "mode": {
        "calldata": "0x010049",
    },
    "lisk": {
        "calldata": "0x0100ee",
    },
}


TRANSACTION_VALUE = 0.000029

TX_DELAY = [10, 20]  # случайная задержка между транзакциями, секунд
WALLETS_DELAY = [120, 600]  # случайная задержка между транзакциями, секунд
MIN_GM_INTERVAL_HOURS = 24  # сколько часов должно пройти между GM для одного кошелька

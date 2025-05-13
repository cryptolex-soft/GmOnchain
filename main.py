from gmsender import run_gm_for_all_wallets
from database import init_db
import time

def print_banner():
    red = "\033[91m"
    reset = "\033[0m"

    banner = r"""
    t.me/olxs_research ^ t.me/olxs_research
    t.me/olxs_research ^ t.me/olxs_research
    t.me/olxs_research ^ t.me/olxs_research
    t.me/olxs_research ^ t.me/olxs_research
    """

    print(red + banner + reset)


def main():
    print_banner()
    time.sleep(3)
    init_db()
    run_gm_for_all_wallets()

if __name__ == "__main__":
    main()
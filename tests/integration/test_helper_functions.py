"""
Testing `erpy.helper_functions`
===============================

Handled functions :
- get_wallet_address

"""
# Necessary packages
from ergpy import helper_functions
from ergpy.appkit import ErgoAppKit
import json
import logging
import os
import sys

# Setup
logger: logging.Logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Tested functions
def test_get_wallet_address():
    # Expected
    expected: str = "3Wz5WvHQe1G5kvLwMBeuxjaChd1j2RzdzFipCmHnJ1MMX7jAvA8f"

    # Arguments
    node_url: str = "http://213.239.193.208:9052/"
    ergo: ErgoAppKit = ErgoAppKit(node_url=node_url)
    amount: int = 1
    wallet_mnemonic: str = ""

    # Call function
    logging.info('BEGIN get_wallet_address')
    actual: str = json.loads(helper_functions.get_wallet_address(ergo=ergo, amount=amount, wallet_mnemonic=wallet_mnemonic))[0]
    logging.info('END get_wallet_address')

    assert actual == expected

# Program entrypoint
if __name__ == '__main__':
    test_get_wallet_address()

    # Gracefully exit
    sys.exit(os.EX_OK)

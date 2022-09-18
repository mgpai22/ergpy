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
    #  Expected
    expected: str = "3Wx2YrSVcrPvC7uXQRp6ZQfRd7VxjZr6fjhFEX5r1yiM8nHkGv93"

    # Arguments
    node_url: str = "http://213.239.193.208:9052/"
    ergo: ErgoAppKit = ErgoAppKit(node_url=node_url)
    amount: int = 1
    wallet_mnemonic: str = "decline reward asthma enter three clean borrow repeat identify wisdom horn pull entire adapt neglect"

    # Call function
    logging.info('BEGIN get_wallet_address')
    actual: str = helper_functions.get_wallet_address(ergo=ergo, amount=amount, wallet_mnemonic=wallet_mnemonic)[0]
    logging.info(f'END get_wallet_address')

    assert actual == expected


# Program entrypoint
if __name__ == '__main__':
    test_get_wallet_address()

    # Gracefully exit
    sys.exit(os.EX_OK)

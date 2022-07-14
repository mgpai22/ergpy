"""
Example no.2
============

Just an example of chained transactions

AUTHOR
    mgpai22@GitHub

CREATED AT
    Sat. 4 Jun. 2022 12:00
"""
# Import packages
import json
import logging

# Import `ergpy`
import time

from ergpy import helper_functions, appkit

# Logging utility
LOGGING_FORMAT = '[%(asctime)s] - [%(levelname)-8s] -  %(message)s'
logging.basicConfig(format=LOGGING_FORMAT)
logger: logging.Logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create connection to the blockchain
node_url: str = "http://213.239.193.208:9052/"  # MainNet or TestNet
ergo = appkit.ErgoAppKit(node_url=node_url)

# Wallet mnemonic
wallet_mnemonic = "decline reward asthma enter three clean borrow repeat identify wisdom horn pull entire adapt neglect"

receiver_addresses = [
    "3WwdXmYP39DLmDWJ6grH9ArXbWuCt2uGAh46VTfeGPrHKJJY6cSJ",
    "3WwuG9amNVDwkJdgT5Ce7aJCfeoafVmd9tag9AEiAZwgPi7pYX3w",
    "3Wxk5oofZ3Laq2CpFW4Fi9YQiaep9bZr6QFg4s4xpzz4bi9tZq2U"
]

amount = [0.22, 0.33, 0.11]


consecutive_transactions = 3
sleep_time = 0.5 # the amount of time in seconds the program will pause in between submitting txs
# here we calculate the amount of ergs required for the genesis outbox
genesis_amount = [consecutive_transactions * (0.22 + 0.33 + 0.11) + (consecutive_transactions + 1) * 0.001]
genesis_receiver = [""]  # wallet of sender

# This creates an outbox for the chained transaction but will not submit it automatically to the node
genesis_tx = helper_functions.simple_send(ergo=ergo, amount=genesis_amount, wallet_mnemonic=wallet_mnemonic,
                                          receiver_addresses=genesis_receiver, return_signed=True)
genesis_outbox = appkit.get_outputs_to_spend(genesis_tx, 0)  # This returns an outbox from the signed tx
print(ergo.txId(genesis_tx))  # This submits the tx to the node and prints the txid to the console
outBox_list = []
for x in range(consecutive_transactions):
    if x == 0: # first tx has to get input box from the genesis outbox
        tx_1 = helper_functions.simple_send(ergo=ergo, amount=amount, wallet_mnemonic=wallet_mnemonic,
                                            receiver_addresses=receiver_addresses, input_box=genesis_outbox,
                                            return_signed=True, chained=True)
    elif x == consecutive_transactions - 1: # last tx is not chained
        tx_1 = helper_functions.simple_send(ergo=ergo, amount=amount, wallet_mnemonic=wallet_mnemonic,
                                            receiver_addresses=receiver_addresses, input_box=outBox_list[x - 1],
                                            return_signed=True)
    else: # gets input box from the prior chained tx
        tx_1 = helper_functions.simple_send(ergo=ergo, amount=amount, wallet_mnemonic=wallet_mnemonic,
                                            receiver_addresses=receiver_addresses, input_box=outBox_list[x - 1],
                                            return_signed=True, chained=True)
    tx_1_outbox = appkit.get_outputs_to_spend(tx_1, 0)
    outBox_list.append(tx_1_outbox)
    time.sleep(sleep_time)
    print(ergo.txId(tx_1)) # submits tx to node
    time.sleep(sleep_time)
helper_functions.exit()
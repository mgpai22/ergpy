"""
Example no.3
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
    "3WwdXmYP39DLmDWJ6grH9ArXbWuCt2uGAh46VTfeGPrHKJJY6cSJ"
]

amount = [0.001]

consecutive_transactions = 3
sleep_time = 0.5  # the amount of time in seconds the program will pause in between submitting txs
# here we calculate the amount of ergs required for the genesis outbox
genesis_amount = [1] # should be good for around 500 token transfers
genesis_receiver = [""]  # wallet of sender

tokenList_genesis = [["tokenID_A", # tokens that need to be selected from input boxes
                      "tokenID_B", # these are in the usual 2D Array format
                      "tokenID_C"
                      ]]
tokenList_tx = [[["tokenID_A"]], # tokens that get put into actual txs to another address
                [["tokenID_B"]], # order does matter here
                [["tokenID_C"]]  # note that these are in the 3D Array format to account for the loop below
                ]

# This creates an outbox for the chained transaction but will not submit it automatically to the node
genesis_tx = helper_functions.send_token(ergo=ergo, amount=genesis_amount, wallet_mnemonic=wallet_mnemonic,
                                         receiver_addresses=genesis_receiver, return_signed=True, tokens=tokenList_genesis)
genesis_outbox = appkit.get_outputs_to_spend(genesis_tx, 0)  # This returns an outbox from the signed tx
print(ergo.txId(genesis_tx))  # This submits the tx to the node and prints the txid to the console
outBox_list = []
for x in range(consecutive_transactions):
    if x == 0:  # first tx has to get input box from the genesis outbox
        tx_1 = helper_functions.send_token(ergo=ergo, amount=amount, wallet_mnemonic=wallet_mnemonic,
                                           receiver_addresses=receiver_addresses, input_box=genesis_outbox,
                                           tokens=tokenList_tx[x], return_signed=True, chained=True)
    elif x == consecutive_transactions - 1:  # last tx is not chained
        tx_1 = helper_functions.send_token(ergo=ergo, amount=amount, wallet_mnemonic=wallet_mnemonic,
                                           receiver_addresses=receiver_addresses, input_box=outBox_list[x - 1],
                                           tokens=tokenList_tx[x], return_signed=True)
    else:  # gets input box from the prior chained tx
        tx_1 = helper_functions.send_token(ergo=ergo, amount=amount, wallet_mnemonic=wallet_mnemonic,
                                           receiver_addresses=receiver_addresses, input_box=outBox_list[x - 1],
                                           tokens=tokenList_tx[x], return_signed=True, chained=True)
    tx_1_outbox = appkit.get_outputs_to_spend(tx_1, 0)
    outBox_list.append(tx_1_outbox)
    time.sleep(sleep_time)
    print(ergo.txId(tx_1))  # submits tx to node
    time.sleep(sleep_time)
helper_functions.exit()
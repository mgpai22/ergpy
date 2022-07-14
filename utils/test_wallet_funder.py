"""
Utility
============

Give a wallet with funds, this program generates additional wallets and automatically adds funds to each of them.
This is useful for quick testing.

AUTHOR
    mgpai22@GitHub

CREATED AT
    Wed. 13 Jul. 2022 01:43
"""
from ergpy import helper_functions, appkit
from mnemonic import Mnemonic

# Create connection to the blockchain
node_url: str = "http://213.239.193.208:9052/"  # MainNet or TestNet
ergo = appkit.ErgoAppKit(node_url=node_url)
mnemo = Mnemonic("english")
wallet_mnemonic = ""
# Insert the mnemonic of where funds will come from
amount_of_wallets = 1 # amount of wallets which will be generated
funds_per_wallet = 1 # amount of funds that will get put into each wallet

mnemonic_list = []
receiver_addresses = []
amount = []
i = 0
for x in range(amount_of_wallets):
    mnemonic_list.append(mnemo.generate(strength=160))
for mnemonic in mnemonic_list:
    receiver_addresses.append(helper_functions.get_wallet_address(ergo=ergo, amount=1, wallet_mnemonic=mnemonic)[0])
    amount.append(funds_per_wallet)
    print(mnemonic, receiver_addresses[i])
    i = i + 1


print(helper_functions.simple_send(ergo=ergo, amount=amount, wallet_mnemonic=wallet_mnemonic, receiver_addresses=receiver_addresses))

helper_functions.exit()

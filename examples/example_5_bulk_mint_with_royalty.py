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

amount_nfts_to_mint = 10
royalty = 5

nft_name = "pythonWrapper v2 NFT example #"
description = "MGpai's python wrapper bulk test with royalties"
image_link = "ipfs://bafkreihvadi66kddokso7x2i4kmqjhj5e3j44rn347i7drghekr2mfw3nu"
image_hash = appkit.sha256caster("f500d1ef286372a4efdf48e299049d3d26d3ce45bbe7d1f1c4c722a3a616db6d")
# creates signed tx of issuer boxes with royalty amount
tx = helper_functions.create_issuer_box(ergo=ergo, wallet_mnemonic=wallet_mnemonic,
                                        royalty_amount_in_percent=royalty,
                                        amount_of_boxes=amount_nfts_to_mint, return_signed=True)
issuer_box = []
# coverts outputs to inputs for chained txs and appends them to a list
for box in range(amount_nfts_to_mint):
    issuer_box.append(appkit.get_outputs_to_spend(tx, box))
# sends the issuer box tx
print(ergo.txId(tx))

# mints nfts getting the inputs from the list
for nft_tx in range(amount_nfts_to_mint):
    print(helper_functions.create_nft(ergo=ergo, nft_name=str(nft_name) + str(nft_tx + 1), description=description, image_link=image_link,
                                      image_hash=image_hash, wallet_mnemonic=wallet_mnemonic, input_box=issuer_box[nft_tx],
                                      ))

helper_functions.exit()
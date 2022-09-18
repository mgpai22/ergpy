# Import packages
import json
import logging

# Import `ergpy`
import time

from jpype import java

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
wallet_mnemonic = "control all chase away alter swarm sight group sorry hybrid impose else truck motor bitter"

amount_nfts_to_mint = 100  # actual total cost for 67 nfts is 0.073
# 100.502 erg required to mint 1000 nfts, the actual fee is 1.024
royalty = 5

sender_address = helper_functions.get_wallet_address(ergo=ergo, amount=2, wallet_mnemonic=wallet_mnemonic)
consolidator_address = sender_address[1]

nft_name = "pythonWrapper v6 NFT example #"
description = "MGpai's python wrapper bulk test with royalties"
image_link = "ipfs://bafkreihvadi66kddokso7x2i4kmqjhj5e3j44rn347i7drghekr2mfw3nu"
image_hash = appkit.sha256caster("f500d1ef286372a4efdf48e299049d3d26d3ce45bbe7d1f1c4c722a3a616db6d")
# creates signed tx of issuer boxes with royalty amount

box_list = java.util.ArrayList([])

genesis_amount = [0.5 + (0.1 * amount_nfts_to_mint) + (2 * 0.001)]

genesis_tx = helper_functions.simple_send(ergo=ergo, amount=genesis_amount, wallet_mnemonic=wallet_mnemonic,
                                          receiver_addresses=[sender_address[0]], return_signed=True)

genesis_outbox = appkit.get_outputs_to_spend(genesis_tx, 0)
ergo.txId(genesis_tx)

consolidator_address_funding = helper_functions.simple_send(ergo=ergo, amount=[0.5], wallet_mnemonic=wallet_mnemonic,
                                                            receiver_addresses=[consolidator_address],
                                                            input_box=genesis_outbox,
                                                            return_signed=True, chained=True)
consolidator_address_funding_outbox = appkit.get_outputs_to_spend(consolidator_address_funding, asArray=False,
                                                                  index_for_outbox=1)

ergo.txId(consolidator_address_funding)
issuer_box_tx = helper_functions.create_issuer_box(ergo=ergo, wallet_mnemonic=wallet_mnemonic,
                                                   royalty_amount_in_percent=royalty,
                                                   input_box=appkit.get_outputs_to_spend(consolidator_address_funding,
                                                                                         0),
                                                   amount_of_boxes=amount_nfts_to_mint, return_signed=True)

print("consolidator address:", consolidator_address)

issuer_box = []
nft_box = []
token_box = []
list_of_tokens = []
final_token_list = []
tList = []
nft_box_list = java.util.ArrayList([])
nft_box_list_1 = []
final_box_list = java.util.ArrayList([])
consolidator_list = []
address_list = []
length = 0

# coverts outputs to inputs for chained txs and appends them to a list
for box in range(amount_nfts_to_mint):
    issuer_box.append(appkit.get_outputs_to_spend(issuer_box_tx, box))
# sends the issuer box tx
ergo.txId(issuer_box_tx)
# time.sleep(0.5)
consolidator_counter = 0
# mints nfts getting the inputs from the list
for nft_tx in range(amount_nfts_to_mint):
    consolidator_counter = consolidator_counter + 1
    nft = helper_functions.create_nft(ergo=ergo, nft_name=str(nft_name) + str(nft_tx + 1), description=description,
                                      image_link=image_link,
                                      image_hash=image_hash, wallet_mnemonic=wallet_mnemonic,
                                      input_box=issuer_box[nft_tx], return_signed=True
                                      )
    nft_box.append(appkit.get_outputs_to_spend(nft, asArray=False))
    ergo.txId(nft)
    #     time.sleep(0.5)

    if consolidator_counter == 50 or nft_tx == amount_nfts_to_mint - 1:
        for box in nft_box:
            box = box.get(0)
            list_of_tokens.append(box.getTokens().get(0).getId())
            nft_box_list.add(box)
        consolidated_tx = helper_functions.send_token(ergo=ergo, amount=[0.001], wallet_mnemonic=wallet_mnemonic,
                                                      receiver_addresses=[consolidator_address], return_signed=True,
                                                      input_box=nft_box_list,
                                                      tokens=[list_of_tokens])
        consolidator_list.append(appkit.get_outputs_to_spend(consolidated_tx, asArray=False))
        print("consolidated tx in progress")
        ergo.txId(consolidated_tx)
        # time.sleep(0.5)
        consolidator_counter = 0
        nft_box.clear()
        nft_box_list.clear()
        list_of_tokens.clear()
for box in consolidator_list:
    token_box.clear()
    item = box.get(0)
    nft_box_list.add(item)
    nft_box_list_1.append(item)

for box in nft_box_list_1:
    tokens_array = box.getTokens()
    for token in range(tokens_array.size()):
        tList.append(tokens_array.get(token).getId())
    final_token_list.append(tList)
    tList = []

nft_box_list.add(consolidator_address_funding_outbox)
amount_list = []
for x in range(len(final_token_list)):
    address_list.append(sender_address[0])
    amount_list.append(0.001)

print("final tx:",
      helper_functions.send_token(ergo=ergo, amount=amount_list, receiver_addresses=address_list,
                                  tokens=final_token_list,
                                  input_box=nft_box_list,
                                  sender_address=consolidator_address,
                                  wallet_mnemonic=wallet_mnemonic, prover_index=1))

helper_functions.exit()

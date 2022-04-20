from ergpy import helperMethods, appkit

ergo = appkit.ErgoAppKit(nodeURL="http://213.239.193.208:9052/") # create connection to the blockchain
# testnet or mainnet will be automatically determined based on the node url
walletMnemonic = ""
# mnemonicPassword = "my password" this is optional. Only include if you have a mnemonic password
receiverAddresses = ["3WwdXmYP39DLmDWJ6grH9ArXbWuCt2uGAh46VTfeGPrHKJJY6cSJ", "3WwuG9amNVDwkJdgT5Ce7aJCfeoafVmd9tag9AEiAZwgPi7pYX3w",
                     "3Wxk5oofZ3Laq2CpFW4Fi9YQiaep9bZr6QFg4s4xpzz4bi9tZq2U"]
amount = [0.22, 0.33, 0.11]
tokens = [["tokenID_A", "tokenID_B", "tokenID_C"], ["tokenID_D"], ["tokenID_E", "tokenID_F"]]

"""
note how parameters are inputed

In simple send, 3WwdX would get 0.22 ERG, 3WwuG9 would get 0.33 ERG, 3Wxk5o would get 0.11 ERG

In token send, 3WwdX would get 0.22 ERG and tokens A, B, C, 3WwuG9 would get 0.33 ERG and token D and so on
"""

nftName = "pythonWrapper NFT"
description = "created by MGpai's python wrapper"
imageLink = "ipfs://bafkreihvadi66kddokso7x2i4kmqjhj5e3j44rn347i7drghekr2mfw3nu"
imageHash = appkit.sha256caster("f500d1ef286372a4efdf48e299049d3d26d3ce45bbe7d1f1c4c722a3a616db6d")

"""
base64 reduced transactions are also possible, the only current problem is the boxes are preselected so
if another tx gets processed before submitting the base64 tx,  it will not go through
Just add the base64reduced=True to get this
for example

print(helperMethods.simpleSend(ergo=ergo, amount=amount, walletMnemonic=walletMnemonic, receiverAddresses=receiverAddresses, base64reduced=True))

Specifying senderAddress is also possible. Once specified, the boxes will be selected from this address and change
will be sent here as well. Make sure the prover index is specified as well (same index as address derivation). 

"""

# print(helperMethods.getWalletAddress(ergo=ergo, amount=5, walletMnemonic=walletMnemonic))
# print(helperMethods.getBoxInfo(ergo=ergo, index=0, senderAddress=receiverAddresses[0]))
# print(helperMethods.simpleSend(ergo=ergo, amount=amount, walletMnemonic=walletMnemonic, receiverAddresses=receiverAddresses))
# print(helperMethods.sendToken(ergo=ergo, amount=amount, receiverAddresses=receiverAddresses, tokens=tokens, walletMnemonic=walletMnemonic))
# print(helperMethods.createToken(ergo=ergo, tokenName=nftName, description=description, tokenAmount=1, tokenDecimals=0, walletMnemonic=walletMnemonic))
# print(helperMethods.createNFT(ergo=ergo, nftName=nftName, description=description, imageLink=imageLink, imageHash=imageHash, walletMnemonic=walletMnemonic))

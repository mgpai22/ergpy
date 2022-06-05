"""
Helper functions
================

Utility functions to make everything easy.

AUTHOR
    mgpai22@GitHub

CREATED AT
    Wed. 20 Apr. 2022 23:43
"""
# Import external packages
import json
import logging
import jpype
from ergpy import appkit

# Functions
def initialize_jvm(function):
    """
    Initialize the JVM before calling the function.
    """
    def wrapper(*args, **kwargs):
        try:
            # Import content inside jar file
            jpype.addClassPath('ergo.jar')

            # Start JVM
            jpype.startJVM()

        except OSError as oserror:
            logging.warning(oserror)
        
        finally:
            # Call function
            res = function(*args, **kwargs)

            return res

    return wrapper

@initialize_jvm
def exit():
    jpype.java.lang.System.exit(0)

@initialize_jvm
def get_wallet_address(ergo: appkit.ErgoAppKit, amount: int, wallet_mnemonic: str,
        mnemonic_password: str=None) -> str:
    # Get mnemonic
    mnemonic = ergo.getMnemonic(wallet_mnemonic=wallet_mnemonic, mnemonic_password=mnemonic_password)

    # Get list of addresses
    addresses: list[str] = [
        str(ergo.getSenderAddress(x, mnemonic[1], mnemonic[2]))
        for x in range(amount)
    ]

    return json.dumps(addresses)

@initialize_jvm
def get_box_info(ergo: appkit.ErgoAppKit, index: int, sender_address: str) -> str:
    # Setup parameters
    amount = [1]
    sender_address = ergo.castAddress(sender_address)
    input_box = ergo.getInputBox(amount_list=amount, sender_address=sender_address)

    return ergo.getBoxInfo(input_box, index)

@initialize_jvm
def simple_send(ergo: appkit.ErgoAppKit, amount: list, receiver_addresses: list, wallet_mnemonic: str,
        mnemonic_Ppassword: str=None, sender_address: str=None, prover_index: int=None,
        base64reduced: bool=None):

    # Get mnemonic associated to wallet
    mnemonic = ergo.getMnemonic(wallet_mnemonic=wallet_mnemonic, mnemonic_password=mnemonic_Ppassword)
    
    # Get sender address from mnemonix
    sender_address = ergo.getSenderAddress(index=0, wallet_mnemonic=mnemonic[1], wallet_password=mnemonic[2]) \
        if sender_address is None \
        else ergo.castAddress(sender_address)

    # Get input box
    input_box = ergo.getInputBox(amount_list=amount, sender_address=sender_address)
    
    # Get output box
    out_box = ergo.buildOutBox(receiver_wallet_addresses=receiver_addresses, amount_list=amount)
    
    # Build unsigned transaction
    unsigned_tx = ergo.buildUnsignedTransaction(input_box=input_box, outBox=out_box, sender_address=sender_address)

    if base64reduced:
        return ergo.getBase64ReducedTX(unsigned_tx)

    # Sign transaction
    signed_tx = ergo.signTransaction(unsigned_tx, mnemonic[0], prover_index)
    
    return ergo.txId(signed_tx)

@initialize_jvm
def send_token(ergo: appkit.ErgoAppKit, amount: list, receiver_addresses: list, tokens: list, wallet_mnemonic: str,
              mnemonic_password: str=None, sender_address: str=None, prover_index: int=None,
              base64reduced: bool=None):
    # Get mnemonice
    mnemonic = ergo.getMnemonic(wallet_mnemonic=wallet_mnemonic, mnemonic_password=mnemonic_password)

    # Get sender address
    sender_address = ergo.getSenderAddress(index=0, wallet_mnemonic=mnemonic[1], wallet_password=mnemonic[2]) \
        if sender_address is None \
        else ergo.castAddress(sender_address)
    
    # Get input and output box
    input_box = ergo.getInputBox(amount_list=amount, sender_address=sender_address)
    out_box = ergo.tokenOutBox(receiver_wallet_addresses=receiver_addresses, amount_list=amount, tokens=tokens)
    
    # Build transaction
    unsigned_tx = ergo.buildUnsignedTransaction(input_box=input_box, outBox=out_box, sender_address=sender_address)

    if base64reduced:
        return ergo.getBase64ReducedTX(unsigned_tx)

    # Sign transaction
    signed_tx = ergo.signTransaction(unsigned_tx, mnemonic[0], prover_index)

    return ergo.txId(signed_tx)

@initialize_jvm
def create_nft(ergo: appkit.ErgoAppKit, nft_name: str, description: str, image_link: str, image_hash: bytes,
              wallet_mnemonic: str, receiver_addresses: str = None,
              mnemonic_password: str = None, amount: list = None,
              sender_address: str = None, prover_index: int = None, base64reduced: bool = None):
    amount = [0.0002] if amount is None else amount
    
    # Get mnemonic
    mnemonic = ergo.getMnemonic(wallet_mnemonic=wallet_mnemonic, mnemonic_password=mnemonic_password)

    # Get sender address
    sender_address = (ergo.getSenderAddress(index=0, wallet_mnemonic=mnemonic[1], wallet_password=mnemonic[2])) \
        if sender_address is None \
        else ergo.castAddress(sender_address)
    
    # Get receiver addresses if given
    # Otherwise yourself
    receiver_addresses = sender_address if receiver_addresses is None else ergo.castAddress(receiver_addresses)

    # Build NFT
    input_box = ergo.getInputBox(amount_list=amount, sender_address=sender_address)
    nft = ergo.NFTbuilder(input_box, nft_name, description, image_link, image_hash)
    out_box = ergo.nftOutBox(nft, amount, receiver_addresses)
    
    # Build transaction
    unsigned_tx = ergo.buildUnsignedTransaction(input_box=input_box, outBox=out_box, sender_address=sender_address)
    
    if base64reduced:
        return ergo.getBase64ReducedTX(unsigned_tx)
    
    # Sign transaction
    signed_tx = ergo.signTransaction(unsigned_tx, mnemonic[0], prover_index)
    
    return ergo.txId(signed_tx)

@initialize_jvm
def create_token(ergo: appkit.ErgoAppKit, token_name: str, description: str, token_amount: int, token_decimals: int,
                wallet_mnemonic: str, receiver_addresses: str = None,
                mnemonic_password: str = None, amount: list = None,
                sender_address: str = None, prover_index: int = None, base64reduced: bool = None):
    amount = [0.0001] if amount is None else amount

    # Get mnemonic
    mnemonic = ergo.getMnemonic(wallet_mnemonic=wallet_mnemonic, mnemonic_password=mnemonic_password)
    
    # Get sender address
    sender_address = (ergo.getSenderAddress(index=0, wallet_mnemonic=mnemonic[1], wallet_password=mnemonic[2])) \
        if sender_address is None \
        else ergo.castAddress(sender_address)

    # Get receiver address
    receiver_addresses = sender_address \
        if receiver_addresses is None \
        else ergo.castAddress(receiver_addresses)

    input_box = ergo.getInputBox(amount_list=amount, sender_address=sender_address)

    # Mint token
    outBox = ergo.tokenMinterOutBox(input_box, token_name, description,
        token_amount, token_decimals, amount, receiver_addresses)

    # Build transaction
    unsigned_tx = ergo.buildUnsignedTransaction(input_box=input_box, outBox=outBox, sender_address=sender_address)

    if base64reduced:
        return ergo.getBase64ReducedTX(unsigned_tx)
    
    # Sign transaction
    signed_tx = ergo.signTransaction(unsigned_tx, mnemonic[0], prover_index)

    return ergo.txId(signed_tx)

import json
import jpype
from ergpy import appkit


def initializeJVM():
    try:
        jpype.addClassPath('ergo.jar')
        jpype.startJVM()
    except OSError:
        pass


def getWalletAddress(ergo: appkit.ErgoAppKit, amount: int, walletMnemonic: str, mnemonicPassword: str = None):
    initializeJVM()
    mnemonic = ergo.getMnemonic(walletMnemonic=walletMnemonic, mnemonicPassword=mnemonicPassword)
    addresses = []
    for x in range(amount):
        addresses.append(str(ergo.getSenderAddress(x, mnemonic[1], mnemonic[2])))
    return json.dumps(addresses)


def getBoxInfo(ergo: appkit.ErgoAppKit, index: int, senderAddress: str):
    initializeJVM()
    amount = [1]
    senderAddress = ergo.castAddress(senderAddress)
    inputBox = ergo.getInputBox(amountList=amount, senderAddress=senderAddress)
    return ergo.getBoxInfo(inputBox, index)


def simpleSend(ergo: appkit.ErgoAppKit, amount: list, receiverAddresses: list, walletMnemonic: str,
               mnemonicPassword: str = None,
               senderAddress: str = None, proverIndex: int = None, base64reduced: bool = None):
    initializeJVM()
    mnemonic = ergo.getMnemonic(walletMnemonic=walletMnemonic, mnemonicPassword=mnemonicPassword)
    if senderAddress is None:
        senderAddress = ergo.getSenderAddress(index=0, walletMnemonic=mnemonic[1], walletPassword=mnemonic[2])
    else:
        senderAddress = ergo.castAddress(senderAddress)
    inputBox = ergo.getInputBox(amountList=amount, senderAddress=senderAddress)
    outBox = ergo.buildOutBox(receiverWalletAddresses=receiverAddresses, amountList=amount)
    unsignedTX = ergo.buildUnsignedTransaction(inputBox=inputBox, outBox=outBox, senderAddress=senderAddress)
    if base64reduced:
        return ergo.getBase64ReducedTX(unsignedTX)
    signedTX = ergo.signTransaction(unsignedTX, mnemonic[0], proverIndex)
    return ergo.txId(signedTX)


def sendToken(ergo: appkit.ErgoAppKit, amount: list, receiverAddresses: list, tokens: list, walletMnemonic: str,
              mnemonicPassword: str = None,
              senderAddress: str = None, proverIndex: int = None, base64reduced: bool = None):
    initializeJVM()
    mnemonic = ergo.getMnemonic(walletMnemonic=walletMnemonic, mnemonicPassword=mnemonicPassword)
    if senderAddress is None:
        senderAddress = ergo.getSenderAddress(index=0, walletMnemonic=mnemonic[1], walletPassword=mnemonic[2])
    else:
        senderAddress = ergo.castAddress(senderAddress)
    inputBox = ergo.getInputBox(amountList=amount, senderAddress=senderAddress)
    outBox = ergo.tokenOutBox(receiverWalletAddresses=receiverAddresses, amountList=amount, tokens=tokens)
    unsignedTX = ergo.buildUnsignedTransaction(inputBox=inputBox, outBox=outBox, senderAddress=senderAddress)
    if base64reduced:
        return ergo.getBase64ReducedTX(unsignedTX)
    signedTX = ergo.signTransaction(unsignedTX, mnemonic[0], proverIndex)
    return ergo.txId(signedTX)


def createNFT(ergo: appkit.ErgoAppKit, nftName: str, description: str, imageLink: str, imageHash: bytes,
              walletMnemonic: str, receiverAddresses: str = None,
              mnemonicPassword: str = None, amount: list = None,
              senderAddress: str = None, proverIndex: int = None, base64reduced: bool = None):
    initializeJVM()
    if amount is None: amount = [0.0001]
    mnemonic = ergo.getMnemonic(walletMnemonic=walletMnemonic, mnemonicPassword=mnemonicPassword)
    if senderAddress is None:
        senderAddress = (ergo.getSenderAddress(index=0, walletMnemonic=mnemonic[1], walletPassword=mnemonic[2]))
    else:
        senderAddress = ergo.castAddress(senderAddress)
    if receiverAddresses is None:
        receiverAddresses = senderAddress
    else:
        receiverAddresses = ergo.castAddress(receiverAddresses)
    inputBox = ergo.getInputBox(amountList=amount, senderAddress=senderAddress)
    nft = ergo.NFTbuilder(inputBox, nftName, description, imageLink, imageHash)
    outBox = ergo.nftOutBox(nft, amount, receiverAddresses)
    unsignedTX = ergo.buildUnsignedTransaction(inputBox=inputBox, outBox=outBox, senderAddress=senderAddress)
    if base64reduced:
        return ergo.getBase64ReducedTX(unsignedTX)
    signedTX = ergo.signTransaction(unsignedTX, mnemonic[0], proverIndex)
    return ergo.txId(signedTX)


def createToken(ergo: appkit.ErgoAppKit, tokenName: str, description: str, tokenAmount: int, tokenDecimals: int,
                walletMnemonic: str, receiverAddresses: str = None,
                mnemonicPassword: str = None, amount: list = None,
                senderAddress: str = None, proverIndex: int = None, base64reduced: bool = None):
    initializeJVM()
    if amount is None: amount = [0.0001]
    mnemonic = ergo.getMnemonic(walletMnemonic=walletMnemonic, mnemonicPassword=mnemonicPassword)
    if senderAddress is None:
        senderAddress = (ergo.getSenderAddress(index=0, walletMnemonic=mnemonic[1], walletPassword=mnemonic[2]))
    else:
        senderAddress = ergo.castAddress(senderAddress)
    if receiverAddresses is None:
        receiverAddresses = senderAddress
    else:
        receiverAddresses = ergo.castAddress(receiverAddresses)
    inputBox = ergo.getInputBox(amountList=amount, senderAddress=senderAddress)
    outBox = ergo.tokenMinterOutBox(inputBox, tokenName, description, tokenAmount, tokenDecimals, amount,
                                    receiverAddresses)
    unsignedTX = ergo.buildUnsignedTransaction(inputBox=inputBox, outBox=outBox, senderAddress=senderAddress)
    if base64reduced:
        return ergo.getBase64ReducedTX(unsignedTX)
    signedTX = ergo.signTransaction(unsignedTX, mnemonic[0], proverIndex)
    return ergo.txId(signedTX)
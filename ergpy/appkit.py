import hashlib
import base64
import requests
import jpype.imports

# End of normal python imports
try:
    jpype.addClassPath('ergo.jar')
    jpype.startJVM()
except OSError:
    pass

# Everything below is java imports
from jpype import *
import java.lang

from org.ergoplatform.appkit import *

from org.ergoplatform.appkit.impl import *


# End of java imports

# to get the stubs (code completion) run: python -m stubgenj --convert-strings --classpath "ergo.jar" org.ergoplatform java

def stringHasher(string):
    bytes = bytearray(string, 'utf-8')
    return hashlib.sha256(bytes).digest()


def sha256caster(string):
    return bytes.fromhex(string)


def fileHasher(filename):
    with open(filename, "rb") as f:
        bytes = f.read()  # read entire file as bytes
        return bytearray(hashlib.sha256(bytes).hexdigest())


def getNodeInfo(nodeURL):
    # client = ApiClient(self._nodeURL)
    # api = client.createService(InfoApi.class)
    try:
        return requests.get(f'{nodeURL}/info').json()['network']
    except Exception as e:
        return requests.get(f'{nodeURL}info').json()['network']


@JImplements(java.util.function.Function)
class TripExecutor(object):
    @JOverride
    def apply(self, blockchain_context) -> BlockchainContext:
        return blockchain_context


class ErgoAppKit:

    def __init__(self, nodeURL):
        network = getNodeInfo(nodeURL)
        if network.lower() == 'mainnet':
            self._networkType = NetworkType.MAINNET
        else:
            self._networkType = NetworkType.TESTNET

        node_client = RestApiErgoClient.create(nodeURL, self._networkType, "",
                                               RestApiErgoClient.getDefaultExplorerUrl(self._networkType))
        self._nodeURL = nodeURL
        self._ctx = node_client.execute(TripExecutor().apply)

    def castAddress(self, address: str) -> Address:
        return Address.create(address)

    def getSenderAddress(self, index: int, walletMnemonic: SecretString, walletPassword: SecretString):
        return Address.createEip3Address(index, self._networkType, walletMnemonic, walletPassword)

    def getInputBox(self, amountList: list, senderAddress) -> InputBox:
        amountTotal = jpype.JLong(Parameters.OneErg * sum(amountList))
        return BoxOperations.createForSender(
            senderAddress,
            self._ctx).withAmountToSpend(amountTotal) \
            .withInputBoxesLoader(ExplorerAndPoolUnspentBoxesLoader()).loadTop()

    def getBoxInfo(self, box, index):
        return box.get(index).getId().toString()

    def NFTbuilder(self, inputBox, name, description, imageLink, sha256):
        return Eip4TokenBuilder.buildNftPictureToken(
            inputBox.get(0).getId().toString(),
            1, name,
            description, 0,
            JByte[:](sha256),
            imageLink)

    def nftOutBox(self, nft, amountList: list, receiverWalletAddress: Address):
        amountTotal = jpype.JLong(Parameters.OneErg * amountList[0])
        tb = self._ctx.newTxBuilder()
        return [tb.outBoxBuilder()
                    .value(amountTotal)
                    .mintToken(nft)
                    .contract(
            ErgoTreeContract(receiverWalletAddress.getErgoAddress().script(), self._networkType))
                    .build()]

    def tokenMinterOutBox(self, inputBox, tokenName, tokenDescription, tokenAmount, tokenDecimals, amountList: list,
                          receiverWalletAddress: Address):
        token = Eip4Token(inputBox.get(0).getId().toString(), tokenAmount, tokenName, tokenDescription, tokenDecimals)
        amountTotal = jpype.JLong(Parameters.OneErg * amountList[0])
        tb = self._ctx.newTxBuilder()
        return [tb.outBoxBuilder()
                    .value(amountTotal)
                    .mintToken(token)
                    .contract(
            ErgoTreeContract(receiverWalletAddress.getErgoAddress().script(), self._networkType))
                    .build()]

    def buildOutBox(self, receiverWalletAddresses: list, amountList: list):
        addresses = []
        outBox = []
        amountCounter = 0
        for x in receiverWalletAddresses:
            addresses.append(Address.create(x))
        tb = self._ctx.newTxBuilder()
        for j in addresses:
            ergo = jpype.JLong(Parameters.OneErg * amountList[amountCounter])
            box = tb.outBoxBuilder() \
                .value(ergo) \
                .contract(ErgoTreeContract(j.getErgoAddress().script(), self._networkType)) \
                .build()
            outBox.append(box)
            amountCounter += 1
        return outBox

    def tokenOutBox(self, receiverWalletAddresses: list, amountList: list, tokens: list, amountTokens: list = None):
        addresses = []
        outBox = []
        amountCounter = 0
        tokenAmountCounter = 0
        tList = []
        tokenList = []

        if amountTokens is None:
            for token in tokens:
                for x in token:
                    tList.append(ErgoToken(x, 1))
                tokenList.append(tList)
                tList = []
        else:
            for token in tokens:
                amountTokens = amountTokens[tokenAmountCounter]
                for x in token:
                    tokensToSend = amountTokens[tokenAmountCounter]
                    tList.append(ErgoToken(x, tokensToSend))
                tokenList.append(tList)
                tList = []
                tokenAmountCounter += 1

        for x in receiverWalletAddresses:
            addresses.append(Address.create(x))
        tb = self._ctx.newTxBuilder()
        for j in addresses:
            ergo = jpype.JLong(Parameters.OneErg * amountList[amountCounter])
            box = tb.outBoxBuilder() \
                .value(ergo) \
                .tokens(tokenList[amountCounter]) \
                .contract(ErgoTreeContract(j.getErgoAddress().script(), self._networkType)) \
                .build()
            outBox.append(box)
            amountCounter += 1
        return outBox

    def buildUnsignedTransaction(self, inputBox: InputBox, outBox: list, senderAddress) -> UnsignedTransaction:
        tb = self._ctx.newTxBuilder()
        return tb.boxesToSpend(inputBox) \
            .outputs(outBox) \
            .fee(Parameters.MinFee) \
            .sendChangeTo(senderAddress.asP2PK()) \
            .build()

    def getBase64ReducedTX(self, UnsignedTx: UnsignedTransaction):
        reducedTx = self._ctx.newProverBuilder().build().reduce(UnsignedTx, 0)
        return base64.urlsafe_b64encode(reducedTx.toBytes()).decode('utf-8')

    def getMnemonic(self, walletMnemonic, mnemonicPassword=None):
        if mnemonicPassword is None:
            mnemonicPassword = ""
        wM: SecretString = SecretString.create(str(walletMnemonic))
        wP: SecretString = SecretString.create(str(mnemonicPassword))
        WMnemonic: Mnemonic = Mnemonic.create(wM, wP)
        return WMnemonic, wM, wP

    def signTransaction(self, unsignedTX: UnsignedTransaction, WMnemonic: Mnemonic,
                        proverIndex: int = None) -> SignedTransaction:
        if proverIndex is None: proverIndex = 0
        prover = self._ctx.newProverBuilder().withMnemonic(WMnemonic).withEip3Secret(proverIndex).build()
        return prover.sign(unsignedTX)

    def txId(self, signedTX):
        return self._ctx.sendTransaction(signedTX).replace('"', '')

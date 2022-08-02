"""
Application KIT
==============================

Appkit Version 4.0.10

AUTHOR
    mgpai22@GitHub

CREATED AT
    Wed. 20 Apr. 2022 23:43
"""
# Import python packages
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

# Import java packages
from jpype import *
import java.lang

from org.ergoplatform.appkit import *
from org.ergoplatform.appkit.impl import *


# Notice:
# In order to get the stubs (code completion) run : 
# python -m stubgenj --convert-strings --classpath "ergo.jar" org.ergoplatform java

def string_hasher(string: str) -> bytes:
    """Hash a given string according to SHA256 algorithm and returns a bytes object"""
    bytes = bytearray(string, 'utf-8')
    return hashlib.sha256(bytes).digest()


def sha256caster(string) -> bytes:
    """Returns a bytes object from a sha256 hash."""
    return bytes.fromhex(string)


def file_hasher(filename):
    with open(filename, "rb") as f:
        bytes = f.read()  # read entire file as bytes
        return bytearray(hashlib.sha256(bytes).hexdigest())


def get_node_info(node_url):
    """Return information about the Node from given url.
    
    Ref:
    ```
    client = ApiClient(self._nodeUrl)
    api = client.createService(InfoApi.class)
    ```
    """
    try:
        return requests.get(f'{node_url}/info').json()['network']
    except Exception as e:
        return requests.get(f'{node_url}info').json()['network']


@JImplements(java.util.function.Function)
class TripExecutor(object):
    @JOverride
    def apply(self, blockchain_context) -> BlockchainContext:
        return blockchain_context


def tokenOutBoxList(tokens: list):
    token_list = [ErgoToken(token, 1) for token in tokens]
    return token_list


def get_outputs_to_spend(signed_tx: SignedTransaction, index_for_outbox=None, asArray=None):
    if index_for_outbox is None:
        if asArray is False:
            return signed_tx.getOutputsToSpend()
        return java.util.ArrayList([signed_tx.getOutputsToSpend()])
    if asArray is False:
        return signed_tx.getOutputsToSpend().get(index_for_outbox)
    return java.util.ArrayList([signed_tx.getOutputsToSpend().get(index_for_outbox)])


def getBoxInfo(box, index) -> str:
    """Get information box information."""
    return box \
        .get(index) \
        .getId() \
        .toString()


def readable_box(boxes: list):
    readable = []
    for box in boxes:
        x = str(box.get(0).getId())
        print("box id:", x)
        readable.append(x)
    return readable


class ErgoAppKit:
    """AppKit class to interact with Ergo blockchain."""

    def __init__(self, node_url):
        """Natural constructor for ErgoAppKit"""
        # Get node information
        network = get_node_info(node_url)

        # Check if node is on MainNet or TestNet
        self._networkType = NetworkType.MAINNET if network.lower() == 'mainnet' else NetworkType.TESTNET

        # Setup Node Client
        node_client = RestApiErgoClient.create(
            node_url,
            self._networkType,
            "",
            RestApiErgoClient.getDefaultExplorerUrl(self._networkType)
        )

        # Initialize attributes
        self._node_url = node_url
        self._ctx = node_client.execute(TripExecutor().apply)

    def castAddress(self, address: str) -> Address:
        """Create Ergo Address from base58 string."""
        return Address.create(address)

    def getSenderAddress(self, index: int, wallet_mnemonic: SecretString, wallet_password: SecretString):
        """Create an Eip3Address from given mnemonic phrase and mnemonic password."""
        return Address.createEip3Address(index, self._networkType, wallet_mnemonic, wallet_password)

    def getInputBox(self, amount_list: list, sender_address, tokenList) -> InputBox:
        """TODO Complete documentation"""
        amount_total = jpype.JLong(Parameters.OneErg * sum(amount_list))
        if tokenList is None:
            token_list = java.util.ArrayList([])
        else:
            token_list = java.util.ArrayList([])
            for token in tokenList:
                for x in token:
                    token_list.add(ErgoToken(x, 1))

        return BoxOperations \
            .createForSender(sender_address, self._ctx) \
            .withAmountToSpend(amount_total) \
            .withTokensToSpend(token_list) \
            .withInputBoxesLoader(ExplorerAndPoolUnspentBoxesLoader()) \
            .loadTop()

    def getInputBoxCovering(self, amount_list: list, sender_address, tokenList: list = None,
                            amount_tokens: list = None):
        amount_total = jpype.JLong(Parameters.OneErg * (sum(amount_list) + 0.001))
        token_list = []
        token_amount_counter = 0
        if tokenList is None:
            token_list = java.util.ArrayList([])
        else:
            if amount_tokens is None:
                token_list = java.util.ArrayList([])
                for token in tokenList:
                    for x in token:
                        token_list.add(ErgoToken(x, 1))
            else:
                for token in tokenList:
                    amountTokens = amountTokens[token_amount_counter]
                    for x in token:
                        tokensToSend = amountTokens[token_amount_counter]
                        token_list.append(ErgoToken(x, tokensToSend))
                    token_amount_counter += 1
                token_list = java.util.ArrayList(token_list)
        return self._ctx.getCoveringBoxesFor(sender_address, amount_total, token_list).getBoxes()

    def NFTbuilder(self, input_box, name, description, image_link, sha256):
        """Mint a picture NFT token."""
        token_id: str = input_box.get(0).getId().toString()
        return Eip4TokenBuilder.buildNftPictureToken(
            token_id,
            1,
            name,
            description, 0,
            JByte[:](sha256),
            image_link
        )

    def nftOutBox(self, nft, amount_list: list, receiver_wallet_address: Address) -> list:
        """TODO Complete documentation"""
        amount_total = jpype.JLong(Parameters.OneErg * amount_list[0])
        tb = self._ctx.newTxBuilder()
        return [tb
                    .outBoxBuilder() \
                    .value(amount_total) \
                    .mintToken(nft) \
                    .contract(ErgoTreeContract(receiver_wallet_address.getErgoAddress().script(), self._networkType)) \
                    .build()
                ]

    def NFT_issuer_box(self, sender_address, amount_of_boxes, royalty_amount_in_percent):
        try:
            address = Address.create(sender_address)
        except Exception as e:
            address = sender_address
        outbox = []
        tb = self._ctx.newTxBuilder()
        for x in range(amount_of_boxes):
            box = tb.outBoxBuilder() \
                .value(jpype.JLong(0.002 * Parameters.OneErg)) \
                .contract(ErgoTreeContract(address.getErgoAddress().script(), self._networkType)) \
                .registers([ErgoValue.of(jpype.JInt(royalty_amount_in_percent * 10))]) \
                .build()
            outbox.append(box)
        return outbox
    
    def genesis_box(self, sender_address, amount_of_boxes, amount):
        try:
            address = Address.create(sender_address)
        except Exception as e:
            address = sender_address
        outbox = []
        tb = self._ctx.newTxBuilder()
        for x in range(amount_of_boxes):
            box = tb.outBoxBuilder() \
                .value(jpype.JLong(amount * Parameters.OneErg)) \
                .contract(ErgoTreeContract(address.getErgoAddress().script(), self._networkType)) \
                .build()
            outbox.append(box)
        return outbox

    def tokenMinterOutBox(self, input_box, token_name, token_description,
                          token_amount, token_decimals, amount_list: list,
                          receiver_wallet_address: Address):
        """TODO Complete documentation"""
        token = Eip4Token(input_box.get(0).getId().toString(), token_amount, token_name, token_description,
                          token_decimals)
        amount_total = jpype.JLong(Parameters.OneErg * amount_list[0])
        tb = self._ctx.newTxBuilder()
        return [tb
                    .outBoxBuilder() \
                    .value(amount_total) \
                    .mintToken(token) \
                    .contract(
            ErgoTreeContract(receiver_wallet_address.getErgoAddress().script(), self._networkType)
        ) \
                    .build() \
                ]

    def buildOutBox(self, receiver_wallet_addresses: list, amount_list: list):
        """TODO Complete documentation"""
        addresses = []
        out_box = []
        amount_counter = 0
        for x in receiver_wallet_addresses:
            addresses.append(Address.create(x))
        tb = self._ctx.newTxBuilder()
        for j in addresses:
            ergo = jpype.JLong(Parameters.OneErg * amount_list[amount_counter])
            box = tb.outBoxBuilder() \
                .value(ergo) \
                .contract(ErgoTreeContract(j.getErgoAddress().script(), self._networkType)) \
                .build()
            out_box.append(box)
            amount_counter += 1
        return out_box

    def tokenOutBox(self, receiver_wallet_addresses: list, amount_list: list, tokens: list, amount_tokens: list = None):
        """TODO Complete documentation"""
        addresses = []
        out_box = []
        amount_counter = 0
        token_amount_counter = 0
        token_list = []

        # TODO Complete documentation
        if amount_tokens is None:
            token_list = [[ErgoToken(x, 1) for x in token] for token in tokens]
        else:
            for token in tokens:
                amount_tokens = amount_tokens[token_amount_counter]
                tList = [ErgoToken(x, amount_tokens[token_amount_counter]) for x in token]
                token_list.append(tList)
                token_amount_counter += 1

        # TODO Complete documentation
        addresses = [Address.create(rw_address) for rw_address in receiver_wallet_addresses]
        tb = self._ctx.newTxBuilder()

        # TODO Complete documentation
        for j in addresses:
            ergo = jpype.JLong(Parameters.OneErg * amount_list[amount_counter])

            box = tb.outBoxBuilder() \
                .value(ergo) \
                .tokens(token_list[amount_counter]) \
                .contract(ErgoTreeContract(j.getErgoAddress().script(), self._networkType)) \
                .build()

            out_box.append(box)
            amount_counter += 1

        return out_box

    def buildUnsignedTransaction(self, input_box: InputBox, outBox: list, sender_address, fee=None) -> UnsignedTransaction:
        """Build an unsigned transaction."""
        if fee is None:
            fee = Parameters.OneErg
        else:
            fee = jpype.JLong(fee * Parameters.OneErg)
        return self._ctx.newTxBuilder() \
            .boxesToSpend(input_box) \
            .outputs(outBox) \
            .fee(fee) \
            .sendChangeTo(sender_address.asP2PK()) \
            .build()

    def buildUnsignedTransactionChained(self, input_box: [InputBox], outBox: list, sender_address,
                                        amount_list: list, tokens=None, issuer_box=None,
                                        royalty_amount_in_percent=None, fee=None) -> UnsignedTransaction:

        """Build an unsigned chained transaction."""
        if fee is None:
            fee = Parameters.OneErg
        else:
            fee = jpype.JLong(fee * Parameters.OneErg)
        tb = self._ctx.newTxBuilder()
        input_box1: InputBox = input_box[0]
        ergo = jpype.JLong((abs(input_box1.getValue() - (Parameters.OneErg * (sum(amount_list) + 0.001)))))
        if tokens:
            t_list = []
            for i in range(len(input_box1.getTokens())):
                token = input_box1.getTokens().get(i).getId()
                t_list.append(token)
            tokens = tokenOutBoxList(t_list)
            tokens.pop(0)
            box = tb.outBoxBuilder() \
                .value(ergo) \
                .tokens(tokens) \
                .contract(ErgoTreeContract(sender_address.getErgoAddress().script(), self._networkType)) \
                .build()
        else:
            box = tb.outBoxBuilder() \
                .value(ergo) \
                .contract(ErgoTreeContract(sender_address.getErgoAddress().script(), self._networkType)) \
                .build()
        if issuer_box:
            if royalty_amount_in_percent is None:
                royalty_amount_in_percent = 5
            box = tb.outBoxBuilder() \
                .value(ergo) \
                .registers([ErgoValue.of(jpype.JInt(royalty_amount_in_percent * 10))]) \
                .contract(ErgoTreeContract(sender_address.getErgoAddress().script(), self._networkType)) \
                .build()
        outBox.insert(0, box)
        return self._ctx.newTxBuilder() \
            .boxesToSpend(input_box) \
            .outputs(outBox) \
            .fee(fee) \
            .sendChangeTo(sender_address.asP2PK()) \
            .build()

    def getBase64ReducedTX(self, unsigned_txx: UnsignedTransaction):
        """Reduce transaction to basae64."""
        reduced_tx = self._ctx \
            .newProverBuilder() \
            .build() \
            .reduce(unsigned_txx, 0)

        return base64 \
            .urlsafe_b64encode(reduced_tx.toBytes()) \
            .decode('utf-8')

    def getMnemonic(self, wallet_mnemonic, mnemonic_password=None):
        """Get mnemonic."""
        mnemonic_password = "" if mnemonic_password is None else mnemonic_password
        wM: SecretString = SecretString.create(str(wallet_mnemonic))
        wP: SecretString = SecretString.create(str(mnemonic_password))
        WMnemonic: Mnemonic = Mnemonic.create(wM, wP)
        return WMnemonic, wM, wP

    def signTransaction(self, unsigned_tx: UnsignedTransaction, w_mnemonic: Mnemonic,
                        prover_index: int = None) -> SignedTransaction:
        """Sign a transaction"""
        prover_index = 0 if prover_index is None else prover_index

        prover = self._ctx \
            .newProverBuilder() \
            .withMnemonic(w_mnemonic) \
            .withEip3Secret(prover_index) \
            .build()

        return prover.sign(unsigned_tx)

    def txId(self, signed_tx):
        """Send signed transaction."""
        return self._ctx \
            .sendTransaction(signed_tx) \
            .replace('"', '')
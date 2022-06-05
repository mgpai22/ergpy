
# ergpy 

A python-jvm wrapper for interacting with the Ergo blockchain.

# Usage

- Requires Java 8 or higher to be installed on system

```
pip install ergpy
```
- There are helper methods created to do simple transactions
    - Please checkout the `examples.py` (on github) to see how to use them.
    - `Simple Send` is available 
        - Allows sending ERG to one address or multiple addresses in ONE transactions
    -  `Get wallet addresses` is available
        - This gives derivations of wallet addresses given the mnemonic
        - If specified `2`, a list of two addresses will be printed in the console 
    - `Get Box Info` is available
        - Given the index and address, the selected box will be printed
    - `Send Token` is available
        - Allows sending token(s) to one or multiple addresses
        - The token id paramter must be given as a 2D array
        - Remember that tokens/nfts are seen as the same when transacting with them
    - `Create NFT` is available
        - Allows creating NFTs 
        - One mint is one transaction 
        - There are helper methods as well to get the sha-256 hash required while minting
            - `SHA256 caster`
                - Put the hash as a string and this will be converted into bytes
            - `String Hasher`
                - Input a string and this will be converted into a hash (only for testing purposes)
            - `File Hasher`
                - Input the file name and the hash will be generateed
    - `Create Token` is available
        - Allows a token to be minted
    - Custom
        - A bit more customization is available using methods from `appkit.py`
        - To truly have custom transactions `appkit.py` must be edited

## Github usage

```
git clone https://github.com/mgpai22/ergpy && cd ergpy
```
```
pip3 install -r requirements.txt
```
```
python -m stubgenj --convert-strings --classpath "./ergpy/ergo.jar" org.ergoplatform java
```
- If using an ide such as pycharm , make sure the root folder is ergpy
    - This allows code completion via stubgenj to work properly
- This method is recommended for developer as it allows for direction customizations in `appkit.py`

# Roadmap
- This is the begining of python support for Ergo! Contributions are essential for this to continue.
- Ergoscript support.
- Better documentation and packaging (first time creating a package).
    - Would love some help with this!

# Credits 

- [MrStahlfelge](https://github.com/ergoplatform/ergo-appkit/wiki/Using-Appkit-from-Python)
    - Showcased jpype usage with appkit
- [Ergopad](https://github.com/ergo-pad/ergopad-api/blob/nft-locked-vesting/app/ergo/appkit.py)
    - Borrowed/Modified some of their code

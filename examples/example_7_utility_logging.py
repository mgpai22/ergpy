"""
Example no.7
============

Example on how to use logging utility

AUTHOR
    rafidini@GitHub

CREATED AT
    Sun. 18 Jun. 2022
"""
# Packages
from ergpy import appkit, helper_functions
from ergpy.logs import setup_logs_env, logging

# Constants
NODE_URL: str = "https://pai-net.mempoolnode.live"
API_URL: str = "https://api.mempoolnode.live"

# Main
def main():
    # Initiate instance
    ergo = appkit.ErgoAppKit(node_url=NODE_URL, api_url=API_URL)
    logging.info(f"Connecting to node url: {NODE_URL}")

    # Transaction data
    wallet_mnemonic = "decline reward asthma enter three clean borrow repeat identify wisdom horn pull entire adapt neglect"
    receiver_addresses = ["3WwdXmYP39DLmDWJ6grH9ArXbWuCt2uGAh46VTfeGPrHKJJY6cSJ"]
    amount = [0.22]
    tx = ""

    # Begin transaction
    try:
        logging.info("simple_send in progress...")
        tx = helper_functions.simple_send(ergo=ergo, amount=amount, wallet_mnemonic=wallet_mnemonic,
                                          receiver_addresses=receiver_addresses, base64reduced=True)
        logging.info("simple_send done")
    except Exception as e:
        logging.error("Error: %s", e)
    finally:
        logging.info("JVM shutdown in progress...")
        logging.info("JVM shutdown done")

    # Save trasaction
    data = f'Transaction: {str(tx)}'
    logging.info(data)
    outfile = 'demo.text'
    with open(outfile, 'w') as file:
        file.write(data)
    logging.info(f"Wrote to file: {outfile}")
    helper_functions.exit()

if __name__ == "__main__":
    setup_logs_env()
    main()


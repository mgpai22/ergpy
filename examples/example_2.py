import logging
from ergpy import helper_functions, appkit

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@helper_functions.initialize_jvm
def main():
    node_url: str = "http://213.239.193.208:9052/"  # MainNet or TestNet
    ergo = appkit.ErgoAppKit(node_url=node_url)
    wallet_mnemonic = "what stadium typical spell rate truly pen tongue fuel intact fluid strike vibrant city shine"
    receiver_addresses = [
        "3WwdXmYP39DLmDWJ6grH9ArXbWuCt2uGAh46VTfeGPrHKJJY6cSJ",
        "3WwuG9amNVDwkJdgT5Ce7aJCfeoafVmd9tag9AEiAZwgPi7pYX3w",
        "3Wxk5oofZ3Laq2CpFW4Fi9YQiaep9bZr6QFg4s4xpzz4bi9tZq2U"
    ]
    amount = [0.22, 0.33, 0.11]
    tx = ""

    try:
        logging.info("simple_send in progress...")
        tx = helper_functions.simple_send(ergo=ergo, amount=amount, wallet_mnemonic=wallet_mnemonic, receiver_addresses=receiver_addresses)
        logging.info("simple_send done")
    except Exception as e:
        logging.error("Error: %s", e)
    finally:
        logging.info("JVM shutdown in progress...")
        logging.info("JVM shutdown done")
    
    data = f'Transaction: {str(tx)}'
    with open('demo.text', 'w') as file:
        file.write(data)
    logging.info("wrote to file")

if __name__ == "__main__":
    main()


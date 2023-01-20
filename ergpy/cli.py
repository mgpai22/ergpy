# Packages
import typing
import click
import ergpy.helper_functions as ergpy_help


# Constants
OPTION_NODE_URL: dict = {
    'envvar':'NODE_URL',
    'type':click.STRING,
    'default':'http://213.239.193.208:9052/',
    'help':'MainNet or TestNet'
}
OPTION_WALLET_MNEMONIC: dict = {
    'type': click.STRING,
    'help': 'Wallet mnemonic'
}
OPTION_MNEMONIC_PASSWORD: dict = {
    'type': click.STRING,
    'default': None,
    'help':'Password for the mnemonic'
}
OPTION_AMOUNT: dict = {
    'type': click.INT,
    'help': 'Amount of addresses'
}
OPTION_INDEX = {
    'type': click.INT,
    'help': 'Index'
}
OPTION_SENDER_ADDRESS: dict = {
    'type': click.STRING,
    'help': 'Address of the sender'
}


# Utils
def secho_iterable(iterable: typing.Iterable, color: str='blue'):
    """Specific echo for iterables (list, tuples...)"""
    for element in iterable:
        click.secho(f'-> {element}', fg=color)

def make_ergo(node_url: str) -> typing.Union[ergpy_help.appkit.ErgoAppKit, None]:
    """Create the appkit connected with the blockchain"""
    try:
        ergo = ergpy_help.appkit.ErgoAppKit(node_url=node_url)
        click.secho(f'Connection established!', fg='green')
        return ergo
    except TimeoutError:
        click.secho(f'Timeout while connecting to {node_url}', fg='red')
        return None
    except Exception as e:
        click.secho(f'Failed connecting to {node_url} : {e}', fg='red')
        return None
    

# Main command
@click.group()
def cli():
    """
    ergpy official CLI
    """
    pass

# Get subcommands
@cli.group()
def get():
    """Retrieve information about wallet address, box info..."""
    pass

# Send subcommands
@cli.group()
def send():
    """simple send or send token"""
    click.echo('Send what ?')

# Create subcommands
@cli.group()
def create():
    """create issuer box, NFT, token..."""
    click.echo('Create what ?')


# Commands
@click.command()
@click.option('--amount', **OPTION_AMOUNT)
@click.option('--wallet-mnemonic', **OPTION_WALLET_MNEMONIC)
@click.option('--mnemonic-password', **OPTION_MNEMONIC_PASSWORD)
@click.option('--node-url', **OPTION_NODE_URL)
def wallet_address(node_url: str, amount: int, wallet_mnemonic: str, mnemonic_password: str = None):
    """Retrieve informations about (a) wallet address(es)."""
    click.secho(f'You selected : Get (a) wallet address(es)', fg='blue')
    click.echo(f'Connecting to blockchain @ {node_url}')

    # Trying to connect w/ blockchain
    ergo: ergpy_help.appkit.ErgoAppKit = make_ergo(node_url=node_url)
    if ergo is None:
        return

    # Launch operation
    click.echo(f'Retrieving wallet address(es)')
    try:
        wallet_address = ergpy_help.get_wallet_address(ergo, amount, wallet_mnemonic, mnemonic_password)
        click.echo(f'Wallet address(es)')
        secho_iterable(wallet_address)
    except Exception as e:
        click.secho(f'Failed to retrieve wallet address(es) : {e}', fg='red')

@click.command()
@click.option('--node-url', **OPTION_NODE_URL)
@click.option('--index', **OPTION_INDEX)
@click.option('--sender-address', **OPTION_SENDER_ADDRESS)
def box_info(node_url: str, index: int, sender_address: str, tokens: list = None):
    """Retrieve informations about box."""
    click.secho(f'You selected : Get box informations', fg='blue')
    click.echo(f'Connecting to blockchain @ {node_url}')

    # Trying to connect w/ blockchain
    ergo: ergpy_help.appkit.ErgoAppKit = make_ergo(node_url=node_url)
    if ergo is None:
        return

    # Launch operation
    click.echo(f'Retrieving box informations')
    try:
        box_informations = ergpy_help.get_box_info(ergo, index, sender_address, tokens)
        click.echo(f'Box informations')
        secho_iterable(box_informations)
    except Exception as e:
        click.secho(f'Failed to retrieve wallet address(es) : {e}', fg='red')

def handle_cli():
    # Registering `get` commands
    get.add_command(wallet_address)
    get.add_command(box_info)

    # CLI
    cli()

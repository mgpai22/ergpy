# Packages
import typing
import click
import ergpy
import ergpy.helper_functions as ergpy_help


# Constants
OPTION__REQUIRED: dict = {'required': True}
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
OPTION_TOKENS: dict = {
    'type': click.STRING,
    'help': 'Tokens',
    'multiple': True
}
OPTION_AMOUNTS: dict = {
    'type': click.STRING,
    'help': 'Amounts',
    'multiple': True
}
OPTION_RECEIVER_ADDRESSESS: dict = {
    'type': click.STRING,
    'help': 'Addresses of receiver',
    'multiple': True
}
OPTION_PROVERINDEX: dict = {
    'type': click.INT,
    'help': 'Prover Index'
}
OPTION__BOOL: dict = {'type': click.BOOL}

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
@cli.command()
def version():
    """Show the current version of the package"""
    click.secho(f'ergpy {ergpy.__version__}', fg='blue')

@cli.group()
def get():
    """Retrieve information about wallet address, box info..."""
    pass

# Send subcommands
@cli.group()
def send():
    """simple send or send token"""
    pass

# Create subcommands
@cli.group()
def create():
    """create issuer box, NFT, token..."""
    click.echo('Create what ?')


# Commands
@click.command()
@click.option('--amount', **OPTION_AMOUNT, **OPTION__REQUIRED)
@click.option('--wallet-mnemonic', **OPTION_WALLET_MNEMONIC, **OPTION__REQUIRED)
@click.option('--mnemonic-password', **OPTION_MNEMONIC_PASSWORD, **OPTION__REQUIRED)
@click.option('--node-url', **OPTION_NODE_URL, **OPTION__REQUIRED)
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
@click.option('--node-url', **OPTION_NODE_URL, **OPTION__REQUIRED)
@click.option('--index', **OPTION_INDEX, **OPTION__REQUIRED)
@click.option('--sender-address', **OPTION_SENDER_ADDRESS, **OPTION__REQUIRED)
@click.option('--tokens', **OPTION_TOKENS)
def box_info(node_url: str, index: int, sender_address: str, tokens: list=None):
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
        click.secho(f'Failed to retrieve box informations : {e}', fg='red')

@click.command()
@click.option('--node-url', **OPTION_NODE_URL, **OPTION__REQUIRED)
@click.option('--amounts', **OPTION_AMOUNTS, **OPTION__REQUIRED)
@click.option('--receiver-addresses', **OPTION_RECEIVER_ADDRESSESS, **OPTION__REQUIRED)
@click.option('--wallet-mnemonic', **OPTION_WALLET_MNEMONIC, **OPTION__REQUIRED)
@click.option('--mnemonic-password', **OPTION_MNEMONIC_PASSWORD, **OPTION__REQUIRED)
@click.option('--sender-address', **OPTION_SENDER_ADDRESS)
@click.option('--prover-index', **OPTION_PROVERINDEX)
@click.option('--base64reduced', **OPTION__BOOL)
@click.option('--input-box')
@click.option('--return-signed', **OPTION__BOOL)
@click.option('--chained', **OPTION__BOOL)
@click.option('--fee')
def simple(**kwargs: dict):
    """Simple send."""
    click.secho(f'You selected : Simple send', fg='blue')
    click.echo(f"Connecting to blockchain @ {kwargs.get('node_url')}")

    # Trying to connect w/ blockchain
    ergo: ergpy_help.appkit.ErgoAppKit = make_ergo(node_url=kwargs.get('node_url'))
    if ergo is None:
        return

    # Launch operation
    click.echo(f'Launch the simple send')
    try:
        transaction = ergpy_help.simple_send(ergo, **kwargs)
        click.echo(f'Transaction')
        click.secho(f'-> {transaction}', fg='blue')
    except Exception as e:
        click.secho(f'Failed to proceed with the transaction : {e}', fg='red')

@click.command()
@click.option('--node-url', **OPTION_NODE_URL, **OPTION__REQUIRED)
@click.option('--amounts', **OPTION_AMOUNTS, **OPTION__REQUIRED)
@click.option('--receiver-addresses', **OPTION_RECEIVER_ADDRESSESS, **OPTION__REQUIRED)
@click.option('--tokens', **OPTION_TOKENS, **OPTION__REQUIRED)
@click.option('--wallet-mnemonic', **OPTION_WALLET_MNEMONIC, **OPTION__REQUIRED)
@click.option('--input-box')
@click.option('--amount-tokens')
@click.option('--mnemonic-password', **OPTION_MNEMONIC_PASSWORD)
@click.option('--sender-address', **OPTION_SENDER_ADDRESS)
@click.option('--prover-index', **OPTION_PROVERINDEX)
@click.option('--base64reduced', **OPTION__BOOL)
@click.option('--return-signed', **OPTION__BOOL)
@click.option('--chained', **OPTION__BOOL)
@click.option('--fee')
def token(**kwargs):
    """Send token."""
    click.secho(f'You selected : Send token', fg='blue')
    click.echo(f"Connecting to blockchain @ {kwargs.get('node_url')}")

    # Trying to connect w/ blockchain
    ergo: ergpy_help.appkit.ErgoAppKit = make_ergo(node_url=kwargs.get('node_url'))
    if ergo is None:
        return

    # Launch operation
    click.echo(f'Launch the send token operation')
    try:
        transaction = ergpy_help.send_token(ergo, **kwargs)
        click.echo(f'Transaction')
        click.secho(f'-> {transaction}', fg='blue')
    except Exception as e:
        click.secho(f'Failed to proceed with the transaction : {e}', fg='red')

def handle_cli():
    # Registering `get` commands
    get.add_command(wallet_address)
    get.add_command(box_info)

    # Registering `send` commands
    send.add_command(simple)
    send.add_command(token)

    # CLI
    cli()

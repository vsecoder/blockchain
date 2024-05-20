from fastapi import APIRouter
from app.blockchain import Coin
import os, json
import logging
import coloredlogs
from datetime import datetime
from app.config import parse_config


logger = logging.getLogger(__name__)
coloredlogs.install(level=logging.INFO)

if not os.path.exists(os.getcwd() + "/blockchain.json"):
    logger.info("Creating new blockchain")
    blockchain = Coin()
else:
    logger.info("Restoring blockchain")
    with open(os.getcwd() + "/blockchain.json", "r") as file:
        data = json.loads(file.read())
        blockchain = Coin(restore=True).from_dict(data)
router = APIRouter()

if not blockchain.validate_chain():
    raise Exception("Invalid chain")
else:
    logger.info("Chain is valid")

config = parse_config("config.toml").web.get_config()
SECRET_KEY = config["key"]


@router.post("/")
def create_wallet():
    """
    Create a new wallet
    """
    return blockchain.Wallet.create_wallet()


@router.get("/")
def get_balance(public_key: str, private_key: str):
    """
    Get the balance of a wallet

    :param public_key: str: Public key of the wallet
    :param private_key: str: Private key of the wallet
    """
    return blockchain.Wallet.get_balance(private_key, public_key)


@router.post("/transfer")
def transfer(from_: str, to: str, amount: float):
    """
    Transfer amount from one wallet to another

    :param from_: str: Private key of the sender (pve)
    :param to: str: Public key of the receiver (pbc)
    """
    try:
        transaction = blockchain.create_transaction(
            datetime.now(),
            data={
                "type": "token-transfer",
                "data": {"to": to, "from": from_, "amount": amount},
            },
        )
        return transaction
    except Exception as e:
        return {"error": str(e)}


@router.post("/credit")
def credit_wallet(public_key: str, amount: float, key: str):
    """
    Credit a wallet with an amount

    :param public_key: str: Public key of the wallet
    :param amount: float: Amount to credit
    :param key: str: Secret key

    :return: float: New balance
    """
    if key != SECRET_KEY:
        return {"error": "Invalid key"}
    return blockchain.Wallet.credit_wallet(public_key, amount)


@router.get("/public-key")
def get_public_key(private_key: str):
    """
    Get the public key of a private key

    :param private_key: str: Private key of the wallet

    :return: str: Public key
    """
    return blockchain.Wallet.get_public_key(private_key)


@router.get("/validate")
def validate_wallet(private_key: str, public_key: str):
    """
    Validate a wallet

    :param private_key: str: Private key of the wallet
    :param public_key: str: Public key of the wallet

    :return: bool: True if the wallet is valid, False if not
    """
    return blockchain.Wallet.validate_wallet(private_key, public_key)


@router.post("/nft")
def create_nft(name: str, description: str, url: str, owner: str):
    """
    Create a new NFT

    :param name: str: Name of the NFT
    :param description: str: Description of the NFT
    :param url: str: URL of the NFT
    :param owner: str: Public key of the owner
    """
    return blockchain.create_nft(
        datetime.now(),
        data={
            "type": "nft-create",
            "data": {
                "name": name,
                "description": description,
                "url": url,
                "owner": owner,
            },
        },
    )


@router.post("/nft-transfer")
def transfer_nft(nft: str, from_: str, to: str):
    """
    Transfer an NFT

    :param nft: str: ID of the NFT
    :param from_: str: Private key of the sender (pve)
    :param to: str: Public key of the receiver (pbc)
    """
    try:
        transaction = blockchain.transfer_nft(
            datetime.now(),
            data={
                "type": "nft-transfer",
                "data": {"nft": nft, "from": from_, "to": to},
            },
        )
        return transaction
    except Exception as e:
        return {"error": str(e)}


@router.get("/sync")
def sync(key: str):
    """
    Sync the blockchain
    """
    if key != SECRET_KEY:
        return {"error": "Invalid key"}
    blockchain.sync()
    return {"status": "success"}

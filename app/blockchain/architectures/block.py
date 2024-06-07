from .transaction import Transaction
from .wallet import Wallet
from .nft import NFT
import hashlib
from typing import Union
from datetime import datetime


class Block:
    """
    Block class for blockchain

    :param timestamp: float: Timestamp of the block
    :param transactions: list: List of transactions
    :param previous_hash: str: Hash of the previous block
    :param proof: int: Proof of work
    :param addresses: dict: Wallet addresses
    :param nft: list: List of NFTs
    """

    def __init__(
        self,
        timestamp,
        transactions: Union[str, list, None] = None,
        previous_hash: str = "",
        proof: int = 0,
        addresses: dict = None,
        nft: dict = None,
    ):
        if addresses is None:
            addresses = {}
        if nft is None:
            nft = {}

        self.addresses = addresses
        self.nft = nft
        self.timestamp = timestamp
        self.transactions = transactions if transactions else []
        self.previous_hash = previous_hash if previous_hash else ""
        self.hash = self.get_hash()
        self.proof = proof if proof else 0
        self.status = 0  # 0 = pending, 1 = completed
        self._complete()

    def _complete(self):
        for transaction in self.transactions:
            try:
                pbc = self.addresses.get_public_key(transaction.input["data"]["from"])
                pve = transaction.input["data"]["from"]
            except:
                pass

            if transaction == "genisis block":
                return

            if transaction.input["type"] == "token-transfer":
                if float(transaction.input["data"]["amount"]) >= 0:
                    if transaction.input["data"]["to"] == pbc:
                        return
                    if self.addresses.get_balance(pve, pbc) >= float(
                        transaction.input["data"]["amount"]
                    ):
                        self.addresses.credit_wallet(
                            transaction.input["data"]["to"],
                            float(transaction.input["data"]["amount"]),
                        )
                        self.addresses.credit_wallet(
                            pbc, -float(transaction.input["data"]["amount"])
                        )

            if transaction.input["type"] == "nft-transfer":
                nft = self.addresses.get_nft(transaction.input["data"]["nft"])
                from_ = transaction.input["data"]["from"]  # pve
                to_ = transaction.input["data"]["to"]  # pbc
                self.addresses.give_nft(to_, nft)
                self.addresses.take_nft(from_, nft)

            if transaction.input["type"] == "nft-create":
                if not self.nft:
                    self.nft = []
                nft = NFT(
                    transaction.input["data"]["name"],
                    transaction.input["data"]["description"],
                    transaction.input["data"]["url"],
                    transaction.input["data"]["owner"],
                    transaction.timestamp,
                )
                self.nft.append(nft)
                self.addresses.give_nft(transaction.input["data"]["owner"], nft)

        self.status = 1

    def get_hash(self) -> str:
        return hashlib.sha256(
            str(self.timestamp).encode("utf-8")
            + str(self.transactions).encode("utf-8")
            + str(self.previous_hash).encode("utf-8")
        ).hexdigest()

    """
    ---
    In development

    convert the block to a dict and dict to a block
    used for syncing the blockchain to a file
    """

    def to_dict(self) -> dict:
        transactions = []
        for transaction in self.transactions:
            if type(transaction) != str:
                transactions.append(transaction.to_dict())
            else:
                transactions.append(transaction)

        obj = {
            "timestamp": self.timestamp,
            "transactions": transactions,
            "addresses": self.addresses.to_dict() if self.addresses else "",
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "status": self.status,
            "nft": [nft.to_dict() for nft in self.nft] if self.nft else "",
            "proof": self.proof if self.proof else 0,
        }

        return obj

    def from_dict(self, obj) -> object:
        # reinit addresses
        self.addresses = Wallet()
        self.addresses.from_dict(obj["addresses"])

        self.timestamp = obj["timestamp"]

        # reinit transactions
        for transaction in obj["transactions"]:
            if type(transaction) != str:
                transaction_class = Transaction(
                    datetime.fromtimestamp(transaction["timestamp"]), None
                )
                self.transactions.append(transaction_class.from_dict(transaction))
            else:
                self.transactions.append(transaction)

        # reinit nft
        self.nft = []
        for nft in obj["nft"]:
            nft_class = NFT(
                nft["name"],
                nft["description"],
                nft["url"],
                nft["owner"],
                nft["timestamp"],
            )
            self.nft.append(nft_class)

        self.previous_hash = obj["previous_hash"]
        self.hash = obj["hash"]
        self.status = obj["status"]
        self.proof = obj["proof"]
        return self

from .transaction import Transaction
from .wallet import Wallet
import hashlib
from typing import Union
from datetime import datetime


class Block:
    """
    Block class for blockchain

    :param timestamp: float: Timestamp of the block
    :param transactions: list: List of transactions
    :param previous_hash: str: Hash of the previous block
    :param addresses: dict: Wallet addresses
    """

    def __init__(
        self,
        timestamp,
        transactions: Union[str, list] = [],
        previous_hash="",
        addresses="",
    ):
        self.addresses = addresses
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.get_hash()
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
                    datetime.fromtimestamp(transaction["timestamp"]),
                )
                self.transactions.append(transaction_class.from_dict(transaction))
            else:
                self.transactions.append(transaction)

        self.previous_hash = obj["previous_hash"]
        self.hash = obj["hash"]
        self.status = obj["status"]
        return self

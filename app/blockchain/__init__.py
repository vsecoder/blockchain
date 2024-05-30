from .architectures.blockchain import Blockchain
from .architectures.block import Block
from .architectures.wallet import Wallet
from .architectures.transaction import Transaction
from datetime import datetime
from typing import Union
import os, json, hashlib


class Coin:
    """
    Coin class, main class for the blockchain

    :param name: str: Name of the blockchain
    :param difficulty: int: Difficulty of the blockchain
    :param minimum_transactions: int: Minimum transactions required to create a block
    :param restore: bool: Restore the blockchain from the blockchain.json file
    """

    def __init__(
        self,
        name="Coin",
        difficulty=4,
        minimum_transactions=1,
        restore=False,
    ):
        self.coin = Blockchain(
            name=name,
            difficulty=difficulty,
            minimum_transactions=minimum_transactions,
        )
        if not restore:
            self.coin.chain.append(Block(datetime.now().timestamp(), ["genisis block"]))

        self.Wallet = Wallet()

    def validate_chain(self) -> bool:
        """
        Validate the chain of the blockchain

        :return: bool: True if the chain is valid, False if not
        """
        for i, chain in enumerate(self.coin.chain):
            if chain.transactions[0] != "genisis block":
                if chain.get_hash() != chain.hash:
                    return False

                if chain.previous_hash != self.coin.chain[i - 1].hash:
                    return False

        return True

    def _valid_proof(self, last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def _proof_of_work(self, last_proof) -> int:
        proof = 0
        while self._valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    def _create_block(self, addresses=None) -> Union[Block, bool]:
        if len(self.coin.pending_transactions) >= self.coin.minimum_transactions:
            # block.hash, block.timestamp, block.transactions, block.previous_hash
            transactions = self.coin.pending_transactions
            self.coin.pending_transactions = []
            block = Block(
                datetime.now().timestamp(),
                transactions,
                self.coin.chain[len(self.coin.chain) - 1].hash,
                self._proof_of_work(self.coin.chain[len(self.coin.chain) - 1].proof),
                addresses,
            )
            self.coin.chain.append(block)
            self.sync()
            return block

        self.sync()
        return False

    def create_transaction(self, timestamp, data) -> None:
        """
        Create a new transaction

        :param timestamp: float: Timestamp of the transaction
        :param data: dict: Data of the transaction

        :return: None
        """
        self.coin.pending_transactions.append(Transaction(timestamp, data=data))
        self._create_block(
            addresses=self.Wallet,
        )

    def get_transaction(self, data) -> Union[Transaction, None]:
        """
        Get a transaction by its hash

        :param data: str: Hash of the transaction

        :return: Transaction: Transaction object
        """
        for block in self.coin.chain:
            for transaction in block.transactions:
                if transaction.hash == data:
                    return transaction

    class Wallet(Wallet):
        # this class is a subclass of Wallet
        pass

    def to_dict(self) -> dict:
        return {
            "coin": [block.to_dict() for block in self.coin.chain],
            "Wallet": self.Wallet.to_dict(),
        }

    def sync(self) -> None:
        """
        Sync the blockchain to the blockchain.json file
        Work automatically when a block is created
        """
        with open(os.getcwd() + "/blockchain.json", "w") as file:
            json.dump(self.to_dict(), file)

    """
    ---
    In development

    convert the block to a dict and dict to a block
    used for syncing the blockchain to a file
    """

    def from_dict(self, data) -> object:
        self.coin.chain = []
        for block in data["coin"]:
            block_ = Block(0)
            block_.from_dict(block)
            self.coin.chain.append(block_)

        wallet = Wallet()
        self.Wallet = wallet.from_dict(data["Wallet"])
        return self

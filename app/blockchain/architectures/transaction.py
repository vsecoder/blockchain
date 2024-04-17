import hashlib


class Transaction:
    """
    Transaction class, needed for the blockchain

    :param timestamp: timestamp
    :param data: dict: Data of the transaction
    """

    def __init__(self, timestamp, data={}):
        self.timestamp = timestamp
        self.input = data
        self.hash = self.get_hash()

    def get_hash(self) -> str:
        return hashlib.sha256(
            str(self.timestamp).encode("utf-8") + str(self.input).encode("utf-8")
        ).hexdigest()

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.timestamp(),
            "input": self.input,
            "hash": self.hash,
        }

    def from_dict(self, obj) -> object:
        self.input = obj["input"]
        self.hash = obj["hash"]
        return self

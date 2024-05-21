class Blockchain:
    """
    Blockchain class

    :param name: str: Name of the blockchain
    :param difficulty: int: Difficulty of the blockchain
    :param minimum_transactions: int: Minimum transactions required to create a block
    """

    def __init__(self, name="", difficulty=2, minimum_transactions=2):
        self.name = name
        self.difficulty = difficulty
        self.minimum_transactions = minimum_transactions
        self.chain = []
        self.pending_transactions = []

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "difficulty": self.difficulty,
            "minimum_transactions": self.minimum_transactions,
            "chain": [block.to_dict() for block in self.chain],
            "pending_transactions": [
                transaction.to_dict() for transaction in self.pending_transactions
            ],
        }

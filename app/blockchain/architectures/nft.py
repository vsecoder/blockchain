import hashlib
import random


class NFT:
    def __init__(self, name, description, url, public_key, timestamp):
        identificator = random.randint(10000000, 9999999999)
        self.id = "0x" + str(
            hashlib.sha256(str(identificator).encode("utf-8")).hexdigest()
        )
        self.name = name
        self.description = description
        self.url = url
        self.owner = public_key
        self.timestamp = timestamp

    def get_hash(self) -> str:
        return hashlib.sha256(
            str(self.id).encode("utf-8")
            + str(self.name).encode("utf-8")
            + str(self.description).encode("utf-8")
            + str(self.url).encode("utf-8")
            + str(self.owner).encode("utf-8")
            + str(self.timestamp).encode("utf-8")
        ).hexdigest()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "owner": self.owner,
            "timestamp": self.timestamp.timestamp(),
            "hash": self.get_hash(),
        }

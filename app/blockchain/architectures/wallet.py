import hashlib, random
from typing import Union


class Wallet:
    """
    Wallet class, saves wallet addresses and balances

    :param addresses: list: List of wallet addresses
    """

    def __init__(self, addresses=None):
        self.addresses = [] if addresses == None else addresses

    def create_wallet(self) -> dict:
        """
        Create a new wallet address

        :return: dict: Wallet address
        """
        pve = random.randint(10000000, 9999999999)
        pbc = random.randint(10000000, 9999999999)
        private_key = str(hashlib.sha256(str(pve).encode("utf-8")).hexdigest())
        public_key = str(hashlib.sha256(str(pbc).encode("utf-8")).hexdigest())
        cred_keys = {
            "address": {"pve": private_key, "pbc": public_key},
            "info": {"balance": float(0)},
        }
        if self.validate_address(private_key, public_key) == False:
            self.addresses.append(cred_keys)
            return cred_keys
        else:
            return self.create_address()

    def get_balance(self, private_key=None, public_key=None) -> Union[float, str]:
        """
        Get the balance of a wallet address

        :param private_key: str: Private key of the wallet (pve)
        :param public_key: str: Public key of the wallet (pbc)

        :return: float: Balance of the wallet
        """
        r = self._require(private_key, public_key)
        if r == False:
            return "Private and Public keys are required"

        for address in self.addresses:
            if (
                address["address"]["pbc"] == public_key
                and address["address"]["pve"] == private_key
            ):
                return float(address["info"]["balance"])

    def get_public_key(self, private_key=None) -> str:
        """
        Get the public key of a wallet address

        :param private_key: str: Private key of the wallet (pve)

        :return: Public key of the wallet (pbc) or "Failed"
        """
        if private_key == None:
            return "Failed"

        for address in self.addresses:
            if address["address"]["pve"] == private_key:
                return address["address"]["pbc"]
        return "Failed"

    def credit_wallet(self, public_key=None, amount=None) -> Union[float, str]:
        """
        Credit a wallet address with an amount

        :param public_key: str: Public key of the wallet (pbc)
        :param amount: float: Amount to credit the wallet with

        :return: New balance of the wallet or "Failed"
        """
        if public_key == None or amount == None:
            return "Failed"

        for address in self.addresses:
            if address["address"]["pbc"] == public_key:
                address["info"]["balance"] += amount
                return address["info"]["balance"]
        return "Failed"

    def validate_address(self, private_key=None, public_key=None) -> Union[bool, str]:
        """
        Validate a wallet address

        :param private_key: str: Private key of the wallet (pve)
        :param public_key: str: Public key of the wallet (pbc)

        :return: True or False or "Private and Public keys are required"
        """
        r = self._require(private_key, public_key)
        if r == False:
            return "Private and Public keys are required"

        for address in self.addresses:
            if (
                address["address"]["pbc"] == public_key
                and address["address"]["pve"] == private_key
            ):
                return True
        return False

    def _require(self, private_key=None, public_key=None) -> bool:
        if private_key == None or public_key == None:
            return False
        return True

    def to_dict(self) -> list:
        return self.addresses

    def from_dict(self, obj) -> object:
        self.addresses = obj
        return self

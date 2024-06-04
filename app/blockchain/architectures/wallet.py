import hashlib, random
from typing import Union
from decimal import Decimal, getcontext
import copy


getcontext().prec = 10


class Wallet:
    """
    Wallet class, saves wallet addresses and balances

    :param addresses: list: List of wallet addresses
    """

    def __init__(self, addresses=None):
        self.addresses = [] if addresses is None else addresses

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
            "info": {"balance": float(0), "nfts": []},
        }
        if self.validate_address(private_key, public_key) == False:
            self.addresses.append(cred_keys)
            return cred_keys
        return self.create_address()

    def get_balance(self, private_key=None, public_key=None) -> Union[float, str]:
        """
        Get the balance of a wallet address

        :param private_key: str: Private key of the wallet (pve)
        :param public_key: str: Public key of the wallet (pbc)

        :return: float: Balance of the wallet
        """
        r = self._require(private_key, public_key)
        if r is False:
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
        if private_key is None:
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
        if public_key is None or amount is None:
            return "Failed"

        for address in self.addresses:
            if address["address"]["pbc"] == public_key:
                address["info"]["balance"] = float(
                    Decimal(address["info"]["balance"]) + Decimal(amount)
                )
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

    def get_nfts(self, public_key=None) -> list:
        """
        Get the NFTs of a wallet address

        :param public_key: str: Public key of the wallet (pbc)

        :return: list: List of NFTs or "Failed"
        """
        if public_key is None:
            return "Failed"

        for address in self.addresses:
            if address["address"]["pbc"] == public_key:
                return address["info"]["nfts"]
        return "Failed"

    def get_nft(self, nft_id=None) -> Union[dict, str]:
        """
        Get an NFT by its ID

        :param nft_id: str: ID of the NFT

        :return: NFT or "Failed"
        """
        if nft_id is None:
            return "Failed"

        for address in self.addresses:
            for nft in address["info"]["nfts"]:
                if nft.id is nft_id:
                    return nft
        return "Failed"

    def give_nft(self, public_key=None, nft=None) -> Union[list, str]:
        """
        Give an NFT to a wallet address

        :param public_key: str: Public key of the wallet (pbc)
        :param nft: dict: NFT to give

        :return: List of NFTs or "Failed"
        """
        if public_key is None or nft is None:
            return "Failed"

        for address in self.addresses:
            if address["address"]["pbc"] == public_key:
                address["info"]["nfts"].append(nft)
                return address["info"]["nfts"]
        return "Failed"

    def take_nft(self, private_key=None, nft=None) -> Union[list, str]:
        """
        Take an NFT from a wallet address

        :param private_key: str: Private key of the wallet (pve)
        :param nft: dict: NFT to take

        :return: List of NFTs or "Failed"
        """
        if private_key is None or nft is None:
            return "Failed"

        for address in self.addresses:
            if address["address"]["pve"] == private_key:
                for n in address["info"]["nfts"]:
                    if n.id == nft.id:
                        address["info"]["nfts"].remove(n)
                        return address["info"]["nfts"]
        return "Failed"

    def _require(self, private_key=None, public_key=None) -> bool:
        if private_key is None or public_key is None:
            return False
        return True

    def to_dict(self) -> list:
        addresses = copy.deepcopy(self.addresses)
        for address in addresses:
            if (
                address["info"]["nfts"] != []
                and type(address["info"]["nfts"][0]) != dict
            ):
                address["info"]["nfts"] = [
                    nft.to_dict() for nft in address["info"]["nfts"]
                ]

        return addresses

    def from_dict(self, obj) -> object:
        self.addresses = obj
        return self

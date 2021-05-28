from pprint import pprint
from models.sbps.Unit import Unit
from models.Upgrade import Upgrade


class Faction:

    def __init__(self, constname):
        self.constname = constname
        self.units = {}
        self.upgrades = {}

    def add_unit(self, unit: Unit) -> None:
        Faction._validate_no_duplicates(unit.constname, self.units)
        self.units[unit.constname] = unit

    def add_upgrade(self, upgrade: Upgrade) -> None:
        Faction._validate_no_duplicates(upgrade.constname, self.upgrades)
        self.upgrades[upgrade.constname] = upgrade

    @staticmethod
    def _validate_no_duplicates(constname, dictionary):
        if constname in dictionary:
            raise Exception(f"Unexpected duplicate constname '{constname}' in {pprint(dictionary)}")

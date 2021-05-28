import json

from FileUtils import FileUtils
from models.AbstractModel import AbstractModel


class Upgrade(AbstractModel):
    def __init__(self, constname, faction, filename, upgrade_json):
        super().__init__(upgrade_json)  # self.raw_json
        self.constname = constname
        self.faction = faction
        self.upgrade_filename = filename



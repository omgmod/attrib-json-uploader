from models.Faction import Faction
from services.AttribParserService import AttribParserService
from services.WarcpDataService import WarcpDataService
from utils.FileUtils import FileUtils

# Cleanup json

# FileUtils.clear_directory_of_filetype("./json", ".json")

# Copy over attrib jsons from ../attrib-parser/json
# FileUtils.copy_directory("../attrib-parser/json", "./json")

# Tables with CONSTNAME:

# factions
# doctrines

# doctrineabilities (docmarkers)

# units
# units_modified
# upgrades
# upgrades_modified

warcp_data_service = WarcpDataService()
faction_constnames, units_by_faction, upgrades_by_faction, docmarkers_by_faction = warcp_data_service.get_base_constnames()


attrib_parser_service = AttribParserService(faction_constnames)
# We have the units and upgrades we want to pull, get their attrib fullpath names from the consts_by_faction mapping
filtered_units_to_path_by_faction = attrib_parser_service.get_const_mapping_by_faction(units_by_faction,
                                                                                       "./json/unit_consts_by_faction.json")
filtered_upgrades_to_path_by_faction = attrib_parser_service.get_const_mapping_by_faction(upgrades_by_faction,
                                                                                          "./json/upgrade_consts_by_faction.json")

factions = {faction_constname: Faction(faction_constname) for faction_constname in faction_constnames}

# For each unit, get the sbps record corresponding to it, built into Factions entities
attrib_parser_service.get_raw_sbps_by_faction("./json/sbps_stats.json", factions, filtered_units_to_path_by_faction)

# Get all ebps records corresponding to entities in the unit
attrib_parser_service.get_raw_ebps_by_faction("./json/ebps_stats.json", factions)

# Get all upgrade records for the Faction
attrib_parser_service.get_raw_upgrade_by_faction("./json/upgrade_stats.json", factions, filtered_upgrades_to_path_by_faction)

# Get all abilities records
abilities = attrib_parser_service.get_abilities('./json/abilities_stats.json')

# Get all weapon records
weapons = attrib_parser_service.get_weapons('./json/weapon_stats.json')

# Get all slot item records
slot_items = attrib_parser_service.get_slot_items('./json/slot_item_stats.json')

units_clean = []
entities_clean = []
upgrades_clean = []
for faction in factions.values():
    units_clean.extend([x.clean() for x in faction.units.values()])
    entities_clean.extend([x.clean() for x in faction.entities.values()])
    upgrades_clean.extend([x.clean() for x in faction.upgrades.values()])

weapons_clean = [x.clean() for x in weapons]
slot_items_clean = [x.clean() for x in slot_items]

print("Finished")

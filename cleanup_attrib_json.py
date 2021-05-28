from AttribParserService import AttribParserService
from FileUtils import FileUtils
from models.Faction import Faction
from WarcpDataService import WarcpDataService


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
attrib_parser_service.get_raw_sbps_by_faction(factions, filtered_units_to_path_by_faction)

infantry = [u.clean() for u in factions['ALLY'].units.values()]

# Get all ebps records corresponding to entities in the unit


# Get all upgrade records for the Faction
attrib_parser_service.get_raw_upgrade_by_faction(factions, filtered_upgrades_to_path_by_faction)

units = []
for faction in factions.values():
    units.extend([x.clean() for x in faction.units.values()])

print("Finished")

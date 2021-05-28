from typing import Set, Dict, AnyStr, List, Any

from models.sbps.EmplacementBuilder import EmplacementBuilder
from models.Faction import Faction
from FileUtils import FileUtils
from models.sbps.Infantry import Infantry
from models.sbps.Unit import Unit
from models.Upgrade import Upgrade
from models.sbps.Vehicle import Vehicle


class AttribParserService:

    def __init__(self, faction_constnames: Set[AnyStr]):
        self.faction_constnames = faction_constnames

    def get_const_mapping_by_faction(self,
                                     constnames_by_faction: Dict[AnyStr, Set[AnyStr]],
                                     const_json_filepath: AnyStr,
                                     ) -> Dict[AnyStr, Dict[AnyStr, AnyStr]]:
        """
            Get only the const filenames from the given const_json_filepath that are in the set of constnames_by_faction.
        """
        const_data = FileUtils.read_json_file(const_json_filepath)

        # Remove faction. from constnames_by_faction when searching
        result = {}
        for faction in self.faction_constnames:
            faction_result = {}
            constname_set = constnames_by_faction[faction]
            raw_const_set = const_data[faction]
            for constname in constname_set:
                search_key = constname.replace(f"{faction}.", "")
                if search_key in raw_const_set:
                    faction_result[search_key] = raw_const_set[search_key]

            result[faction] = faction_result

        return result

    def get_raw_sbps_by_faction(self,
                                factions: Dict[AnyStr, Faction],
                                units_to_path_by_faction: Dict[AnyStr, Dict[AnyStr, AnyStr]],
                                ) -> None:
        sbps_json_file = FileUtils.read_json_file("./json/sbps_stats.json")
        for faction_constname in self.faction_constnames:
            faction_units_to_path = units_to_path_by_faction[faction_constname]

            faction = factions[faction_constname]
            for unit_const, path in faction_units_to_path.items():
                # Check if emplacement styling
                is_emplacement_builder = AttribParserService._is_emplacement_builder(path)
                file_path_elements = AttribParserService._get_file_path_elements('sbps', path)

                sbps_json = AttribParserService._get_value_from_nested_json(sbps_json_file, file_path_elements)

                if is_emplacement_builder:
                    unit = EmplacementBuilder(unit_const, faction_constname, path, sbps_json)
                elif AttribParserService._is_vehicle(path):
                    unit = Vehicle(unit_const, faction_constname, path, sbps_json)
                else:
                    assert AttribParserService._is_infantry(path)
                    unit = Infantry(unit_const, faction_constname, path, sbps_json)

                faction.add_unit(unit)

    def get_raw_ebps_by_faction(self):
        """

        """

    def get_raw_upgrade_by_faction(self,
                                   factions: Dict[AnyStr, Faction],
                                   upgrades_to_path_by_faction: Dict[AnyStr, Dict[AnyStr, AnyStr]],
                                   ) -> None:
        upgrade_json_file = FileUtils.read_json_file("./json/upgrade_stats.json")
        for faction_constname in self.faction_constnames:
            faction_upgrades_to_path = upgrades_to_path_by_faction[faction_constname]

            faction = factions[faction_constname]
            for upgrade_const, path in faction_upgrades_to_path.items():

                file_path_elements = AttribParserService._get_file_path_elements('upgrade', path)

                upgrade_json = AttribParserService._get_value_from_nested_json(upgrade_json_file, file_path_elements)

                upgrade = Upgrade(upgrade_const, faction_constname, path, upgrade_json)

                faction.add_upgrade(upgrade)

    @staticmethod
    def _is_emplacement_builder(filepath):
        return AttribParserService.REFERENCE_DELIMITER in filepath and 'emplacement' in filepath

    @staticmethod
    def _is_vehicle(filepath):
        return 'vehicles' in filepath and 'emplacements' not in filepath

    @staticmethod
    def _is_infantry(filepath):
        return 'soldiers' in filepath and 'vehicles' not in filepath

    @staticmethod
    def _get_file_path_elements(main_directory: AnyStr, filepath):
        if AttribParserService._is_emplacement_builder(filepath):
            elements = filepath.split(AttribParserService.REFERENCE_DELIMITER)
        else:
            elements = filepath.split(AttribParserService.NON_REFERENCE_DELIMITER)

        elements = [x.lower() for x in elements]

        return AttribParserService._validate_and_cleanup_file_path_elements(main_directory, elements, filepath)

    @staticmethod
    def _validate_and_cleanup_file_path_elements(main_directory: AnyStr, file_path_elements: List[AnyStr], path: AnyStr) -> List[AnyStr]:
        if file_path_elements[0] != main_directory:
            raise Exception(f"Invalid file path {path}, expected '{main_directory}' at beginning of path.")
        if ".lua" not in file_path_elements[-1] and ".rgd" not in file_path_elements[-1]:
            raise Exception(f"Invalid lua file {path}, expected '.lua' or '.rgd' file extension.")

        del file_path_elements[0]
        file_path_elements[-1] = file_path_elements[-1].replace('.lua', '').replace('.rgd', '')

        return file_path_elements

    @staticmethod
    def _get_value_from_nested_json(json_dict: Dict[AnyStr, Any], path_elements: List[AnyStr]) -> Dict[AnyStr, Any]:
        current_level = json_dict
        last_element = None
        max_depth = len(path_elements)
        for idx, element in enumerate(path_elements):
            if element not in current_level:
                if last_element:
                    raise Exception(f"Invalid path elements {path_elements}, at level {last_element} could not find key {element}")
                else:
                    raise Exception(f"Invalid path elements {path_elements} could not find key {element}")
            else:
                if idx == max_depth - 1:
                    return current_level[element]
                else:
                    current_level = current_level[element]

    NON_REFERENCE_DELIMITER = '/'
    REFERENCE_DELIMITER = '\\'

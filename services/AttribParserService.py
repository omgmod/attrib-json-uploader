from typing import Set, Dict, AnyStr, List, Any

from models.Ability import Ability
from models.Faction import Faction
from models.SlotItem import SlotItem
from models.Upgrade import Upgrade
from models.Weapon import Weapon
from models.ebps.Building import Building
from models.ebps.EmplacementBuilder import EmplacementBuilder
from models.ebps.EmplacementGun import EmplacementGun
from models.ebps.Infantry import Infantry
from models.ebps.Prop import Prop
from models.ebps.Vehicle import Vehicle
from models.sbps.EmplacementBuilder import EmplacementBuilder as EmplacementBuilderSquad
from models.sbps.Infantry import Infantry as InfantrySquad
from models.sbps.Vehicle import Vehicle as VehicleSquad
from utils.FileUtils import FileUtils
from utils.StringUtils import StringUtils


class AttribParserService:

    def __init__(self, faction_constnames: Set[AnyStr]):
        self.faction_constnames = faction_constnames

    def get_const_mapping_by_faction(self,
                                     constnames_by_faction: Dict[AnyStr, Set[AnyStr]],
                                     const_json_filepath: AnyStr,
                                     flatten_docmarkers: bool = False,
                                     ) -> Dict[AnyStr, Dict[AnyStr, AnyStr]]:
        """
            Get only the const filenames from the given const_json_filepath that are in the set of constnames_by_faction.
        """
        const_data = FileUtils.read_json_file(const_json_filepath)
        if flatten_docmarkers:
            const_data = self.flatten_docmarker_const_mapping(const_data)

        # Remove faction. from constnames_by_faction when searching
        result = {}
        for faction in self.faction_constnames:
            faction_result = {}
            constname_set = constnames_by_faction[faction]
            raw_const_set = const_data[faction]
            for constname in constname_set:
                if flatten_docmarkers:
                    search_key = constname
                else:
                    search_key = constname.replace(f"{faction}.", "")
                if search_key in raw_const_set:
                    faction_result[search_key] = raw_const_set[search_key]

            result[faction] = faction_result

        return result

    def flatten_docmarker_const_mapping(self, constnames_by_faction: Dict[AnyStr, Dict[AnyStr, Dict[AnyStr, Dict[AnyStr, Dict[AnyStr, AnyStr]]]]]):
        """
            Docmarkers have a 5 level hieraarchy of
            wrapping dict -> faction CONSTNAME -> doctrine CONSTNAME -> TR -> B -> T
            constnames_by_action -> CMW -> ENGINEERS -> TR1 -> B1 -> T1 -> string
            Flatten to
            constnames_by_action -> CMW -> OMGDOCUPG.CMW.ENGINEERS.TR1.B1.T1 -> string
        """
        result = {}
        for faction in self.faction_constnames:
            faction_result = {}
            faction_constname_set = constnames_by_faction[faction]
            for doctrine_constname, doctrine_values in faction_constname_set.items():
                for tr_constname, tr_values in doctrine_values.items():
                    for b_constname, b_values in tr_values.items():
                        for t_constname, t_value in b_values.items():
                            new_constname_key = f'OMGDOCUPG.{faction}.{doctrine_constname}.{tr_constname}.{b_constname}.{t_constname}'
                            faction_result[new_constname_key] = StringUtils.remove_file_endings(t_value)
            result[faction] = faction_result
        return result

    def get_raw_sbps_by_faction(self,
                                filepath,
                                factions: Dict[AnyStr, Faction],
                                units_to_path_by_faction: Dict[AnyStr, Dict[AnyStr, AnyStr]],
                                ) -> None:
        """
            Parse the sbps_stats.json file and for every sbps entry with a unit constname in our given
            units_to_path_by_faction set, transform the entry into a Unit object and add to the respective Faction
            object in factions.
        """
        sbps_json_file = FileUtils.read_json_file(filepath)
        for faction_constname in self.faction_constnames:
            faction_units_to_path = units_to_path_by_faction[faction_constname]

            faction = factions[faction_constname]
            for unit_const, path in faction_units_to_path.items():
                # Check if emplacement styling
                is_emplacement_builder = AttribParserService._is_emplacement_builder(path)
                file_path_elements = AttribParserService._get_file_path_elements('sbps', path)

                sbps_json = AttribParserService._get_value_from_nested_json(sbps_json_file, file_path_elements)

                if is_emplacement_builder:
                    unit = EmplacementBuilderSquad(unit_const, faction_constname, path, sbps_json)
                elif AttribParserService._is_vehicle(path):
                    unit = VehicleSquad(unit_const, faction_constname, path, sbps_json)
                else:
                    assert AttribParserService._is_infantry(path)
                    unit = InfantrySquad(unit_const, faction_constname, path, sbps_json)

                faction.add_unit(unit)

    def get_raw_ebps_by_faction(self,
                                filepath,
                                factions: Dict[AnyStr, Faction],
                                ):
        """

        """
        ebps_json_file = FileUtils.read_json_file(filepath)
        factions_dict = ebps_json_file['races']
        for faction_constname in self.faction_constnames:
            faction_name = AttribParserService.EBPS_FACTION_CONSTNAME_TO_DIRECTORY[faction_constname]
            faction_dict = factions_dict[faction_name]
            results = []
            for soldier_key, soldier_dict in faction_dict['soldiers'].items():
                if 'squad_veterancy_ext' in soldier_dict.keys():
                    print(f"Warning - Encountered {soldier_key} with squad type keys in ebps: {soldier_dict}")
                    continue
                results.append(Infantry(soldier_dict, faction_constname, f'ebps\\races\\{faction_name}\\soldiers\\{soldier_key}'))
            for vehicle_key, vehicle_dict in faction_dict['vehicles'].items():
                if 'hq_wreck' in vehicle_key:
                    continue
                results.append(Vehicle(vehicle_dict, faction_constname, f'ebps\\races\\{faction_name}\\vehicles\\{vehicle_key}'))
            for building_key, building_dict in faction_dict['buildings'].items():
                if building_key in ('quarter_master', 'panzer_artillerie_kommand', 'panzerjager_kommand', 'sp'):
                    continue
                if 'hq_wreck' in building_key:
                    continue
                results.append(Building(building_dict, faction_constname, f'ebps\\races\\{faction_name}\\buildings\\{building_key}'))
            for truck_key, truck_dict in faction_dict['emplacements']['trucks'].items():
                results.append(EmplacementBuilder(truck_dict, faction_constname, f'ebps\\races\\{faction_name}\\emplacements\\trucks\\{truck_key}'))
            for gun_key, gun_dict in faction_dict['emplacements']['guns'].items():
                results.append(EmplacementGun(gun_dict, faction_constname, f'ebps\\races\\{faction_name}\\emplacements\\guns\\{gun_key}'))
            faction = factions[faction_constname]
            for entity in results:
                faction.add_entity(entity)

        # Get props
        # ebps/props     ebps/gameplay/props
        raw_props = ebps_json_file['props']
        raw_gameplay_props = ebps_json_file['gameplay']['props']
        props = []
        for raw_prop_key, raw_prop_dict in raw_props.items():
            props.append(Prop(raw_prop_dict, None, f'ebps\\props\\{raw_prop_key}'))
        for raw_prop_key, raw_prop_dict in raw_gameplay_props.items():
            props.append(Prop(raw_prop_dict, None, f'ebps\\gameplay\\props\\{raw_prop_key}'))
        return props

    def get_raw_upgrade_by_faction(self,
                                   filepath,
                                   factions: Dict[AnyStr, Faction],
                                   upgrades_to_path_by_faction: Dict[AnyStr, Dict[AnyStr, AnyStr]],
                                   ) -> List:
        upgrade_json_file = FileUtils.read_json_file(filepath)
        for faction_constname in self.faction_constnames:
            faction_upgrades_to_path = upgrades_to_path_by_faction[faction_constname]

            faction = factions[faction_constname]
            for upgrade_const, path in faction_upgrades_to_path.items():

                file_path_elements = AttribParserService._get_file_path_elements('upgrade', path)

                upgrade_json = AttribParserService._get_value_from_nested_json(upgrade_json_file, file_path_elements)

                upgrade = Upgrade(upgrade_const, faction_constname, path, upgrade_json)

                faction.add_upgrade(upgrade)

        # Get upgrades by faction for upgrades without CONSTNAME
        upgrades = []
        folder_factions = {'allies': 'ALLY', 'allies_cw': 'CMW', 'axis': 'AXIS', 'axis_pe': 'PE'}
        for folder, constname in folder_factions.items():
            self.get_faction_upgrades_recursive(upgrade_json_file[folder], f"upgrade\\{folder}", constname, upgrades)
        return upgrades

    def get_faction_upgrades_recursive(self, target, path_so_far, faction_constname, result):
        for key, value in target.items():
            current_path = f"{path_so_far}\\{key}"
            if 'upgrade_bag' in value:
                result.append(Upgrade('', faction_constname, current_path, value))
            else:
                self.get_faction_upgrades_recursive(value, current_path, faction_constname, result)

    def get_abilities(self, filepath):
        abilities_json_file = FileUtils.read_json_file(filepath)
        omg_abilities_json = abilities_json_file['omg']
        # parse omg subsection
        # Only care about 'doctrine' and 'vet'
        doctrine_abilities = [Ability(ability_json, f"abilities\\omg\\doctrine\\{name}") for name, ability_json in omg_abilities_json['doctrine'].items()]
        vet_abilities = [Ability(ability_json, f"abilities\\omg\\vet\\{name}") for name, ability_json in omg_abilities_json['vet'].items()]

        # ignore sp subsection

        # parse remaining top level abilities
        default_abilities = []
        for key, ability_json in abilities_json_file.items():
            if key in ('omg', 'sp'):
                continue
            ability = Ability(ability_json, f"abilities\\{key}")
            default_abilities.append(ability)

        return {
            'omg': {
                'doctrine': doctrine_abilities,
                'vet': vet_abilities
            },
            'default': default_abilities
        }

    def get_weapons(self, filepath):
        weapons_json_file = FileUtils.read_json_file(filepath)
        result = []
        self.get_weapons_recursive(weapons_json_file, "weapon", result)
        return result

    def get_weapons_recursive(self, target, path_so_far, result):
        for key, value in target.items():
            current_path = f"{path_so_far}\\{key}"
            # Since some dicts are "directories" and some are not, have to check for `weapon_bag`
            if 'weapon_bag' in value:
                # Found a weapon
                result.append(Weapon(value, current_path))
            else:
                # Value is a dictionary of weapons, recurse
                self.get_weapons_recursive(value, current_path, result)

    def get_slot_items(self, filepath):
        slot_item_json_file = FileUtils.read_json_file(filepath)
        result = []
        self.get_slot_items_recursive(slot_item_json_file, "slot_item", result)
        return result

    def get_slot_items_recursive(self, target, path_so_far, result):
        for key, value in target.items():
            current_path = f"{path_so_far}\\{key}"
            if 'slot_item_bag' in value:
                result.append(SlotItem(value, current_path))
            elif 'upgrade_bag' in value:
                continue
            else:
                self.get_slot_items_recursive(value, current_path, result)

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
        file_path_elements[-1] = StringUtils.remove_file_endings(file_path_elements[-1])

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

    EBPS_FACTION_CONSTNAME_TO_DIRECTORY = {
        'ALLY': 'allies',
        'CMW': 'allies_commonwealth',
        'AXIS': 'axis',
        'PE': 'axis_panzer_elite'
    }

from pprint import pprint
from typing import AnyStr, Dict, List, Union

from factories.ActionFactory import ActionFactory
from models.AbstractModel import AbstractModel
from models.Cover import Cover
from utils.DictUtils import DictUtils
from utils.StringUtils import StringUtils


class Entity(AbstractModel):
    """
        Represents an ebps record
    """
    def __init__(self, raw_json, faction, filename):
        super().__init__(raw_json)
        self.faction = faction
        self.ebps_filename = filename

    def get_abilities(self):
        """
            If the ebps has abilities, return them as a list in format [[abilities\\X_ability.lua]]
        """
        try:
            abilities_dict = self.raw_json['ability_ext']['abilities']
            abilities = [StringUtils.remove_bracket_file_endings(a) for a in abilities_dict.values()]
        except KeyError:
            abilities = None
        return abilities

    def get_actions(self):
        try:
            action_table_json = self.raw_json['action_apply_ext']['actions']

            clean_ability_actions = None
            clean_upgrade_actions = None
            if 'ability_actions' in action_table_json:
                clean_ability_actions = [ActionFactory.create_action_from_json(a).clean() for a in
                                         action_table_json['ability_actions'].values()]
            if 'upgrade_actions' in action_table_json:
                clean_upgrade_actions = [ActionFactory.create_action_from_json(a).clean() for a in
                                         action_table_json['upgrade_actions'].values()]
            clean_actions = []
            if clean_ability_actions:
                clean_actions.extend([x for x in clean_ability_actions if x is not None])
            if clean_upgrade_actions:
                clean_actions.extend([x for x in clean_upgrade_actions if x is not None])
            return clean_actions
        except KeyError:
            return None

    def get_weapons(self):
        weapons = []
        try:
            hardpoints = self.raw_json['combat_ext']['hardpoints']
            for hardpoint_dict in hardpoints.values():
                try:
                    for weapon_dict in hardpoint_dict['weapon_table'].values():
                        if 'type' in weapon_dict and weapon_dict['type'] == '[[accessory]]':
                            continue
                        weapon = weapon_dict['weapon']
                        weapons.append(StringUtils.remove_bracket_file_endings(weapon))
                    if len(hardpoint_dict['weapon_table']) > 1 and hardpoint_dict['weapon_table']['weapon_02']['type'] != '[[accessory]]':
                        if hardpoint_dict['weapon_table']['weapon_01']['weapon'] == hardpoint_dict['weapon_table']['weapon_02']['weapon']:
                            print(
                                f"WARNING - {self.ebps_filename} Duplicate weapons for hardpoint {pprint(hardpoint_dict['weapon_table'])}")
                        else:
                            print(
                                f"WARNING - {self.ebps_filename} More than one weapon found for a hardpoint weapon table {pprint(hardpoint_dict['weapon_table'])}")
                except KeyError:
                    continue
        except KeyError:
            pass
        return weapons

    def get_cover(self):
        cover_ext_dict = self.raw_json['cover_ext']
        cover_results = {}
        for cover_type, cover_dict in cover_ext_dict.items():
            if cover_type == 'reference':
                continue
            cover = Cover(cover_dict, cover_type)
            cover_results[cover_type] = cover.clean()
        return cover_results

    def get_health(self):
        try:
            health_ext_dict = self.raw_json['health_ext']
            health = {}
            DictUtils.add_to_dict_if_in_source(health_ext_dict, health, 'hitpoints')
            DictUtils.add_to_dict_if_in_source(health_ext_dict, health, 'rear_damage_critical_type')
            DictUtils.add_to_dict_if_in_source(health_ext_dict, health, 'rear_damage_enabled')
            return health
        except KeyError:
            return {}

    def get_moving(self):
        try:
            moving_ext_dict = self.raw_json['moving_ext']
            moving = {}
            DictUtils.add_to_dict_if_in_source(moving_ext_dict, moving, 'speed_max')
            DictUtils.add_to_dict_if_in_source(moving_ext_dict, moving, 'acceleration')
            DictUtils.add_to_dict_if_in_source(moving_ext_dict, moving, 'deceleration')
            DictUtils.add_to_dict_if_in_source(moving_ext_dict, moving, 'rotation_rate')
            return moving
        except KeyError:
            return None

    def get_population(self):
        try:
            population_ext_dict = self.raw_json['population_ext']
            result = {}
            DictUtils.add_to_dict_if_in_source(population_ext_dict, result, 'personnel_pop')
            DictUtils.add_to_dict_if_in_source(population_ext_dict, result, 'medic_pop')
            if 'medic_pop' in population_ext_dict:
                print(f"Warning - encountered medic pop {population_ext_dict}")
            return result
        except KeyError:
            return {}

    def get_sight(self):
        try:
            sight_ext_dict = self.raw_json['sight_ext']
            result = {}
            if 'sight_package' in sight_ext_dict:
                DictUtils.add_to_dict_if_in_source(sight_ext_dict['sight_package'], result, 'outer_radius')
            if 'detect_camouflage' in sight_ext_dict:
                DictUtils.add_to_dict_if_in_source(sight_ext_dict['detect_camouflage'], result, 'detect_radius')
            return result
        except KeyError:
            return {}

    def get_types(self):
        try:
            type_ext_dict = self.raw_json['type_ext']
            if 'type_target_weapon' not in type_ext_dict:
                print(f"WARNING - {self.ebps_filename} missing type_target_weapon")
            if 'type_target_critical' not in type_ext_dict:
                print(f"WARNING - {self.ebps_filename} missing type_target_critical")
            target_type_weapon = type_ext_dict.get('type_target_weapon', None)  # axis_howitzer_gun_nest
            if target_type_weapon is not None:
                target_type_weapon = StringUtils.remove_bracket_file_endings(target_type_weapon['reference'])

            type_target_critical = type_ext_dict.get('type_target_critical', None)  # Some hq wrecks don't have this
            if type_target_critical is not None:
                type_target_critical = StringUtils.remove_bracket_file_endings(type_target_critical['reference'])

            result = {}
            if target_type_weapon:
                result['type_target_weapon'] = target_type_weapon
            if type_target_critical:
                result['type_target_critical'] = type_target_critical
            return result
        except KeyError:
            return {}

    def get_veterancy_value(self):
        try:
            veterancy_ext_dict = self.raw_json['veterancy_ext']
            return {
                'experience_value': veterancy_ext_dict['experience_value']
            }
        except KeyError:
            return {}

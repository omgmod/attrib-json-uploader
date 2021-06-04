from pprint import pprint
from typing import Dict, Union

from models.action.Action import Action
from models.action.ability.ApplyModifiersAction import ApplyModifiersAction
from models.action.ability.DelayAction import DelayAction
from models.action.ability.TargetAction import TargetAction
from utils.DictUtils import DictUtils
from utils.StringUtils import StringUtils


class UpgradeAction(Action):

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def clean(self):
        if type(self.raw_json) == str:
            self.raw_json = {
                'reference': self.raw_json
            }
        reference = UpgradeAction.get_reference_with_depth(self.raw_json['reference'], 2)
        if ']]' in reference:
            print(f"WARNING - found UpgradeAction reference with malformed path {self.raw_json['reference']}")
            return None

        if reference == 'apply_modifiers_action':
            action = ApplyModifiersAction(self.raw_json)
            return action.clean()
        elif reference == 'add_weapon':
            if 'weapon' in self.raw_json:
                weapon = self.raw_json['weapon']['weapon']
            else:
                weapon = self.raw_json['hardpoint']['weapon']['weapon']
            result = {
                'reference': reference,
                'weapon': StringUtils.remove_bracket_file_endings(weapon)
            }
            DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'hardpoint')
            return result
        elif reference == 'change_weapon':
            if 'weapon' in self.raw_json:
                weapon = self.raw_json['weapon']
            else:
                weapon = self.raw_json['hardpoint']['weapon']
            if type(weapon) == dict:
                weapon = weapon['weapon']
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            if 'weapon' in self.raw_json:
                result['weapon'] = StringUtils.remove_bracket_file_endings(weapon)
            DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'hardpoint')
            return result
        elif reference == 'upgrade_add':
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            if 'upgrade' in self.raw_json:
                result['upgrade'] = StringUtils.remove_bracket_file_endings(self.raw_json['upgrade'])
            return result
        elif reference == 'slot_item_add':
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            if 'slot_item' in self.raw_json:
                result['slot_item'] = StringUtils.remove_bracket_file_endings(self.raw_json['slot_item'])
            return result
        elif reference == 'slot_item_remove':
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            if 'slot_item' in self.raw_json:
                result['slot_item'] = StringUtils.remove_bracket_file_endings(self.raw_json['slot_item'])
            return result
        elif reference == 'slot_item_replace':
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            if 'old_slot_item' in self.raw_json:
                result['old_slot_item'] = StringUtils.remove_bracket_file_endings(self.raw_json['old_slot_item'])
            if 'new_slot_item' in self.raw_json:
                result['new_slot_item'] = StringUtils.remove_bracket_file_endings(self.raw_json['new_slot_item'])
            return result
        elif reference == 'change_move_data_action':
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'acceleration_multiplier')
            return result
        elif reference == 'change_weapon_target_type':
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            if 'new_type' in self.raw_json:
                result['new_type'] = StringUtils.remove_bracket_file_endings(self.raw_json['new_type'])
            if 'original_type' in self.raw_json:
                result['original_type'] = StringUtils.remove_bracket_file_endings(self.raw_json['original_type'])
            return result
        elif reference == 'change_critical_target_type':
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            if 'new_type' in self.raw_json:
                result['new_type'] = StringUtils.remove_bracket_file_endings(self.raw_json['new_type'])
            if 'original_type' in self.raw_json:
                result['original_type'] = StringUtils.remove_bracket_file_endings(self.raw_json['original_type'])
            return result
        elif reference == 'replace_ability_action':
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            if 'ability_to_add' in self.raw_json:
                result['ability_to_add'] = StringUtils.remove_bracket_file_endings(self.raw_json['ability_to_add'])
            if 'ability_to_remove' in self.raw_json:
                result['ability_to_remove'] = StringUtils.remove_bracket_file_endings(self.raw_json['ability_to_remove'])
            return result
        elif reference == 'remove_weapon':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference)
            }
        elif reference == 'add_crew_action':
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            if 'crew_name' in self.raw_json:
                result['crew_name'] = StringUtils.remove_bracket_file_endings(self.raw_json['crew_name'])
            return result
        elif reference == 'remove_crew_action':
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            if 'crew_name' in self.raw_json:
                result['crew_name'] = StringUtils.remove_bracket_file_endings(self.raw_json['crew_name'])
            return result
        elif reference == 'upgrade_remove':
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            if 'upgrade' in self.raw_json:
                result['upgrade'] = StringUtils.remove_bracket_file_endings(self.raw_json['upgrade'])
            return result
        elif reference == 'activate_extension_action':
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            if 'repair_station_ext' in self.raw_json:
                result['repair_station_ext'] = StringUtils.remove_bracket_file_endings(self.raw_json['repair_station_ext'])
            return result
        elif reference == 'garrison_squad_action':
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
            }
            if 'squad_blueprint' in self.raw_json:
                result['squad_blueprint'] = StringUtils.remove_bracket_file_endings(
                    self.raw_json['squad_blueprint'])
            return result
        elif reference == 'delay_action':
            delay_action = DelayAction(self.raw_json).clean()
            return delay_action

        elif reference == 'timed_action':
            subactions = []
            for subactions_dict in self.raw_json['subactions'].values():
                if 'ability_actions' in subactions_dict:
                    for action_dict in subactions_dict['ability_actions'].values():
                        action = UpgradeAction._build_ability_action(action_dict)
                        clean_action = action.clean()
                        if clean_action:
                            subactions.append(clean_action)
            result = {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'subactions': subactions,
            }
            DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'duration')
            return result

        # Actions to ignore
        elif reference in UpgradeAction.REFERENCES_TO_IGNORE:
            return None
        else:
            raise Exception(f"Unexpected upgrade action {pprint(self.raw_json)}")

    REFERENCES_TO_IGNORE = ('retreat_status_action', 'alter_squad_ui_info_action', 'ui_decorator_action',
                            'ui_unit_modifier_action', 'animator_set_state', 'no_action', 'set_crush_obb',
                            'animator_set_event', 'filter_action', 'hold_action', 'ui_selection_type_change',
                            'swap_actor_action', 'animator_set_variable',
                            )

    @staticmethod
    def _build_ability_action(action_json: Dict) -> Union[Dict, None]:
        reference = UpgradeAction._get_ability_upgrade_reference(action_json['reference'])
        if reference == 'apply_modifiers_action':
            return ApplyModifiersAction(action_json).clean()
        elif 'upgrade_action' in action_json['reference']:
            # Bizarrely this is actually an upgrade action
            print(f"WARNING Unexpected UpgradeAction {action_json['reference']} for action {action_json}")
            return UpgradeAction(action_json).clean()

        elif reference == 'delay' or reference == 'delay]]':  #TODO FIX THIS SPECIAL CASE
            if reference == 'delay]]':
                print(f"WARNING Malformed delay action reference {reference} for action {action_json}")
            return DelayAction(action_json).clean()

        elif reference == 'target':
            return TargetAction(action_json).clean()

        elif reference in ('no_action', 'ui_unit_modifier_action', 'ui_decorator_action'):
            return None

        else:
            raise Exception(f"Unexpected ability action reference {reference} for RequirementAction")

    @staticmethod
    def _get_ability_upgrade_reference(path):
        return path.split('\\')[2].replace('.lua]]', '')

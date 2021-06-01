from pprint import pprint
from typing import Dict, Union

from models.action.Action import Action
from models.action.ability.ApplyModifiersAction import ApplyModifiersAction
from models.action.ability.DelayAction import DelayAction
from models.action.ability.TargetAction import TargetAction
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
            return {
                'reference': reference,
                'weapon': weapon
            }
        elif reference == 'change_weapon':
            if 'weapon' in self.raw_json:
                weapon = self.raw_json['weapon']
            else:
                weapon = self.raw_json['hardpoint']['weapon']
            if type(weapon) == dict:
                weapon = weapon['weapon']
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'weapon': StringUtils.remove_bracket_file_endings(weapon),
            }
        elif reference == 'upgrade_add':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'upgrade': StringUtils.remove_bracket_file_endings(self.raw_json['upgrade'])
            }
        elif reference == 'slot_item_add':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'slot_item': StringUtils.remove_bracket_file_endings(self.raw_json['slot_item'])
            }
        elif reference == 'slot_item_replace':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'old_slot_item': StringUtils.remove_bracket_file_endings(self.raw_json['old_slot_item']),
                'new_slot_item': StringUtils.remove_bracket_file_endings(self.raw_json['new_slot_item']),
            }
        elif reference == 'change_move_data_action':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'acceleration_multiplier': self.raw_json['acceleration_multiplier']
            }
        elif reference == 'change_weapon_target_type':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'new_type': StringUtils.remove_bracket_file_endings(self.raw_json['new_type']),
                'original_type': StringUtils.remove_bracket_file_endings(self.raw_json['original_type']),
            }
        elif reference == 'change_critical_target_type':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'new_type': StringUtils.remove_bracket_file_endings(self.raw_json['new_type']),
                'original_type': StringUtils.remove_bracket_file_endings(self.raw_json['original_type']),
            }
        elif reference == 'replace_ability_action':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'ability_to_add': StringUtils.remove_bracket_file_endings(self.raw_json['ability_to_add']),
                'ability_to_remove': StringUtils.remove_bracket_file_endings(self.raw_json['ability_to_remove']),
            }
        elif reference == 'remove_weapon':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference)
            }
        elif reference == 'add_crew_action':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'crew_name': StringUtils.remove_bracket_file_endings(self.raw_json['crew_name'])
            }
        elif reference == 'remove_crew_action':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'crew_name': StringUtils.remove_bracket_file_endings(self.raw_json['crew_name'])
            }
        elif reference == 'upgrade_remove':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'upgrade': StringUtils.remove_bracket_file_endings(self.raw_json['upgrade'])
            }
        elif reference == 'activate_extension_action':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'repair_station_ext': StringUtils.remove_bracket_file_endings(self.raw_json['repair_station_ext'])
            }
        elif reference == 'garrison_squad_action':
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'squad_blueprint': StringUtils.remove_bracket_file_endings(self.raw_json['squad_blueprint'])
            }
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
            return {
                'reference': StringUtils.remove_bracket_file_endings(reference),
                'duration': self.raw_json['duration'],
                'subactions': subactions,
            }

        # Actions to ignore
        elif reference in UpgradeAction.REFERENCES_TO_IGNORE:
            return None
        else:
            raise Exception(f"Unexpected upgrade action {pprint(self.raw_json)}")

    REFERENCES_TO_IGNORE = ('retreat_status_action', 'alter_squad_ui_info_action', 'ui_decorator_action',
                            'ui_unit_modifier_action', 'animator_set_state', 'no_action', 'set_crush_obb',
                            'animator_set_event', 'filter_action', 'hold_action', 'ui_selection_type_change'
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

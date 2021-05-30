from functools import partial
from typing import AnyStr, Union, Dict

from utils.DictUtils import DictUtils
from models.sbps.Unit import Unit


class Infantry(Unit):
    def __init__(self, constname, faction, filename, sbps_json):
        super().__init__(constname, faction, filename, sbps_json)

    def clean(self):
        """
            Parse the raw sbps_json dict into a condensed dictionary with only the values we need.

            Properties to look at:
                squad_ability_ext.abilities.ability_0X references [abilities]
                squad_action_apply_ext.actions
                    ability_actions.action_0X references [action]
                        - apply_modifiers_action
                            modifiers.modifiers_0X references [modifiers]
                                value
                                application_type (optional)
                                usage_type (optional)
                        - requirement_action
                            action_table
                                ability_actions.action_01 references [action] most likely apply_modifiers_action
                                    [modifiers block]
                                upgrade_actions.action_01 references [action] most likely apply_modifiers_action
                                    [modifiers block]
                            requirement_table.required_X references [requirements]
                                operation if requirement is logical operator like required_unary_expr this could be [[not]]
                                requirement_table.required_X references [requirements]
                                    min_owned
                                    max_owned
                                    slot_item references [slot_item]
                    upgrade_actions
                squad_combat_behaviour_ext
                    suppression
                        cover_info.tp_X.recover_multipler uses cover types
                        noncombat_delay
                        noncombat_recover_multiplier
                        recover_rate
                        suppressed_activate_threshold
                        pin_down_activate_threshold
                        suppressed_recover_threshold
                squad_loadout_ext.unit_list.unit_0X
                    type.type references [ebps]
                    num
                squad_veterancy_ext.veterancy_rank_info
                    veterancy_rank_(01-05)
                        experience_value
                        squad_actions.actions_0X references [action] most likely apply_modifiers_action
                            [modifiers_block]
        """
        abilities = self.get_abilities()
        actions = self.get_actions()
        combat_behavior_suppression = self.get_combat_behaviour_suppression()
        loadout = self.get_loadout()
        veterancy = self.get_veterancy()

        result = {
            'reference': self.sbps_filename,
            'constname': self.constname,
            'faction': self.faction,
            'type': 'infantry',
            'combat_behavior_suppression': combat_behavior_suppression,
            'loadout': loadout,
            'veterancy': veterancy
        }
        if actions:
            result['actions'] = [action for action in actions]
        if abilities:
            result['abilities'] = abilities

        return result

    def get_combat_behaviour_suppression(self) -> Dict[AnyStr, Union[AnyStr, float, Dict[AnyStr, float]]]:
        """
            Get a dict of suppression combat behavior
        """
        suppression_dict = self.raw_json['squad_combat_behaviour_ext']['suppression']

        result = {
            'cover_info': {cover_type: value['recover_multiplier'] for cover_type, value in suppression_dict['cover_info'].items()},
        }
        add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, suppression_dict, result)
        add_to_dict_partial('noncombat_delay')
        add_to_dict_partial('noncombat_recover_multiplier')
        add_to_dict_partial('recover_rate')
        add_to_dict_partial('suppressed_activate_threshold')
        add_to_dict_partial('pin_down_activate_threshold')
        add_to_dict_partial('suppressed_recover_threshold')

        return result

from pprint import pprint

from models.action.Action import Action
from models.action.ability.ApplyModifiersAction import ApplyModifiersAction
from models.action.ability.DelayAction import DelayAction


class UpgradeAction(Action):

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def clean(self):
        reference = UpgradeAction.get_reference_with_depth(self.raw_json['reference'], 2)
        if ']]' in reference:
            print(f"WARNING - found UpgradeAction reference with malformed path {self.raw_json['reference']}")
            return None

        if reference == 'apply_modifiers_action':
            action = ApplyModifiersAction(self.raw_json)
            return action.clean()
        elif reference == 'add_weapon':
            if 'hardpoint' in self.raw_json:
                weapon = self.raw_json['hardpoint']['weapon']['weapon']
            else:
                weapon = self.raw_json['weapon']['weapon']
            return {
                'reference': reference,
                'weapon': weapon
            }
        elif reference == 'change_weapon':
            if 'hardpoint' in self.raw_json:
                weapon = self.raw_json['hardpoint']['weapon']
            else:
                weapon = self.raw_json['weapon']
            return {
                'reference': reference,
                'weapon': weapon
            }
        elif reference == 'upgrade_add':
            return {
                'reference': reference,
                'upgrade': self.raw_json['upgrade']
            }
        elif reference == 'slot_item_add':
            return {
                'reference': reference,
                'slot_item': self.raw_json['slot_item']
            }
        elif reference == 'slot_item_replace':
            return {
                'reference': reference,
                'old_slot_item': self.raw_json['old_slot_item'],
                'new_slot_item': self.raw_json['new_slot_item']
            }
        elif reference == 'change_move_data_action':
            return {
                'reference': reference,
                'acceleration_multiplier': self.raw_json['acceleration_multiplier']
            }
        elif reference == 'change_weapon_target_type':
            return {
                'reference': reference,
                'new_type': self.raw_json['new_type'],
                'original_type': self.raw_json['original_type'],
            }
        elif reference == 'change_critical_target_type':
            return {
                'reference': reference,
                'new_type': self.raw_json['new_type'],
                'original_type': self.raw_json['original_type'],
            }
        elif reference == 'replace_ability_action':
            return {
                'reference': reference,
                'ability_to_add': self.raw_json['ability_to_add'],
                'ability_to_remove': self.raw_json['ability_to_remove'],
            }
        elif reference == 'delay_action':
            delay_action = DelayAction(self.raw_json).clean()
            return delay_action

        # Actions to ignore
        elif reference in UpgradeAction.REFERENCES_TO_IGNORE:
            return None
        else:
            raise Exception(f"Unexpected upgrade action {pprint(self.raw_json)}")

    REFERENCES_TO_IGNORE = ('retreat_status_action', 'alter_squad_ui_info_action', 'ui_decorator_action',
                            'ui_unit_modifier_action',
                            )



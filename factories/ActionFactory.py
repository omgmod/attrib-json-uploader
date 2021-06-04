from typing import AnyStr, Tuple, List

from models.action.AbilityAction import AbilityAction
from models.action.Action import Action
from models.action.CriticalAction import CriticalAction
from models.action.NoopAction import NoopAction
from models.action.UpgradeAction import UpgradeAction
from models.action.ability.ApplyModifiersAction import ApplyModifiersAction
from models.action.ability.ChangeMoveDataAction import ChangeMoveDataAction
from models.action.ability.HealAction import HealAction
from models.action.ability.RequirementAction import RequirementAction


class ActionFactory:

    ACTION_CLASS_NAME_TO_CLASS = {
        'ability_action': AbilityAction,
        'critical_action': CriticalAction,
        'upgrade_action': UpgradeAction
    }

    ACTION_TYPE_NAME_TO_CLASS = {
        'requirement_action': RequirementAction,
        'apply_modifiers_action': ApplyModifiersAction,
        'alter_squad_ui_info_action': NoopAction,
        'animator_set_state': NoopAction,
        'change_move_data_action': ChangeMoveDataAction,
        'heal_action': HealAction,
        'ui_unit_modifier_action': NoopAction,
    }

    @staticmethod
    def build_clean_actions_from_json(actions_list) -> List:
        """"""
        try:
            result = []
            for action in actions_list:
                if type(action) == str:
                    return None
                reference = action['reference']
                if reference in ('[[tables\\ability_action_table.lua]]', '[[tables\\upgrade_action_table.lua]]'):
                    subresult = ActionFactory.build_clean_actions_from_json(action.values())
                    result.extend(subresult)
                else:
                    # single action
                    action_instance = ActionFactory.create_action_from_json(action)
                    result.append(action_instance.clean())
            return result
        except TypeError:
            return []

    @staticmethod
    def create_action_from_json(json_dict) -> Action:
        # Get the reference from the action dict, depending on action do something different
        try:
            reference = json_dict['reference']
            if reference == '[[]]':
                return NoopAction(json_dict)
            action_class_name, action_type = ActionFactory._get_action_class_and_type(reference)

            if action_class_name not in ActionFactory.ACTION_CLASS_NAME_TO_CLASS:
                raise Exception(f"Unexpected action class name {action_class_name}")

            action_class = ActionFactory.ACTION_CLASS_NAME_TO_CLASS[action_class_name]

            if action_class == AbilityAction or action_type in ('requirement_action', 'apply_modifiers_action'):
                # Multiple types of ability action, map to type
                action_type_class = ActionFactory.ACTION_TYPE_NAME_TO_CLASS[action_type]

                action_instance = action_type_class(json_dict)
            elif action_class == UpgradeAction:
                action_instance = action_class(json_dict)
            else:
                action_instance = action_class(json_dict)

            return action_instance
        except TypeError:
            return NoopAction(json_dict)
        except KeyError:
            return NoopAction(json_dict)

    @staticmethod
    def _get_action_class_and_type(path) -> Tuple[AnyStr, AnyStr]:
        path_elements = path.split('\\')
        assert len(path_elements) == 3, path_elements

        action_class = path_elements[1]
        action_type = path_elements[2].replace('.lua]]', '')

        return action_class, action_type

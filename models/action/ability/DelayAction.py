from typing import AnyStr, Dict, Union, List, Any

from models.action.AbilityAction import AbilityAction
from models.modifiers.Modifier import Modifier


class DelayAction(AbilityAction):

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def clean(self) -> Dict[AnyStr, Union[List[Dict[Any, Union[dict, Any]]], list, None]]:
        reference = DelayAction.get_reference_with_depth(self.raw_json['reference'], 2)
        clean_upgrade_actions = None
        clean_ability_actions = None
        clean_delayed_actions = None
        if 'delayed_actions' in self.raw_json:
            delayed_actions_json = self.raw_json['delayed_actions']
            if 'upgrade_actions' in delayed_actions_json:
                clean_upgrade_actions = [DelayAction._build_delay_actions(action_json) for action_json in delayed_actions_json['upgrade_actions'].values()]

            if 'ability_actions' in delayed_actions_json:
                clean_ability_actions = [DelayAction._build_delay_actions(action_json) for action_json in delayed_actions_json['ability_actions'].values()]

            if 'action_01' in delayed_actions_json:
                # Strange case where actions are directly listed under delayed_actions
                clean_delayed_actions = [DelayAction._build_delay_actions(action_json) for action_json in self.raw_json['delayed_actions'].values()]
        result = {
            'reference': reference,
            'delay': self.raw_json['delay'],
        }
        clean_actions = []
        if clean_upgrade_actions:
            clean_actions.extend([x for x in clean_upgrade_actions if x is not None])
        if clean_ability_actions:
            clean_actions.extend([x for x in clean_ability_actions if x is not None])
        if clean_delayed_actions:
            clean_actions.extend([x for x in clean_delayed_actions if x is not None])
        result['clean_delayed_actions'] = clean_actions
        return result

    @staticmethod
    def _build_delay_actions(action_json):
        reference = DelayAction.get_reference_with_depth(action_json['reference'], 2)
        if reference == 'apply_modifiers_action':
            modifiers = []
            for modifier_json in action_json['modifiers'].values():
                modifier = Modifier(modifier_json)
                modifiers.append(modifier.clean())
            return {
                'reference': reference,
                'modifiers': modifiers
            }

        # If we have recursive delay actions, skip them
        elif reference in ('delay', 'ui_decorator_action'):
            return None
        else:
            raise Exception(f"Unexpected DelayAction subaction {action_json}")


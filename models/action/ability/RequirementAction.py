from typing import AnyStr, Dict, Union, List, Any

from models.Requirement import Requirement
from utils.DictUtils import DictUtils
from models.action.AbilityAction import AbilityAction
from models.action.Action import Action
from models.action.UpgradeAction import UpgradeAction
from models.action.ability.ApplyModifiersAction import ApplyModifiersAction
from models.action.ability.DelayAction import DelayAction


class RequirementAction(AbilityAction):

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def clean(self) -> Dict[AnyStr, Union[List[Dict[Any, Union[dict, Any]]], list, None]]:
        # Get requirements from requirement_table
        if 'requirement_table' not in self.raw_json:
            return None
        requirements_json = self.raw_json['requirement_table']

        clean_requirements = [RequirementAction._build_requirement(r) for r in requirements_json.values()]

        # Get actions from action_table
        action_table_json = self.raw_json['action_table']

        clean_ability_actions = None
        clean_upgrade_actions = None
        if 'ability_actions' in action_table_json:
            clean_ability_actions = [RequirementAction._build_ability_action(a) for a in action_table_json['ability_actions'].values()]
        if 'upgrade_actions' in action_table_json:
            clean_upgrade_actions = [RequirementAction._build_upgrade_action(a) for a in action_table_json['upgrade_actions'].values()]

        return {
            'reference': Action.get_reference_with_depth(self.raw_json['reference'], 2),
            'requirements': [x for x in clean_requirements if x is not None],
            'ability_actions': [x for x in clean_ability_actions if x is not None] if clean_ability_actions else None,
            'upgrade_actions': [x for x in clean_upgrade_actions if x is not None] if clean_upgrade_actions else None,
        }

    @staticmethod
    def _build_ability_action(action_json: Dict) -> Union[Dict, None]:
        reference = RequirementAction._get_ability_upgrade_reference(action_json['reference'])
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

        elif reference == 'requirement_action':
            return RequirementAction(action_json).clean()

        elif reference in ('no_action', 'ui_unit_modifier_action', 'ui_decorator_action'):
            return None

        else:
            raise Exception(f"Unexpected ability action reference {reference} for RequirementAction")

    @staticmethod
    def _build_upgrade_action(action_json: Dict) -> Dict:
        return UpgradeAction(action_json).clean()

    @staticmethod
    def _build_requirement(requirement_json: Dict) -> Dict[AnyStr, Union[AnyStr, Dict[AnyStr, AnyStr]]]:
        if 'reference' not in requirement_json:
            return None
        reference = RequirementAction._get_requirement_reference(requirement_json['reference'])

        nested_requirements = []
        if 'requirement_table' in requirement_json:
            # have nested requirements
            for nested_requirement in requirement_json['requirement_table'].values():
                requirement = Requirement(nested_requirement)
                nested_requirements.append(requirement.clean())

        result = {
            'reference': reference,
            'nested_requirements': nested_requirements
        }
        DictUtils.add_to_dict_if_in_source(requirement_json, result, 'operation')
        DictUtils.add_to_dict_if_in_source(requirement_json, result, 'garrisoned')
        DictUtils.add_to_dict_if_in_source(requirement_json, result, 'upgrade_name')

        return result

    @staticmethod
    def _get_ability_upgrade_reference(path):
        return path.split('\\')[2].replace('.lua]]', '')

    @staticmethod
    def _get_requirement_reference(path):
        return path.split('\\')[1].replace('.lua]]', '')

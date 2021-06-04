from functools import partial
from typing import AnyStr, Dict, Union, List, Any

from models.Requirement import Requirement
from models.action.ability.ChangeMoveDataAction import ChangeMoveDataAction
from models.action.ability.TargetAction import TargetAction
from models.action.ability.UpgradeRemoveAction import UpgradeRemoveAction
from utils.DictUtils import DictUtils
from models.action.AbilityAction import AbilityAction
from models.action.Action import Action
from models.action.UpgradeAction import UpgradeAction
from models.action.ability.ApplyModifiersAction import ApplyModifiersAction
from models.action.ability.DelayAction import DelayAction
from utils.StringUtils import StringUtils


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
            clean_upgrade_actions = RequirementAction._build_clean_upgrade_actions(action_table_json['upgrade_actions'].values())

        result = {
            'reference': Action.get_reference_with_depth(self.raw_json['reference'], 2),
            'requirements': [x for x in clean_requirements if x is not None],
        }

        if clean_ability_actions:
            result['ability_actions'] = [x for x in clean_ability_actions if x is not None]
        if clean_upgrade_actions:
            result['upgrade_actions'] = [x for x in clean_upgrade_actions if x is not None]

        return result

    @staticmethod
    def _build_clean_upgrade_actions(upgrade_actions):
        try:
            result = []
            for action in upgrade_actions:
                if type(action) == str:
                    return None
                reference = action['reference']
                if reference == '[[tables\\ability_action_table.lua]]':
                    subresult = RequirementAction._build_clean_upgrade_actions(action.values())
                    result.extend(subresult)
                else:
                    # single action
                    action_instance = RequirementAction._build_upgrade_action(action)
                    result.append(action_instance)
            return result
        except KeyError:
            return []

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
        elif reference == 'change_move_data_action':
            return ChangeMoveDataAction(action_json).clean()

        elif reference == 'requirement_action':
            return RequirementAction(action_json).clean()

        elif reference == 'target':
            return TargetAction(action_json).clean()

        elif reference == 'upgrade_remove':
            return UpgradeRemoveAction(action_json).clean()

        elif reference in ('no_action', 'ui_unit_modifier_action', 'ui_decorator_action', 'activate_extension_action',
                           'animator_set_variable', 'ui_selection_type_change', 'pass_type_action', 'set_crush_mode',
                           'modify_crush_obb'):
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
        }
        if len(nested_requirements) > 0:
            result['nested_requirements'] = nested_requirements

        if 'upgrade_name' in requirement_json:
            result['upgrade_name'] = StringUtils.remove_bracket_file_endings(requirement_json['upgrade_name'])

        add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, requirement_json, result)
        add_to_dict_partial('is_present')
        add_to_dict_partial('slot_item')
        add_to_dict_partial('min_owned')
        add_to_dict_partial('max_owned')
        add_to_dict_partial('not_moving')
        add_to_dict_partial('garrisoned')
        add_to_dict_partial('max_cap')
        add_to_dict_partial('in_supply')
        add_to_dict_partial('comparison')
        add_to_dict_partial('number_of_members')
        add_to_dict_partial('veterancy_rank')
        add_to_dict_partial('cover_type_table')

        return result

    @staticmethod
    def _get_ability_upgrade_reference(path):
        return path.split('\\')[2].replace('.lua]]', '')

    @staticmethod
    def _get_requirement_reference(path):
        return path.split('\\')[1].replace('.lua]]', '')

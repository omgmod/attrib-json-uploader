from typing import List, Dict, Union

from factories.ActionFactory import ActionFactory
from models.AbstractModel import AbstractModel
from models.Requirement import Requirement
from utils.DictUtils import DictUtils


class Ability(AbstractModel):

    # Note: filepath name is 'abilities'

    def __init__(self, raw_json, filename,):
        super().__init__(raw_json)
        self.filename = filename

    def clean(self):
        """
            Properties to get:
                ability_bag
                    action_list
                        start_self_actions
                            action_0X
                        end_self_actions
                        start_target_actions
                        end_target_actions
                    activation
                    duration_time
                    recharge_time
                    requirements
                        required_X
        """
        actions = self.get_actions()
        requirements = self.get_requirements()

        result = {
            'reference': self.filename,
            'actions': actions
        }
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'activation')
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'duration_time')
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'recharge_time')
        if requirements:
            result['requirements'] = requirements
        return result

    def get_actions(self) -> Union[None, List[Dict]]:
        """
            If the sbps has squad actions, break them down as Action objects
        """
        try:
            actions_dict = self.raw_json['ability_bag']['action_list']
            actions = []
            actions.extend(Ability._build_actions_for_actions_table(actions_dict, 'start_self_actions'))
            actions.extend(Ability._build_actions_for_actions_table(actions_dict, 'end_self_actions'))
            actions.extend(Ability._build_actions_for_actions_table(actions_dict, 'start_target_actions'))
            actions.extend(Ability._build_actions_for_actions_table(actions_dict, 'end_target_actions'))
        except KeyError:
            actions = None

        return actions

    def get_requirements(self):
        if 'requirements' in self.raw_json:
            requirements_dict = self.raw_json['requirements']
            requirements = []
            for requirement_dict in requirements_dict.values():
                requirement = Requirement(requirement_dict)
                requirements.append(requirement.clean())
            return requirements
        else:
            return None

    @staticmethod
    def _build_actions_for_actions_table(actions_table_dict, actions_list_key):
        result = []
        if actions_list_key not in actions_table_dict:
            return result
        for action_dict in actions_table_dict[actions_list_key].values():
            action = ActionFactory.create_action_from_json(action_dict)
            clean_action = action.clean()
            if clean_action:
                result.append(clean_action)
        return result

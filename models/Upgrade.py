from typing import Union, Dict, List

from factories.ActionFactory import ActionFactory
from models.AbstractModel import AbstractModel
from models.Requirement import Requirement
from utils.StringUtils import StringUtils


class Upgrade(AbstractModel):
    def __init__(self, constname, faction, filename, raw_json):
        upgrade_bag_dict = raw_json['upgrade_bag']
        super().__init__(upgrade_bag_dict)
        self.constname = constname
        self.faction = faction
        self.upgrade_filename = StringUtils.remove_file_endings(filename)

    def clean(self):
        """
            Properties
                upgrade_bag
                    actions
                        action_0X
                    requirements
                        required_1
        """
        actions = self.get_actions()
        requirements = self.get_requirements()
        result = {
            'reference': self.upgrade_filename,
            'constname': self.constname,
            'faction': self.faction,
            'actions': actions
        }
        if requirements:
            result['requirements'] = requirements
        return result

    def get_actions(self) -> Union[None, List[Dict]]:
        """
            If the sbps has squad actions, break them down as Action objects
        """
        try:
            actions_dict = self.raw_json['actions']
            actions = []
            for action_dict in actions_dict.values():
                action = ActionFactory.create_action_from_json(action_dict)
                clean_action = action.clean()
                if clean_action:
                    actions.append(clean_action)
        except KeyError:
            actions = None

        return actions

    def get_requirements(self):
        if 'requirements' in self.raw_json:
            requirements_dict = self.raw_json['requirements']
            requirements = []
            for requirement_dict in requirements_dict.values():
                requirement = Requirement(requirement_dict)
                if requirement.is_usable():
                    requirements.append(requirement.clean())
            return requirements
        else:
            return None



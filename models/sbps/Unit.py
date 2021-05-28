import json
from typing import AnyStr, Dict, List, Union

from ActionFactory import ActionFactory
from FileUtils import FileUtils
from models.AbstractModel import AbstractModel
from models.SquadVeterancy import SquadVeterancy


class Unit(AbstractModel):
    """
        Represents a specific squad blueprint.

        A unit in warcp2 that is upgraded to change the composition of its members will map to a squad blueprint different
        from the one a vanilla version of the unit would map to.
    """

    def __init__(self, constname, faction, filename, sbps_json):
        super().__init__(sbps_json)  # self.raw_json
        self.constname = constname
        self.faction = faction
        self.sbps_filename = filename

    def clean(self):
        """
            Parse the raw_json dict into a condensed dictionary with only the values we need.
        """
        pass

    def get_abilities(self) -> Union[None, List[AnyStr]]:
        """
            If the sbps has squad abilities, returns them as a list in format [[abilities\\X_ability.lua]]
        """
        try:
            abilities_dict = self.raw_json['squad_ability_ext']['abilities']
            abilities = list(abilities_dict.values())
        except KeyError:
            abilities = None
        return abilities

    def get_actions(self) -> Union[None, List[Dict]]:
        """
            If the sbps has squad actions, break them down as Action objects
        """
        try:
            actions_dict = self.raw_json['squad_action_apply_ext']['actions']
            actions = []
            if 'ability_actions' in actions_dict:
                for action_dict in actions_dict['ability_actions'].values():
                    action = ActionFactory.create_action_from_json(action_dict)
                    clean_action = action.clean()
                    if clean_action:
                        actions.append(clean_action)
            if 'upgrade_actions' in actions_dict:
                for action_dict in actions_dict['upgrade_actions'].values():
                    action = ActionFactory.create_action_from_json(action_dict)
                    clean_action = action.clean()
                    if clean_action:
                        actions.append(clean_action)
        except KeyError:
            actions = None

        return actions

    def get_loadout(self) -> Dict[AnyStr, int]:
        """
            Get ebps references and numbers for the squad loadout.
        """
        unit_list_dict = self.raw_json['squad_loadout_ext']['unit_list']
        loadout = {}
        for unit_dict in unit_list_dict.values():
            # Somehow some sbps have unused units in the loadout without type, skip them
            if 'type' in unit_dict:
                ebps = unit_dict['type']['type']
                number = unit_dict.get('num', 1)  # default to 1 if no number given
                loadout[ebps] = number

        return loadout

    def get_veterancy(self) -> Dict:
        """
            Get exp and modifiers for Vet 1 through 5
        """
        veterancy_rank_info_dict = self.raw_json['squad_veterancy_ext']['veterancy_rank_info']
        squad_veterancy = SquadVeterancy(veterancy_rank_info_dict)

        return squad_veterancy.clean()

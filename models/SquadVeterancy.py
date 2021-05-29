from factories.ActionFactory import ActionFactory
from models.AbstractModel import AbstractModel
from models.modifiers.Modifier import Modifier


class SquadVeterancy(AbstractModel):

    def __init__(self, raw_json):
        """ """
        super().__init__(raw_json)

    def clean(self):
        results = {}
        for i in range(1, 6):
            rank_key = f'veterancy_rank_0{i}'
            if rank_key not in self.raw_json:
                continue
            rank_data = self.raw_json[rank_key]

            squad_actions = rank_data['squad_actions']
            actions = []
            for key, action_dict in squad_actions.items():
                if type(action_dict) == str:
                    print(f"Found string value in squad_actions: {key} - {action_dict}")
                    continue
                if 'modifier' in action_dict['reference'].split('\\')[0]:
                    # Sometimes this is a modifier even though it's supposed to be a list of actions
                    modifier = Modifier(action_dict)
                    actions.append(modifier.clean())
                else:
                    action = ActionFactory.create_action_from_json(action_dict)
                    clean_action = action.clean()
                    if clean_action:
                        actions.append(clean_action)

            results[i] = {
                'experience_value': rank_data['experience_value'],
                'action': actions
            }
        return results

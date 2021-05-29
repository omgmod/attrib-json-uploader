from factories.ActionFactory import ActionFactory
from models.AbstractModel import AbstractModel
from utils.DictUtils import DictUtils


class Cover(AbstractModel):
    def __init__(self, raw_json, cover_type):
        super().__init__(raw_json)
        self.cover_type = cover_type

    def clean(self):
        result = {
            'reference': self.cover_type
        }

        if 'actions' in self.raw_json:
            actions = []
            for action_json in self.raw_json['actions'].values():
                action = ActionFactory.create_action_from_json(action_json)
                clean_action = action.clean()
                if clean_action:
                    actions.append(clean_action)
            if actions:
                result['actions'] = actions

        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'speed_multiplier')
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'safety_value')
        return result

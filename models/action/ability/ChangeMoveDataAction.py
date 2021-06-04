from models.action.AbilityAction import AbilityAction
from utils.DictUtils import DictUtils


class ChangeMoveDataAction(AbilityAction):

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def clean(self):
        reference = ChangeMoveDataAction.get_reference_with_depth(self.raw_json['reference'], 2)
        result = {
            'reference': reference,
        }
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'acceleration_multiplier')
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'deceleration_multiplier')

        return result

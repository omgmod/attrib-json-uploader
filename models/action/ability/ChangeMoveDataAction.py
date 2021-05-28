from models.action.AbilityAction import AbilityAction


class ChangeMoveDataAction(AbilityAction):

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def clean(self):
        reference = ChangeMoveDataAction.get_reference_with_depth(self.raw_json['reference'], 2)
        return {
            'reference': reference,
            'acceleration_multiplier': self.raw_json['acceleration_multiplier']
        }

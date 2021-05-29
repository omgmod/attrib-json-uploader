from models.action.Action import Action
from models.modifiers.Modifier import Modifier
from utils.DictUtils import DictUtils


class CriticalAction(Action):

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def clean(self):
        """

        """
        reference = CriticalAction.get_reference_with_depth(self.raw_json['reference'], 2)

        result = {
            'reference': reference,
        }
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'duration')
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'permanent')

        if 'modifiers' in self.raw_json:
            modifiers = []
            for modifier_json in self.raw_json['modifiers'].values():
                modifier = Modifier(modifier_json)
                modifiers.append(modifier.clean())
            if modifiers:
                result['modifiers'] = modifiers
        if not set(self.raw_json.keys()).issubset(CriticalAction.EXPECTED_KEYS):
            if reference == '[[action\\critical_action\\animator_set_action.lua]]':
                return None
            raise Exception(f"Unexpected CriticalAction keys {set(self.raw_json.keys()).difference(CriticalAction.EXPECTED_KEYS)}")

        return result

    EXPECTED_KEYS = {'reference', 'duration', 'permanent', 'modifiers', 'action_name'}

from utils.DictUtils import DictUtils
from models.action.AbilityAction import AbilityAction
from models.modifiers.Modifier import Modifier


class ApplyModifiersAction(AbilityAction):

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def clean(self):
        # Build a list of modifiers
        reference = ApplyModifiersAction._get_ability_upgrade_reference(self.raw_json['reference'])

        if 'modifiers' not in self.raw_json.keys():
            return None

        modifiers = []
        for modifier_json in self.raw_json['modifiers'].values():
            modifier = Modifier(modifier_json)
            modifiers.append(modifier.clean())
        result = {
            'reference': reference,
            'modifiers': modifiers
        }
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'duration',)
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'permanent',)

        return result

    @staticmethod
    def _get_ability_upgrade_reference(path):
        return path.split('\\')[2].replace('.lua]]', '')

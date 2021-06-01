from models.action.AbilityAction import AbilityAction
from utils.StringUtils import StringUtils


class UpgradeRemoveAction(AbilityAction):

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def clean(self):
        reference = UpgradeRemoveAction.get_reference_with_depth(self.raw_json['reference'], 2)

        result = {
            'reference': reference,
        }
        if 'apply_to_entities_in_squad' in self.raw_json:
            result['apply_to_entities_in_squad'] = self.raw_json['apply_to_entities_in_squad']
        if 'upgrade' in self.raw_json:
            result['upgrade'] = StringUtils.remove_bracket_file_endings(self.raw_json['upgrade'])

        return result

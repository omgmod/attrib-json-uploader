from utils.DictUtils import DictUtils
from models.AbstractModel import AbstractModel


class Modifier(AbstractModel):

    def __init__(self, raw_json):
        """

        """
        super().__init__(raw_json)

    def clean(self):
        result = {
            'reference': Modifier._get_modifier_name(self.raw_json['reference']),
        }
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'value')
        if 'target_type_name' in self.raw_json:
            result['target_type_name'] = self.raw_json['target_type_name']
        if 'application_type' in self.raw_json:
            result['application_type'] = Modifier._strip_brackets(self.raw_json['application_type'])
        if 'usage_type' in self.raw_json:
            result['usage_type'] = Modifier._strip_brackets(self.raw_json['usage_type'])
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'exclusive')
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'modifier_id')

        if result.keys() != self.raw_json.keys():
            raise Exception(f'Modifier result keys {result.keys()} different from raw modifier keys {self.raw_json.keys()}')

        return result

    @staticmethod
    def _get_modifier_name(raw_modifier_path):
        """
            Pull the modifier name out of the path
        """
        return raw_modifier_path.replace('[[modifiers\\', '').replace('.lua]]', '')

    @staticmethod
    def _strip_brackets(raw_name):
        return raw_name.replace('[[', '').replace(']]', '')

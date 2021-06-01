from functools import partial

from models.AbstractModel import AbstractModel
from utils.DictUtils import DictUtils


class Requirement(AbstractModel):

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def is_usable(self):
        return 'reference' in self.raw_json

    def clean(self):
        """

        """
        reference = Requirement._get_requirement_reference(self.raw_json['reference'])
        result = {
            'reference': reference
        }
        add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, self.raw_json, result)
        add_to_dict_partial('upgrade_name')
        add_to_dict_partial('is_present')
        add_to_dict_partial('upgrade_name')
        add_to_dict_partial('slot_item')
        add_to_dict_partial('min_owned')
        add_to_dict_partial('max_owned')
        add_to_dict_partial('not_moving')
        add_to_dict_partial('garrisoned')
        add_to_dict_partial('max_cap')
        add_to_dict_partial('in_supply')
        add_to_dict_partial('comparison')
        add_to_dict_partial('number_of_members')
        add_to_dict_partial('veterancy_rank')
        add_to_dict_partial('cover_type_table')
        if not set(self.raw_json.keys()).issubset(Requirement.EXPECTED_NESTED_REQUIREMENT_KEYS):
            if 'reason' in self.raw_json and self.raw_json['reason'] == '[[usage_and_display]]':
                pass
            elif 'structure_name' in self.raw_json:
                pass
            else:
                raise Exception(f"Unexpected Requirement keys {set(self.raw_json.keys()).difference(Requirement.EXPECTED_NESTED_REQUIREMENT_KEYS)}")
        return result

    @staticmethod
    def _get_requirement_reference(path):
        return path.split('\\')[1].replace('.lua]]', '')

    EXPECTED_NESTED_REQUIREMENT_KEYS = {'reference', 'not_moving', 'slot_item', 'min_owned', 'max_owned',
                                        'ui_name', 'garrisoned', 'is_present', 'upgrade_name', 'max_cap', 'reason',
                                        'in_supply', 'comparison', 'number_of_members', 'veterancy_rank', 'cover_type_table',
                                        'display_requirement', 'include_queued'}

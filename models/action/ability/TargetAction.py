from typing import AnyStr, Dict, Union, List, Any

from models.TargetInfo import TargetInfo
from models.action.AbilityAction import AbilityAction
from models.action.ability.ApplyModifiersAction import ApplyModifiersAction
from models.modifiers.Modifier import Modifier
from utils.DictUtils import DictUtils
from utils.StringUtils import StringUtils


class TargetAction(AbilityAction):

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def clean(self):
        reference = TargetAction.get_reference_with_depth(self.raw_json['reference'], 2)
        subactions = self.get_subactions()

        result = {
            'reference': reference,
            'target_info': TargetInfo(self.raw_json['target_info']).clean()
        }
        if subactions:
            result['subactions'] = subactions

        DictUtils.add_to_dict_if_in_source(self.raw_json, result, StringUtils.remove_bracket_wrapping('unit_type'))
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'stationary')

        return result

    def get_subactions(self):
        if 'subactions' in self.raw_json:
            results = []
            for subaction_dict in self.raw_json['subactions'].values():
                reference = StringUtils.remove_bracket_file_endings(subaction_dict['reference'])

                if 'apply_modifiers_action' in reference:
                    results.append(ApplyModifiersAction(subaction_dict).clean())

                else:
                    raise Exception(f"Unexpected target action subaction {subaction_dict}")
            return results
        else:
            return None

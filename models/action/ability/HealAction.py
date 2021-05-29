from typing import AnyStr, Dict, Union, List, Any

from models.TargetInfo import TargetInfo
from models.action.AbilityAction import AbilityAction
from models.modifiers.Modifier import Modifier
from utils.DictUtils import DictUtils


class HealAction(AbilityAction):

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def clean(self):
        reference = HealAction.get_reference_with_depth(self.raw_json['reference'], 2)

        result = {
            'reference': reference,
            'target_info': TargetInfo(self.raw_json['target_info']).clean()
        }

        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'amount')
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'bonus_health_amount')


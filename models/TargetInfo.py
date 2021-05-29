from functools import partial

from models.AbstractModel import AbstractModel
from utils.DictUtils import DictUtils
from utils.StringUtils import StringUtils


class TargetInfo(AbstractModel):

    def __init__(self, raw_json):
        super().__init__(raw_json)

    def clean(self):
        reference = TargetInfo.get_reference_with_depth(self.raw_json['reference'], 1)
        if reference == TargetInfo.BINARY_EXPRESSION:
            # handle binary expression of two TargetInfos
            result = {
                'reference': reference,
                'operation': StringUtils.remove_bracket_wrapping(self.raw_json['operation']),
                'target_info_1': TargetInfo(self.raw_json['target_info_1']).clean(),
                'target_info_2': TargetInfo(self.raw_json['target_info_2']).clean(),
            }
        elif reference == TargetInfo.UNARY_EXPRESSION:
            # handle unary expression of one TargetInfo
            result = {
                'reference': reference,
                'operation': StringUtils.remove_bracket_wrapping(self.raw_json['operation']),
                'target_info': StringUtils.remove_bracket_wrapping(self.raw_json['target_info']),
            }

        else:
            # Simple TargetInfo
            result = {
                'reference': reference
            }
            add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, self.raw_json, result)
            add_to_dict_partial('unit_type')

            if not set(self.raw_json.keys()).issubset(TargetInfo.EXPECTED_LEAF_TARGET_INFO_KEYS):
                raise Exception(f"Unexpected TargetInfo keys {set(self.raw_json.keys()).difference(TargetInfo.EXPECTED_LEAF_TARGET_INFO_KEYS)}")

        return result

    BINARY_EXPRESSION = 'binary_expr'
    UNARY_EXPRESSION = 'unary_expr'

    EXPECTED_LEAF_TARGET_INFO_KEYS = ('reference', 'unit_type')

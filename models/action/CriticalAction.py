from models.SlotItem import SlotItem
from models.action.Action import Action
from models.modifiers.Modifier import Modifier
from utils.DictUtils import DictUtils
from utils.StringUtils import StringUtils


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
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'damage')
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'percentage')

        if 'modifiers' in self.raw_json:
            modifiers = []
            for modifier_json in self.raw_json['modifiers'].values():
                modifier = Modifier(modifier_json)
                modifiers.append(modifier.clean())
            if modifiers:
                result['modifiers'] = modifiers
        elif reference == 'slot_item_apply':
            result['slot_item'] = StringUtils.remove_bracket_file_endings(self.raw_json['slot_item'])
        elif reference == 'apply_crew_action':
            result['crew_name'] = StringUtils.remove_bracket_wrapping(self.raw_json['crew_name'])

        if not set(self.raw_json.keys()).issubset(CriticalAction.EXPECTED_KEYS):
            if reference == '[[action\\critical_action\\animator_set_action.lua]]':
                return None
            raise Exception(f"Unexpected CriticalAction keys {set(self.raw_json.keys()).difference(CriticalAction.EXPECTED_KEYS)}")

        return result

    EXPECTED_KEYS = {'reference', 'duration', 'permanent', 'modifiers', 'action_name', 'slot_item',
                     'crew_name', 'damage', 'percentage',
                     'do_action_state_name', 'state_machine_name', 'scale_x', 'scale_y', 'deform_decal', 'undoable'}

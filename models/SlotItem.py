from models.AbstractModel import AbstractModel
from utils.DictUtils import DictUtils
from utils.StringUtils import StringUtils


class SlotItem(AbstractModel):

    def __init__(self, raw_json, filename):
        slot_item_bag_dict = raw_json['slot_item_bag']

        super().__init__(slot_item_bag_dict)
        self.filename = filename

    def clean(self):
        """
            Properties
                drop_rate
                slot_size
                weapon references [weapon]
        """
        weapon = self.get_weapon()

        result = {
            'reference': self.filename,
        }
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'drop_rate')
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'slot_size')
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'item_uses')
        if weapon:
            result['weapon'] = weapon
        return result

    def get_weapon(self):
        try:
            weapon_dict = self.raw_json['weapon']
            result = {
                'type': StringUtils.remove_bracket_wrapping(weapon_dict['type']),
                'weapon': StringUtils.remove_bracket_file_endings(weapon_dict['weapon']),
            }
            return result
        except KeyError:
            return None

from pprint import pprint
from utils.FileUtils import FileUtils
from utils.StringUtils import StringUtils

up = FileUtils.read_json_file('./json/raw/ebps_stats.json')

panther = up['races']['axis_panzer_elite']['vehicles']['pe_panther']


def get_weapons(entity):
    weapons = []
    try:
        hardpoints = entity['combat_ext']['hardpoints']
        for hardpoint_dict in hardpoints.values():
            try:
                for weapon_dict in hardpoint_dict['weapon_table'].values():
                    if 'type' in weapon_dict and weapon_dict['type'] == '[[accessory]]':
                        continue
                    weapon = weapon_dict['weapon']
                    weapons.append(StringUtils.remove_bracket_file_endings(weapon))
                if len(hardpoint_dict['weapon_table']) > 1 and hardpoint_dict['weapon_table']['weapon_02']['type'] != '[[accessory]]':
                    if hardpoint_dict['weapon_table']['weapon_01']['weapon'] == hardpoint_dict['weapon_table']['weapon_02']['weapon']:
                        print(
                            f"WARNING - Duplicate weapons for hardpoint {pprint(hardpoint_dict['weapon_table'])}")
                    else:
                        print(
                            f"WARNING -  More than one weapon found for a hardpoint weapon table {pprint(hardpoint_dict['weapon_table'])}")
            except KeyError:
                continue
    except KeyError:
        pass
    return weapons

result = get_weapons(panther)

print(result)

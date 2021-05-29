from models.Cover import Cover
from models.ebps.Entity import Entity
from utils.DictUtils import DictUtils
from utils.StringUtils import StringUtils


class Vehicle(Entity):

    def __init__(self, raw_json, faction, filename):
        super().__init__(raw_json, faction, filename)

    def clean(self):
        """
            Properties to look at:
                ability_ext.abilities.ability_0X references [abilities]
                combat_ext.hardpoints.hardpoint_0X
                    weapon_table.weapon_01.weapon references [weapon]
                cover_ext.tp_X references [cover]
                crush_ext
                    default_crush_mode
                    crushes_humans
                health_ext
                    hitpoints
                    rear_damage_critical_type references [type_target_critical]
                    rear_damage_enabled
                hit_object_ext.projectile_pass_through - Don't know how to use this
                hold_ext
                    num_slots
                    num_squad_slots
                    percent_unload_on_death
                moving_ext
                    acceleration
                    deceleration
                    speed_max
                    rotation_rate
                population_ext.personnel_pop
                sight_ext
                    detect_camouflage.tp_global
                    sight_package.outer_radius
                type_ext
                    type_target_weapon references [type_target_weapon]
                    type_target_critical references [type_target_critical]
                veterancy_ext.experience_value
        """
        print(f"Processing [{self.ebps_filename}]")

        abilities = self.get_abilities()
        weapons = self.get_weapons()
        cover = self.get_cover()
        crush = self.get_crush()
        health = self.get_health()
        hold = self.get_hold()
        moving = self.get_moving()
        population = self.get_population()
        sight = self.get_sight()
        types = self.get_types()
        veterancy_value = self.get_veterancy_value()

        result = {
            'reference': self.ebps_filename,
            'faction': self.faction,
            'type': 'vehicle',
            'cover': cover,
        }
        if abilities:
            result['abilities'] = abilities
        if crush:
            result['crush'] = crush
        if hold:
            result['hold'] = hold
        if len(weapons) > 0:
            result['weapons'] = weapons
        if moving:
            result['moving'] = moving
        result.update(health)
        result.update(population)
        result.update(sight)
        result.update(types)
        result.update(veterancy_value)
        return result

    def get_crush(self):
        try:
            crush_ext_dict = self.raw_json['crush_ext']
            result = {
                'crushes_humans': crush_ext_dict['crushes_humans'],
            }
            DictUtils.add_to_dict_if_in_source(crush_ext_dict, result, 'default_crush_mode')
            return result
        except KeyError:
            return None

    def get_hold(self):
        try:
            hold_ext_dict = self.raw_json['hold_ext']
            return {
                'num_slots': hold_ext_dict['num_slots'],
                'num_squad_slots': hold_ext_dict['num_squad_slots'],
                'percent_unload_on_death': hold_ext_dict['percent_unload_on_death'],
            }
        except KeyError:
            return None

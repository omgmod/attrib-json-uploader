from factories.ActionFactory import ActionFactory
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
                action_apply_ext.actions
                    ability_actions.action_0X
                    critical_actions.action_0X
                    upgrade_actions.action_0X
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
        actions = self.get_actions()
        weapons = self.get_weapons()
        hardpoints = self.get_hardpoints()
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
        }
        if abilities:
            result['abilities'] = abilities
        if actions:
            result['actions'] = actions
        if cover:
            result['cover'] = cover
        if crush:
            result['crush'] = crush
        if hold:
            result['hold'] = hold
        if len(weapons) > 0:
            result['weapons'] = weapons
        if len(hardpoints) > 0:
            result['hardpoints'] = hardpoints
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
            result = {}
            DictUtils.add_to_dict_if_in_source(crush_ext_dict, result, 'crushes_humans')
            DictUtils.add_to_dict_if_in_source(crush_ext_dict, result, 'default_crush_mode')
            return result
        except KeyError:
            return None

    def get_hold(self):
        try:
            hold_ext_dict = self.raw_json['hold_ext']
            on_loaded_hold_actions = []
            if 'on_loaded_hold_actions' in hold_ext_dict:
                for action_dict in hold_ext_dict['on_loaded_hold_actions'].values():
                    action = ActionFactory.create_action_from_json(action_dict)
                    clean_action = action.clean()
                    if clean_action:
                        on_loaded_hold_actions.append(clean_action)

            on_loaded_squad_actions = []
            if 'on_loaded_squad_actions' in hold_ext_dict:
                if 'ability_actions' in hold_ext_dict['on_loaded_squad_actions']:
                    for action_dict in hold_ext_dict['on_loaded_squad_actions']['ability_actions'].values():
                        action = ActionFactory.create_action_from_json(action_dict)
                        clean_action = action.clean()
                        if clean_action:
                            on_loaded_squad_actions.append(clean_action)
                if 'upgrade_actions' in hold_ext_dict['on_loaded_squad_actions']:
                    for action_dict in hold_ext_dict['on_loaded_squad_actions']['upgrade_actions'].values():
                        action = ActionFactory.create_action_from_json(action_dict)
                        clean_action = action.clean()
                        if clean_action:
                            on_loaded_squad_actions.append(clean_action)

            result = {}
            DictUtils.add_to_dict_if_in_source(hold_ext_dict, result, 'num_slots')
            DictUtils.add_to_dict_if_in_source(hold_ext_dict, result, 'num_squad_slots')
            DictUtils.add_to_dict_if_in_source(hold_ext_dict, result, 'percent_unload_on_death')

            if len(on_loaded_hold_actions) > 0:
                result['on_loaded_hold_actions'] = on_loaded_hold_actions
            if len(on_loaded_squad_actions) > 0:
                result['on_loaded_squad_actions'] = on_loaded_squad_actions

            return result
        except KeyError:
            return None

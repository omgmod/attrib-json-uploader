from factories.ActionFactory import ActionFactory
from models.Requirement import Requirement
from models.ebps.Entity import Entity


class Building(Entity):

    def __init__(self, raw_json, faction, filename):
        super().__init__(raw_json, faction, filename)

    def clean(self):
        """
            Properties to look at:
                action_apply_ext.actions
                    ability_actions.action_0X references [AbilityAction]
                    upgrade_actions.action_0X references [UpgradeAction]
                aide_station_ext
                    casualty_search_radius
                    number_of_medics
                combat_ext.hardpoints.hardpoints_01.weapon_table.weapon_01.weapon references [weapon]
                construction_ext.on_construction_actions
                    ability_actions.action_0X references [AbilityAction]
                    upgrade_actions.action_0X references [UpgradeAction]
                cost_ext.time_cost.time_seconds
                garrison_ext.max_units
                health_ext.hitpoints
                population_ext.personnel_pop
                requirement_ext
                    requirement_table.required_1 references [requirements]
                sight_ext
                    sight_package.outer_radius
                type_ext
                    type_target_weapon references [type_target_weapon]
                    type_target_critical references [type_target_critical]
                veterancy_ext.experience_value
        """
        print(f"Processing [{self.ebps_filename}]")

        abilities = self.get_abilities()
        actions = self.get_actions()
        aide_station = self.get_aide_station()
        weapons = self.get_weapons()
        construction = self.get_construction()
        cost = self.get_cost()
        garrison = self.get_garrison()
        health = self.get_health()
        population = self.get_population()
        requirement = self.get_requirement()
        sight = self.get_sight()
        types = self.get_types()
        veterancy_value = self.get_veterancy_value()

        result = {
            'reference': self.ebps_filename,
            'faction': self.faction,
            'type': 'building',
        }
        if abilities:
            result['abilities'] = abilities
        if actions:
            result['actions'] = actions
        if aide_station:
            result['aide_station'] = aide_station
        if construction:
            result['construction'] = construction
        if garrison:
            result['garrison'] = garrison
        if requirement:
            result['requirement'] = requirement
        if len(weapons) > 0:
            result['weapons'] = weapons
        result.update(cost)
        result.update(health)
        result.update(population)
        result.update(sight)
        result.update(types)
        result.update(veterancy_value)
        return result

    def get_aide_station(self):
        try:
            aide_station_ext_dict = self.raw_json['aide_station_ext']
            return {
                'casualty_search_radius': aide_station_ext_dict['casualty_search_radius'],
                'number_of_medics': aide_station_ext_dict['number_of_medics']
            }
        except KeyError:
            return None

    def get_construction(self):
        try:
            construction_action_table_json = self.raw_json['construction_ext']['on_construction_actions']

            clean_ability_actions = None
            clean_upgrade_actions = None
            if 'ability_actions' in construction_action_table_json:
                clean_ability_actions = [ActionFactory.create_action_from_json(a).clean() for a in
                                         construction_action_table_json['ability_actions'].values()]
            if 'upgrade_actions' in construction_action_table_json:
                clean_upgrade_actions = [ActionFactory.create_action_from_json(a).clean() for a in
                                         construction_action_table_json['upgrade_actions'].values()]
            clean_actions = []
            if clean_ability_actions:
                clean_actions.extend([x for x in clean_ability_actions if x is not None])
            if clean_upgrade_actions:
                clean_actions.extend([x for x in clean_upgrade_actions if x is not None])
            return clean_actions
        except KeyError:
            return None

    def get_cost(self):
        cost = {}
        try:
            cost_ext = self.raw_json['cost_ext']
            cost['time_cost'] = cost_ext['time_cost']['time_seconds']
        except KeyError:
            pass
        return cost

    def get_garrison(self):
        try:
            garrison_ext_dict = self.raw_json['garrison_ext']
            return {
                'max_units': garrison_ext_dict['max_units'],
            }
        except KeyError:
            return None

    def get_requirement(self):
        try:
            requirement_table_dict = self.raw_json['requirement_ext']['requirement_table']
            requirements = []
            for requirement_dict in requirement_table_dict.values():
                requirement = Requirement(requirement_dict)
                requirements.append(requirement.clean())
            return requirements
        except KeyError:
            return None

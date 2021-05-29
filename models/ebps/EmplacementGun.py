from models.ebps.Entity import Entity
from utils.StringUtils import StringUtils


class EmplacementGun(Entity):
    def __init__(self, raw_json, faction, filename):
        super().__init__(raw_json, faction, filename)

    def clean(self):
        """
            Properties
                ability_ext.abilities.ability_0X references [abilities]
                action_apply_ext.actions
                    ability_actions.action_0X references [AbilityAction]
                    upgrade_actions.action_0X references [UpgradeAction]
                combat_ext.hardpoints.hardpoint_01.weapon_table.weapon_01.weapon references [weapon]

                construction_ext.construction_menus.construction_menu_entry_01.construction_type

                health_ext.hitpoints
                population_ext.personnel_pop
                sight_ext
                type_ext
                veterancy_ext
        """
        print(f"Processing [{self.ebps_filename}]")

        abilities = self.get_abilities()
        actions = self.get_actions()
        weapons = self.get_weapons()
        construction_type = self.get_construction_type()
        health = self.get_health()
        population = self.get_population()
        sight = self.get_sight()
        types = self.get_types()
        veterancy_value = self.get_veterancy_value()

        result = {
            'reference': self.ebps_filename,
            'faction': self.faction,
            'type': 'emplacement_gun',
            'construction_type': construction_type,
        }
        if abilities:
            result['abilities'] = abilities
        if actions:
            result['actions'] = actions
        if len(weapons) > 0:
            result['weapons'] = weapons
        result.update(health)
        result.update(population)
        result.update(sight)
        result.update(types)
        result.update(veterancy_value)
        return result

    def get_construction_type(self):
        return {
            'construction_type': StringUtils.remove_bracket_wrapping(self.raw_json['construction_ext']['construction_menus']['construction_menu_entry_01']['construction_type'])
        }

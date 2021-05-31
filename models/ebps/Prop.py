from models.ebps.Entity import Entity


class Prop(Entity):
    def __init__(self, raw_json, faction, filename):
        super().__init__(raw_json, faction, filename)

    def clean(self):
        """
            Properties
                ability_ext.abilities.ability_0X references [abilities]
                action_apply_ext.actions.ability_actions.action_0X references [action]
                combat_ext.hardpoints.hardpoint_01.weapon_table.weapon_01.weapon references [weapon]
                health_ext.hitpoints
                type_ext
                    type_target_weapon
                    type_target_critical
        """
        abilities = self.get_abilities()
        actions = self.get_actions()
        weapons = self.get_weapons()
        health = self.get_health()
        types = self.get_types()

        result = {
            'reference': self.ebps_filename,
            'type': 'prop',
        }
        if abilities:
            result['abilities'] = abilities
        if actions:
            result['actions'] = actions
        if len(weapons) > 0:
            result['weapons'] = weapons
        result.update(health)
        result.update(types)

        return result

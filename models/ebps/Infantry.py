from models.ebps.Entity import Entity


class Infantry(Entity):

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
                camoflage_ext                   SKIP FOR NOW
                    attack_priority
                    detection_radius
                    first_strike_actions.ability_actions.action_0X references [actions]
                combat_ext.hardpoints.hardpoint_01.weapon_table.weapon_01.weapon references [weapon]
                cover_ext.tp_X references [cover]
                health_ext
                    hitpoints
                moving_ext.speed_max
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
        health = self.get_health()
        moving = self.get_moving()
        population = self.get_population()
        sight = self.get_sight()
        types = self.get_types()
        veterancy_value = self.get_veterancy_value()

        result = {
            'reference': self.ebps_filename,
            'faction': self.faction,
            'type': 'infantry',
            'cover': cover,
            'moving': moving
        }
        if abilities:
            result['abilities'] = abilities
        if actions:
            result['actions'] = actions
        if len(weapons) > 0:
            result['weapons'] = weapons
        if len(hardpoints) > 0:
            result['hardpoints'] = hardpoints
        result.update(health)
        result.update(population)
        result.update(sight)
        result.update(types)
        result.update(veterancy_value)
        return result

    def get_camouflage(self):
        # Skip for now
        pass




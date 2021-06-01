from models.sbps.Unit import Unit


class Vehicle(Unit):
    def __init__(self, constname, faction, filename, sbps_json):
        super().__init__(constname, faction, filename, sbps_json)

    def clean(self):
        """
            Parse the raw sbps_json dict into a condensed dictionary with only the values we need.

            Properties to look at:
                squad_ability_ext.abilities.ability_0X references [abilities]
                squad_action_apply_ext.actions
                    ability_actions.action_0X references [action]
                        - apply_modifiers_action
                            modifiers.modifiers_0X references [modifiers]
                                value
                                application_type (optional)
                                usage_type (optional)
                        - requirement_action
                            action_table
                                ability_actions.action_01 references [action] most likely apply_modifiers_action
                                    [modifiers block]
                                upgrade_actions.action_01 references [action] most likely apply_modifiers_action
                                    [modifiers block]
                            requirement_table.required_X references [requirements]
                                operation if requirement is logical operator like required_unary_expr this could be [[not]]
                                requirement_table.required_X references [requirements]
                                    min_owned
                                    max_owned
                                    slot_item references [slot_item]
                    upgrade_actions
                squad_loadout_ext.unit_list.unit_01
                    type.type references [ebps]
                squad_upgrade_apply_ext.upgrades.upgrade_0X references [upgrade}
                squad_upgrade_ext.upgrades.upgrade_0X references [upgrade}
                squad_veterancy_ext.veterancy_rank_info
                    veterancy_rank_(01-05)
                        experience_value
                        squad_actions.actions_0X references [action] most likely apply_modifiers_action
                            [modifiers_block]
        """
        abilities = self.get_abilities()
        actions = self.get_actions()
        loadout = self.get_loadout()
        squad_upgrade_apply = self.get_squad_upgrade_apply()
        squad_upgrade = self.get_squad_upgrade()
        veterancy = self.get_veterancy()

        result = {
            'reference': self.sbps_filename,
            'constname': self.constname,
            'faction': self.faction,
            'type': 'vehicle',
            'loadout': loadout,
            'veterancy': veterancy
        }
        if actions:
            result['actions'] = [action for action in actions]

        if abilities:
            result['abilities'] = abilities
        if squad_upgrade_apply:
            result['squad_upgrade_apply'] = squad_upgrade_apply
        if squad_upgrade:
            result['squad_upgrade'] = squad_upgrade

        return result


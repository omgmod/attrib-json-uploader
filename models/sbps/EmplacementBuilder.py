from models.sbps.Unit import Unit


class EmplacementBuilder(Unit):

    def __init__(self, constname, faction, filename, sbps_json):
        super().__init__(constname, faction, filename, sbps_json)

    def clean(self):
        """
            Parse the raw sbps_json dict into a condensed dictionary with only the values we need.

            Properties to look at:
                squad_loadout_ext.unit_list.unit_0X
                    type.type references [ebps]
                    num
                squad_veterancy_ext.veterancy_rank_info
                    veterancy_rank_(01-05)
                        experience_value
                        squad_actions.actions_0X references [action] most likely apply_modifiers_action
                            [modifiers_block]

        """
        loadout = self.get_loadout()
        veterancy = self.get_veterancy()
        return {
            'reference': self.sbps_filename,
            'constname': self.constname,
            'faction': self.faction,
            'loadout': loadout,
            'veterancy': veterancy
        }

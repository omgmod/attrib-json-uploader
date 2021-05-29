from models.ebps.Vehicle import Vehicle
from utils.StringUtils import StringUtils


class EmplacementBuilder(Vehicle):

    def __init__(self, raw_json, faction, filename):
        super().__init__(raw_json, faction, filename)

    def clean(self):
        """
            Properties:
                crush_ext.default_crush_mode

                engineer_ext.construction_menus.construction_menu_01.construction_type

                health_ext.hitpoints
                moving_ext
                population_ext - no personnel_pop, broken???
                sight_ext
                type_ext
                veterancy_ext
        """
        print(f"Processing [{self.ebps_filename}]")

        crush = self.get_crush()
        construction_type = self.get_construction_type()
        health = self.get_health()
        moving = self.get_moving()
        sight = self.get_sight()
        types = self.get_types()
        veterancy_value = self.get_veterancy_value()

        result = {
            'reference': self.ebps_filename,
            'faction': self.faction,
            'type': 'emplacement_builder',
            'construction_type': construction_type,
            'crush': crush,
            'moving': moving
        }
        result.update(health)
        result.update(sight)
        result.update(types)
        result.update(veterancy_value)
        return result

    def get_construction_type(self):
        return {
            'construction_type': StringUtils.remove_bracket_wrapping(self.raw_json['engineer_ext']['construction_menus']['construction_menu_01']['construction_type'])
        }

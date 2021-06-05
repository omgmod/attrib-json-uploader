from functools import partial

from models.AbstractModel import AbstractModel
from utils.DictUtils import DictUtils
from utils.StringUtils import StringUtils


class Weapon(AbstractModel):

    def __init__(self, raw_json, filename):
        weapon_bag_dict = raw_json['weapon_bag']

        super().__init__(weapon_bag_dict)
        self.filename = filename

    def clean(self):
        """
            Properties
                accuracy
                    [DLMS]
                aim
                    fire_aim_time
                        min/max
                    fire_aim_time_multiplier
                        [DLMS]
                    ready_aim_time
                        min/max
                    post_firing_aim_time
                    post_firing_cooldown
                area_effect
                    area_info.radius
                    has_friendly_fire
                    distance
                        [DLMS]
                    accuracy
                        [DLMS]
                    damage
                        [DLMS]
                    penetration
                        [DLMS]
                    suppression
                        [DLMS]
                    damage_friendly
                        [DLMS]
                    suppression_friendly
                        [DLMS]
                behaviour
                    aa_weapon
                    artillery_force_obey_los
                    attack_ground
                    attack_individual_entity
                    can_be_substituted
                    enable_auto_target_search
                    ignore_shot_blocking
                burst
                    can_burst
                    duration
                        min/max
                    incremental_target_table
                        accuracy_multiplier
                        search_radius
                            [DLMS]
                    rate_of_fire
                        min/max
                cooldown
                    duration
                        min/max
                    duration_multiplier
                        [DLMS]
                cover_table
                    tp_X references [type_cover]
                        accuracy_multiplier
                        damage_multiplier
                        suppression_multiplier
                        penetration_multiplier
                critical_table
                    tp_X references [type_target_critical]
                        critical_table_01
                            hit_0X
                                critical_type
                                    critical references [critical]

                                    reference paired with critical combo only
                                    critical_combo.reference references [critical_combo]
                                weight
                        critical_table_02
                        critical_table_03
                damage
                    min/max
                damage_over_time.reference
                deflection
                    deflection_damage_multiplier
                    has_deflection_damage
                fire
                    wind_up
                    wind_down
                flinch_radius
                moving
                    accuracy_multiplier
                    burst_multiplier
                    cooldown_multiplier
                    disable_moving_firing
                    moving_start_time
                    moving_end_time
                name [[ ]]
                penetration
                    [DLMS]
                projectile.projectile references [ebps\\projectile]
                range
                    min
                    max
                    mid
                        distant
                        long
                        medium
                        short
                reload
                    duration
                        min/max
                    duration_multiplier
                        [DLMS]
                    frequency
                        min/max
                scatter
                    angle_scatter
                    distance_scatter_max
                    distance_scatter_offset
                    distance_scatter_ratio
                    fow_angle_multiplier
                    fow_distance_multiplier
                setup.duration
                suppressed
                    pinned_burst_multiplier
                    pinned_cooldown_multiplier
                    pinned_reload_multiplier
                    suppressed_burst_multiplier
                    suppressed_cooldown_multiplier
                    suppressed_reload_multiplier
                suppression
                    suppression
                        [DLMS]
                    nearby_suppression_multiplier
                    nearby_suppression_radius
                    target_suppressed_multipliers
                        accuracy_multiplier
                        damage_multiplier
                        suppression_multiplier
                    target_pinned_multipliers
                        accuracy_multiplier
                        damage_multiplier
                        suppression_multiplier
                target_table
                    tp_X references [type_target_weapon]
                        accuracy_multiplier
                        moving_accuracy_multiplier
                        damage_multiplier
                        penetration_multiplier
                        rear_penetration_multiplier
                        suppression_multiplier
                        priority
                        disable_target
                        disable_auto_search
                tracking.normal
                    max_up
                    max_down
                    max_left
                    max_right
                    speed_horizontal
                    speed_vertical
        """
        print(f"Processing Weapon {self.filename}")
        accuracy = self.get_accuracy()
        aim = self.get_aim()
        area_effect = self.get_area_effect()
        behaviour = self.get_behaviour()
        burst = self.get_burst()
        cooldown = self.get_cooldown()
        cover_table = self.get_cover_table()
        critical_table = self.get_critical_table()
        damage = self.get_damage()
        damage_over_time = self.get_damage_over_time()
        deflection = self.get_deflection()
        fire = self.get_fire()
        moving = self.get_moving()
        penetration = self.get_penetration()
        projectile = self.get_projectile()
        range_values = self.get_range()
        reload = self.get_reload()
        scatter = self.get_scatter()
        setup_duration = self.get_setup_duration()
        suppressed = self.get_suppressed()
        suppression = self.get_suppression()
        target_table = self.get_target_table()
        tracking = self.get_tracking()

        result = {
            'reference': self.filename,
            'type': Weapon._get_weapon_type(self.filename),
            'accuracy': accuracy,
            'cover_table': cover_table,
            'critical_table': critical_table,
            'scatter': scatter,
            'target_table': target_table,
        }
        if area_effect:
            result['area_effect'] = area_effect
        if aim:
            result['aim'] = aim
        if behaviour:
            result['behaviour'] = behaviour
        if burst:
            result['burst'] = burst
        if cooldown:
            result['cooldown'] = cooldown
        if damage:
            result['damage'] = damage
        if deflection:
            result['deflection'] = deflection
        if fire:
            result['fire'] = fire
        if moving:
            result['moving'] = moving
        if penetration:
            result['penetration'] = penetration
        if range_values:
            result['range'] = range_values
        if reload:
            result['reload'] = reload
        if suppressed:
            result['suppressed'] = suppressed
        if suppression:
            result['suppression'] = suppression
        if tracking:
            result['tracking'] = tracking

        if 'name' in self.raw_json:
            result['name'] = StringUtils.remove_bracket_wrapping(self.raw_json['name'].replace('\"', 'inch'))

        result.update(damage_over_time)
        result.update(projectile)
        result.update(setup_duration)
        DictUtils.add_to_dict_if_in_source(self.raw_json, result, 'flinch_radius')

        return result

    @staticmethod
    def _get_weapon_type(reference):
        path_elements = reference.split('\\')
        subclass = path_elements[-2]
        return subclass

    @staticmethod
    def _get_dlms_dict(data):
        result = {}
        dlms_partial = partial(DictUtils.add_to_dict_if_in_source, data, result)
        dlms_partial('distant')
        dlms_partial('long')
        dlms_partial('medium')
        dlms_partial('short')
        return result

    @staticmethod
    def _get_min_max_dict(data):
        result = {}
        dlms_partial = partial(DictUtils.add_to_dict_if_in_source, data, result)
        dlms_partial('min')
        dlms_partial('max')
        return result

    @staticmethod
    def _add_to_dict_if_not_empty(target, key, data):
        if len(data) > 0:
            target[key] = data

    def get_accuracy(self):
        accuracy_dict = self.raw_json['accuracy']
        return Weapon._get_dlms_dict(accuracy_dict)

    def get_aim(self):
        try:
            aim_dict = self.raw_json['aim']
            fire_aim_time = Weapon._get_min_max_dict(aim_dict.get('fire_aim_time', {}))
            fire_aim_time_multiplier = Weapon._get_dlms_dict(aim_dict.get('fire_aim_time_multiplier', {}))
            ready_aim_time = Weapon._get_min_max_dict(aim_dict.get('ready_aim_time', {}))
            result = {}
            if len(fire_aim_time) > 0:
                result['fire_aim_time'] = fire_aim_time
            if len(fire_aim_time_multiplier) > 0:
                result['fire_aim_time_multiplier'] = fire_aim_time_multiplier
            if len(ready_aim_time) > 0:
                result['ready_aim_time'] = ready_aim_time
            if 'post_firing_aim_time' in aim_dict:
                result['post_firing_aim_time'] = aim_dict['post_firing_aim_time']
            if 'post_firing_cooldown_interval' in aim_dict:
                result['post_firing_cooldown_interval'] = aim_dict['post_firing_cooldown_interval']
            return result
        except KeyError:
            return None

    def get_area_effect(self):
        area_effect_dict = self.raw_json['area_effect']
        if 'area_info' not in area_effect_dict or 'radius' not in area_effect_dict['area_info']:  # If theres no radius why bother
            return None
        result = {}
        Weapon._add_to_dict_if_not_empty(result, 'distance', Weapon._get_dlms_dict(area_effect_dict.get('distance', {})))
        Weapon._add_to_dict_if_not_empty(result, 'accuracy', Weapon._get_dlms_dict(area_effect_dict.get('accuracy', {})))
        Weapon._add_to_dict_if_not_empty(result, 'damage', Weapon._get_dlms_dict(area_effect_dict.get('damage', {})))
        Weapon._add_to_dict_if_not_empty(result, 'penetration', Weapon._get_dlms_dict(area_effect_dict.get('penetration', {})))
        Weapon._add_to_dict_if_not_empty(result, 'suppression', Weapon._get_dlms_dict(area_effect_dict.get('suppression', {})))
        Weapon._add_to_dict_if_not_empty(result, 'damage_friendly', Weapon._get_dlms_dict(area_effect_dict.get('damage_friendly', {})))
        Weapon._add_to_dict_if_not_empty(result, 'suppression_friendly', Weapon._get_dlms_dict(area_effect_dict.get('suppression_friendly', {})))
        result['radius'] = area_effect_dict['area_info']['radius']
        DictUtils.add_to_dict_if_in_source(area_effect_dict, result, 'has_friendly_fire')
        return result

    def get_behaviour(self):
        try:
            behaviour_dict = self.raw_json['behaviour']
            result = {}
            add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, behaviour_dict, result)
            add_to_dict_partial('aa_weapon')
            add_to_dict_partial('artillery_force_obey_los')
            add_to_dict_partial('attack_ground')
            add_to_dict_partial('attack_individual_entity')
            add_to_dict_partial('can_be_substituted')
            add_to_dict_partial('enable_auto_target_search')
            add_to_dict_partial('ignore_shot_blocking')
            return result
        except KeyError:
            return None

    def get_burst(self):
        try:
            burst_dict = self.raw_json['burst']
            result = {}
            DictUtils.add_to_dict_if_in_source(burst_dict, result, 'can_burst')
            Weapon._add_to_dict_if_not_empty(result, 'duration', Weapon._get_min_max_dict(burst_dict.get('duration', {})))
            Weapon._add_to_dict_if_not_empty(result, 'rate_of_fire', Weapon._get_min_max_dict(burst_dict.get('rate_of_fire', {})))
            incremental_target_table_dict = burst_dict.get('incremental_target_table')
            if incremental_target_table_dict:
                DictUtils.add_to_dict_if_in_source(incremental_target_table_dict, result, 'accuracy_multiplier', 'incremental_accuracy_multiplier')
                Weapon._add_to_dict_if_not_empty(result, 'incremental_search_radius', Weapon._get_dlms_dict(incremental_target_table_dict.get('search_radius', {})))
            return result
        except KeyError:
            return None

    def get_cooldown(self):
        try:
            cooldown_dict = self.raw_json['cooldown']
            result = {}
            Weapon._add_to_dict_if_not_empty(result, 'duration', Weapon._get_min_max_dict(cooldown_dict.get('duration', {})))
            Weapon._add_to_dict_if_not_empty(result, 'duration_multiplier', Weapon._get_dlms_dict(cooldown_dict.get('duration_multiplier', {})))
            return result
        except KeyError:
            return None

    def get_cover_table(self):
        cover_table_dict = self.raw_json['cover_table']
        result = {}
        for key, value in cover_table_dict.items():
            cover_type_result = {}
            add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, value, cover_type_result)
            add_to_dict_partial('accuracy_multiplier')
            add_to_dict_partial('damage_multiplier')
            add_to_dict_partial('suppression_multiplier')
            add_to_dict_partial('penetration_multiplier')
            if len(cover_type_result) > 0:
                result[key] = cover_type_result
        return result

    def get_critical_table(self):
        critical_table_dict = self.raw_json['critical_table']
        result = {}
        # For each critical target type
        for critical_type, value in critical_table_dict.items():
            if 'tp_' not in critical_type:
                continue
            # "tp_armour": {
            #   "critical_table_01": {
            #     "hit_01": {"critical_type": {"critical": "[[critical\\_no_critical.lua]]"}, "weight": "85"}, 
            #     "hit_02": {
            #         "critical_type": {
            #           "reference": "[[critical_type\\critical_combo.lua]]", 
            #           "critical_combo": {
            #             "reference": "[[critical_combo\\vehicle_destroy_secondary_weapon.lua]]"}
            #           }, 
            #         "weight": "15"
            #      }
            #   },
            #   "critical_table_02": {
            #       "hit_01": {
            #                   "critical_type": {"reference": "[[critical_type\\critical_combo.lua]]",
            #                                     "critical_combo": {
            #                                         "reference": "[[critical_combo\\vehicle_destroy_secondary_weapon.lua]]"}},
            #                   "weight": "25"}, "hit_02": {"weight": "75"}}, 
            #   "critical_table_03": {
            #         "hit_01": {"critical_type": {"critical": "[[critical\\vehicle_make_wreck.lua]]"}, "weight": "25"},
            #         "hit_02": {"critical_type": {"critical": "[[critical\\vehicle_out_of_control_fast.lua]]"},
            #                    "weight": "25"},
            #         "hit_03": {"critical_type": {"critical": "[[critical\\vehicle_destroy_maingun.lua]]"},
            #                    "weight": "25"},
            #         "hit_04": {"critical_type": {"critical": "[[critical\\_no_critical.lua]]"}, "weight": "25"}}},
         
            # Each critical type has 3 critical tables, corresponding to green, yellow, red damage
            critical_type_result = {}
            for critical_table_num, critical_table_value in value.items():
                # Looking for hit_0X with critical_type and weight
                critical_table_result = {}  # weight to critical/critical_combo ref
                DictUtils.add_to_dict_if_in_source(critical_table_value, critical_table_result, 'damage_bound')
                for hit_num, hit_value in critical_table_value.items():
                    if 'critical_type' not in hit_value or 'weight' not in hit_value:
                        continue
                    hit_critical_type_dict = hit_value['critical_type']
                    weight = hit_value['weight']
                    if 'critical' in hit_critical_type_dict:
                        # simple critical
                        reference = StringUtils.remove_bracket_file_endings(hit_critical_type_dict['critical'])
                        critical_table_result[reference] = weight
                    elif 'critical_combo' in hit_critical_type_dict:
                        # critical_combo
                        reference = StringUtils.remove_bracket_file_endings(hit_critical_type_dict['critical_combo']['reference'])
                        critical_table_result[reference] = weight
                    elif 'critical_combo' in hit_critical_type_dict['reference']:
                        # If this is a critical combo reference but no 'critical_combo' is provided, the default critical_combo
                        # is critical_combo\_no_critical_combo.lua. Treat as no critical
                        reference = 'critical\\_no_critical'
                        critical_table_result[reference] = weight
                    else:
                        raise Exception(f"Malformed hit critical type dict, could not find critical or critical_combo {hit_critical_type_dict}")
                critical_type_result[critical_table_num] = critical_table_result
            result[critical_type] = critical_type_result
        return result

    def get_damage(self):
        try:
            damage_dict = self.raw_json['damage']
            return Weapon._get_min_max_dict(damage_dict)
        except KeyError:
            return None

    def get_damage_over_time(self):
        try:
            damage_over_time_dict = self.raw_json['damage_over_time']
            return {
                'damage_over_time': StringUtils.remove_bracket_wrapping(damage_over_time_dict['reference'])
            }
        except KeyError:
            return {}

    def get_deflection(self):
        try:
            deflection_dict = self.raw_json['deflection']
            result = {}
            add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, deflection_dict, result)
            add_to_dict_partial('deflection_damage_multiplier')
            add_to_dict_partial('has_deflection_damage')
            return result
        except KeyError:
            return None
    
    def get_fire(self):
        try:
            fire_dict = self.raw_json['fire']
            result = {}
            add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, fire_dict, result)
            add_to_dict_partial('wind_up')
            add_to_dict_partial('wind_down')
            return result
        except KeyError:
            return None
    
    def get_moving(self):
        try:
            moving_dict = self.raw_json['moving']
            result = {}
            add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, moving_dict, result)
            add_to_dict_partial('accuracy_multiplier')
            add_to_dict_partial('burst_multiplier')
            add_to_dict_partial('cooldown_multiplier')
            add_to_dict_partial('disable_moving_firing')
            add_to_dict_partial('moving_start_time')
            add_to_dict_partial('moving_end_time')
            return result
        except KeyError:
            return None

    def get_penetration(self):
        try:
            penetration_dict = self.raw_json['penetration']
            result = {}
            Weapon._add_to_dict_if_not_empty(result, 'penetration', Weapon._get_dlms_dict(penetration_dict))
            return result
        except KeyError:
            return None

    def get_projectile(self):
        try:
            projectile_dict = self.raw_json['projectile']
            return {
                'projectile': StringUtils.remove_bracket_file_endings(projectile_dict['projectile'])
            }
        except KeyError:
            return {}

    def get_range(self):
        try:
            range_dict = self.raw_json['range']
            result = {}
            DictUtils.add_to_dict_if_in_source(range_dict, result, 'min')
            DictUtils.add_to_dict_if_in_source(range_dict, result, 'max')
            result['mid'] = Weapon._get_dlms_dict(range_dict['mid'])
            return result
        except KeyError:
            return None

    def get_reload(self):
        try:
            reload_dict = self.raw_json['reload']
            result = {}
            Weapon._add_to_dict_if_not_empty(result, 'duration', Weapon._get_min_max_dict(reload_dict.get('duration', {})))
            Weapon._add_to_dict_if_not_empty(result, 'duration_multiplier', Weapon._get_dlms_dict(reload_dict.get('duration_multiplier', {})))
            Weapon._add_to_dict_if_not_empty(result, 'frequency', Weapon._get_min_max_dict(reload_dict.get('frequency', {})))
            return result
        except KeyError:
            return None

    def get_scatter(self):
        scatter_dict = self.raw_json['scatter']
        result = {}
        add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, scatter_dict, result)
        add_to_dict_partial('angle_scatter')
        add_to_dict_partial('distance_scatter_max')
        add_to_dict_partial('distance_scatter_offset')
        add_to_dict_partial('distance_scatter_ratio')
        add_to_dict_partial('fow_angle_multiplier')
        add_to_dict_partial('fow_distance_multiplier')
        return result

    def get_setup_duration(self):
        try:
            setup_dict = self.raw_json['setup']
            return {
                'setup_duration': StringUtils.remove_bracket_wrapping(setup_dict['duration'])
            }
        except KeyError:
            return {}

    def get_suppressed(self):
        try:
            suppressed_dict = self.raw_json['suppressed']
            result = {}
            add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, suppressed_dict, result)
            add_to_dict_partial('pinned_burst_multiplier')
            add_to_dict_partial('pinned_cooldown_multiplier')
            add_to_dict_partial('pinned_reload_multiplier')
            add_to_dict_partial('suppressed_burst_multiplier')
            add_to_dict_partial('suppressed_cooldown_multiplier')
            add_to_dict_partial('suppressed_reload_multiplier')
            return result
        except KeyError:
            return None

    def get_suppression(self):
        try:
            suppression_dict = self.raw_json['suppression']
            result = {}
            if 'suppression' not in suppression_dict:
                return None  # No suppression

            Weapon._add_to_dict_if_not_empty(result, 'suppression', Weapon._get_dlms_dict(suppression_dict.get('suppression', {})))

            add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, suppression_dict, result)
            add_to_dict_partial('nearby_suppression_multiplier')
            add_to_dict_partial('nearby_suppression_radius')

            for key in ('target_suppressed_multipliers', 'target_pinned_multipliers'):
                if key in suppression_dict:
                    target_multipliers = suppression_dict[key]
                    key_result = {}
                    add_to_target_dict_partial = partial(DictUtils.add_to_dict_if_in_source, target_multipliers, key_result)
                    add_to_target_dict_partial('accuracy_multiplier')
                    add_to_target_dict_partial('damage_multiplier')
                    add_to_target_dict_partial('suppression_multiplier')
                    result[key] = key_result

            return result
        except KeyError:
            return None

    def get_target_table(self):
        target_table_dict = self.raw_json['target_table']
        result = {}
        for key, value in target_table_dict.items():
            cover_type_result = {}
            add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, value, cover_type_result)
            add_to_dict_partial('accuracy_multiplier')
            add_to_dict_partial('moving_accuracy_multiplier')
            add_to_dict_partial('damage_multiplier')
            add_to_dict_partial('suppression_multiplier')
            add_to_dict_partial('penetration_multiplier')
            add_to_dict_partial('rear_penetration_multiplier')
            add_to_dict_partial('priority')
            add_to_dict_partial('disable_target')
            add_to_dict_partial('disable_auto_search')
            if len(cover_type_result) > 0:
                result[key] = cover_type_result
        return result

    def get_tracking(self):
        try:
            tracking_dict = self.raw_json['tracking']['normal']
            result = {}
            add_to_dict_partial = partial(DictUtils.add_to_dict_if_in_source, tracking_dict, result)
            add_to_dict_partial('max_up')
            add_to_dict_partial('max_down')
            add_to_dict_partial('max_left')
            add_to_dict_partial('max_right')
            add_to_dict_partial('speed_horizontal')
            add_to_dict_partial('speed_vertical')
            return result
        except KeyError:
            return None

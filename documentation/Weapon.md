## Weapon Stats rundown
Within a `weapon_bag`, there are the following:

*Time values are in seconds*

#### `accuracy`
Value between 0 and 1, 1 being 100% accurate, 0 being 0%.

* `distant`\
 Accuracy between the long to max range band. Many weapons do not use this and have a max range = long
 
* `long`\
 Medium to long band

* `medium`\
 Short to medium band

* `short`\
 Minimum range to short band

#### `ai_info`
Seems to be some sort of ai prioritization against targets, *unsure how this interacts with target table priorities.*
* `anti`
    * `aiclass_infantry`
    * `aiclass_light_vehicle`
    * `aiclass_medium_vehicle`
    * `aiclass_heavy_vehicle`
    * `aiclass_structure`

#### `aim`
How much time is required to aim the weapon, at different ranges.

* `fire_aim_time`\
Delay before each shot, excluding the first shot.
    * `min`
    * `max`

* `fire_aim_time_multiplier`\
Range based multiplier on fire_aim_time. Default value is 1.
    * `distant`
    * `long`
    * `medium`
    * `short`

* `ready_aim_time`\
Delay before the first shot at a specific target. Applies every time you change targets.
    * `min`
    * `max`
    
* `post_firing_aim_time`\
Duration that the weapon remains aimed after firing.

* `post_firing_cooldown`\
Delay after firing before the weapon can be aimed again.
    
#### `anim table`
Defines what animations to use.

#### `area_effect`
Describes area of effect characteristics around the weapon's impact.

* `area_info`
    * `radius`\
    Max radius of the AOE circle.
    
* `has_friendly_fire`\
Does the weapon do friendly fire. Default true, set to false for weapons like flamethrowers.

* `distance`
Sets the range bands used for other AoE stats, indicates how large the AoE circles are.
    * `distant`
    * `long`
    * `medium`
    * `short`
    
* `accuracy`
Multiplier on weapon accuracy at different ranges. Default values are 1
    * `distant`
    * `long`
    * `medium`
    * `short`    
* `damage`
Multiplier on weapon damage at different ranges. Default to 1.
    * `distant`
    * `long`
    * `medium`
    * `short`
* `penetration`
Multiplier on weapon penetration at different ranges. Default to 1.
    * `distant`
    * `long`
    * `medium`
    * `short`
* `suppression`
Multiplier on weapon suppression at different ranges. Default to 1.
    * `distant`
    * `long`
    * `medium`
    * `short`

* `damage_friendly`
Multiplier on weapon damage at different ranges against friendly targets. Default to 1.
    * `distant`
    * `long`
    * `medium`
    * `short`
* `suppression_friendly`
Multiplier on weapon suppression at different ranges against friendly targets. Default to 1.
    * `distant`
    * `long`
    * `medium`
    * `short`

#### `behaviour`
Flags that give the weapon special abilities.

* `aa_weapon`\
Can the weapon target air units?

* `artillery_force_obey_los`\
Is the weapon forced to shoot within line of sight (not into fog of war)? Used by flamethrowers.

* `attack_ground`\
Can the weapon attack ground?

* `attack_individual_entity`\
Can the weapon target a specific entity within a squad? Used by sniper rifles.

* `can_be_substituted`\
Can the weapon be substituted for a pickup/upgrade weapon.

* `enable_auto_target_search`\
Can the weapon find targets by itself. Default true, set to false for weapons that should only fire on command like artillery.

* `ignore_shot_blocking`\
Can the weapon ignore shot blockers? Typically grenades.

* `point_blank`\
Can the weapon fire at range 0?

* `prevents_prone`\
Does the weapon prevent the wielding model from going prone? Used by infantry AT and support weapons.

* `support_weapon`\
Is the weapon one that can be picked up? *(Not sure on this)*

`aa_weapon_shoot_through`\
`can_be_offhanded`\
`fire_at_building_combat_slot`\
`ground_hit_rate`\
`pick_best_position`\
`reset_rotation_on_teardown`\
`single_handed_weapon`\
`share_parent_anim`\
`splash_damage`\
`splash_damage_amount`\
`splash_damage_radius`\
`substitute_weapon`\
`surprises_idle`

What is splash damage and how is it different from AoE?\
```splash damage
is explosive? yes or no.\
-amount and radius indicates the damage caused by explosion, and 
how large the radius is in which the unit can receive damage.
```

#### `burst`
Number of bullets fired per burst = burst duration * rate of fire
* `can_burst`\
Can the weapon shoot several rounds rather than 1 at a time?

* `duration`\
How long the unit will shoot for in a burst
    * `min`
    * `max` 

* `incremental_target_table`\
Incremental targets refers to the bursting weapon firing at multiple models.

    * `accuracy_multiplier`\
    Modifies the weapon accuracy for the range band by this multiplier for every model the weapon is shooting at.\
    A value > 1 means the weapon is more accurate as it shoots at more models in its burst, and the inverse is also true.
    Default value is 1.
    
    * `search_radius`\
    Incremental accuracy only applies to targets within the weapon search radius. A larger radius is better.\
    If a weapon only has a short band search_radius, the rest are 0.
        * `distant`
        * `long`
        * `medium`
        * `short`
        
* `rate_of_fire`\
Bullets per second
    * `min`
    * `max` 
    
#### `cooldown`
* `duration`\
Time between bursts or rounds
    * `min`
    * `max`

* `duration_multiplier`\
Multiplier that increases or decreases the cooldown time for different ranges.
    * `distant`
    * `long`
    * `medium`
    * `short`

#### `cover_table`
Various multipliers applied when targeting units in cover. Each type of cover can have accuracy, damage, suppression, 
and penetration multipliers, which each use a default value of 1 if not specified.

* `tp_defcover`\
Default cover type
    * `accuracy_multiplier`
    * `damage_multiplier`
    * `suppression_multiplier`
    * `penetration_multiplier`
* `tp_light`\
Light (yellow) cover
* `tp_heavy`\
Heavy (green) cover
* `tp_negative`\
Negative (red) cover
* `tp_smoke`\
Smoke cover
* `tp_garrison_cover`\
Garrison cover
* `tp_garisson_halftrack`\
Halftrack cover
* `tp_trench`\
Trench cover
* `tp_water`\
Water cover
* `tp_z_bunker`\
Bunker cover
* `tp_z_emplacement`\
Emplacement cover
* `tp_open`\
Open cover. What is this?

#### `critical_table`
Contains weight and critical type information against different critical types. Death always requires an equivalent critical to occur. 
There are three critical tables per critical type, corresponding to `damage` type, and each can have 0 to 5 critical 
hits with a weight of likelihood. Weights should, but do not always, add up to 100. Critical hits with weight of 0 are ignored.

The different critical effects are specified in `critical`.
Critical types for units are specified by `type_target_critical` on entities.

Some weapons against certain critical types, typically armour or vehicle, can inflict combo criticals which essentially 
destroy the target's secondary weapon, typically a mounted gunner. This is a way of generically destroying 
mounted gunners as types like `tp_armour` are not unit or faction specific.

Damage bounds are specified in `damage` but in general are, for percentage of damage taken against total health:\
Green (`damage_green`): `0 - 0.6`\
Yellow (`damage_yellow`): `0.61 - 0.94`\
Red (`damage_red`): `0.95 - 1`

* `tp_armour`
    * `critical_table_01`
        * `hit_01`
            * `critical_type`
                * `reference`\
                Reference to `critical_combo.lua`, used for destroying vehicle gunners.
                * `critical`\
                The actual critical that occurs with this given critical hit
                * `critical_combo`\
                Used in conjunction with a reference to `critical_combo.lua`, used for destroying vehicle gunners.
            * `weight`\
            Likelihood of this critical hit happening among all critical hits of this damage table.
        * `hit_02`
        * `hit_03`
        * `hit_04`
        * `hit_05`
    * `critical_table_02`
    * `critical_table_03`
* `tp_armour_elite`
* `tp_armour_rear`
* `tp_bridge`
* `tp_building`
* `tp_building_emplacement`
* `tp_defenses`
* `tp_deftarget`
* `tp_flyer`
* `tp_goliath`
* `tp_infantry`
* `tp_infantry_flamethrower_death`
* `tp_infantry_heroic`
* `tp_infantry_villers_bocage`
* `tp_light_building`
* `tp_light_vehicle`
* `tp_mine`
* `tp_ooc_vehicle`
* `tp_panel_building`
* `tp_panel_building_hq`
* `tp_resource`
* `tp_sp_razorwire`
* `tp_supply_truck`
* `tp_vehicle`
* `tp_vehicle_halftrack`
* `tp_villers_bocage_tiger`
* `tp_weapon_crew`
* `tp_world_object`

#### `damage`
How much damage the weapon does per round or bullet, usually 2-15 for anti infantry (lower for fast firing, higher for slow firing), 70-100 for infantry AT, and 125-275 for tank guns depending on size.
* `min`
* `max`

#### `damage_over_time`
TODO LINK the reference to corresponding `dot_type`

* `reference`\
Reference to the `dot_type` object which describes the actual damge over time effects.

* `duration_min`\
*Not sure, sounds like a duration minimum override on the `dot_type` object's `duration_min`.*

#### `deflection`
Used when the weapon can still do damage without penetrating, usually for tank or vehicle damage.

* `deflection_damage_multiplier`\
Multiplier for how much of the weapon's damage will be applied on nonpenetrating hits. Typically 0.10 or 0.15

* `has_deflection_damage`\
Flag for whether the the weapon does deflection damage.

#### `fire`
Contains details for actions when the weapon is fired, as well as "winding", used mainly for rotating weapons. Default 
values are 0.

* `wind_up`\
Delay just before firing a shot or burst, usually associated with an animation.\
It can be combined with cooldown, but it is not affected by the cooldown multiplier. 

* `wind_down`\
Delay after a burst or rounds has been fired, usually associated with an animation.\
It can be combined with cooldown, but it is not affected by the cooldown multiplier. 

#### `flinch_radius`
Radius around the impact where units will respond to being fire upon.

#### `fx_action_target_name`
Effect on the target hit by the weapon

#### `fx_always_visible`
If true, the weapon effects are always visible, default false.

#### `fx_delay_in_building`
#### `fx_munition_name`
Name of the munition effect to use at the point of impact.

#### `fx_tracer_name`
Name of the tracer effect to use when this weapon is fired. If none, no tracer is used.

#### `fx_tracer_speed`
Speed of the tracer

#### `fx_use_building_panel_normal`

#### `help_text`
#### `icon_name`

#### `moving`
Modifiers applied when firing on the move.\

* `accuracy_multiplier`\
Modifies the standard accuracy when firing on the move. A value < 1 reduces accuracy when firing on the move.

* `burst_multiplier`\
Modifies the standard burst duration when firing on the move. A value > 1 increases burst length when firing on the move.

* `cooldown_multiplier`\
Modifies the standard cooldown when firing on the move. A value > 1 increases cooldown when firing on the move.

* `disable_moving_firing`\
Flag for whether firing on the move is disabled.

* `moving_start_time`\
How long the unit has to be moving before moving multipliers take effect. Used by crewed AT and arty.

* `moving_end_time`\
How long the unit has to be stationary before moving multipliers stop applying.

#### `name`
Weapon name

#### `offhand`
* `offhand_start_time`
* `offhand_end_time`

Unsure.\
```needs to be timed with any abilities, so that the weapon moves to offhand and back in time with the grenade toss, etc.```

#### `penetration`
The base chance to penetrate and do full damage, before modification by target type. A value of 1 means a 100% chance.
    * `distant`
    * `long`
    * `medium`
    * `short`

#### `priority`
Determines how the unit will choose targets based on where the other targets are. See target tables.

#### `projectile`
Determines the type of projectile entity fired from the weapon. Not used for small arms.

* `projectile`\
Reference to the projectile ebps.

#### `range`
Determines min, max, and "mid" ranges. These values set the range for accuracy, cooldown, and other multipliers. 
A distant range will receive distant multipliers between long and distant, long multipliers between long and medium, and so on.

* `min`\
Optional minimum range

* `max`\
Maximum range, is often equal to `long` range which makes `distant` unused

* `mid`\
Container for the intermediate range bands
    * `distant`
    Limit of the long to distant band. Not used if `max` == `long`
    * `long`
    Limit of the medium to long band
    * `medium`
    Limit of the short to medium band
    * `short`
    Limit of the minimum range to short band. If minimum range is not provided, starts at 0

#### `reload`
* `duration`\
Reload duration at the end of a firing cycle, can be a range if `min` != `max`
    * `min`
    * `max`

* `duration_multiplier`\
Optional multipler that increases or decreases the reload time for different ranges. If not provided, value is 1.
    * `distant`
    * `long`
    * `medium`
    * `short`

* `frequency`
How many bursts or rounds can be fired before starting a reload cycle.\
Burst weapons fire 1 more burst than the reload frequency.
    * `min`
    * `max`

#### `scatter`
Characteristics determining what happens to the weapon's projectile if it misses its target.

* `angle_scatter`\
Degree of scatter, the high the more likely the random scatter will hit somewhere other than the target.

* `distance_scatter_max`\
Max scatter distance around the intended target.

* `distance_scatter_offset`\
Determines whether the scatter will tend to land on the near or far side of the intended target. Between -1 and 1, 
values < 0 will tend to scatter closer to the firer, while values > 0 will tend to scatter on the far side of the target.
Most weapons have offsets > 0.

* `distance_scatter_ratio`\
How often the weapon will scatter away from the intended target. A value of 0 means it will never scatter away from the 
intended target, while a value of 1 means it will always scatter.

* `fow_angle_multiplier`\
Multiplier on scatter angle when firing into the fog of war.

* `fow_distance_multiplier`\
Multiplier on scatter distance when firing into the fog of war. Is this on every `distance_scatter_x` variable?

* `distance_scatter_obj_hit_min`
* `tilt_max_distance`\
*Unknown*

#### `setup`
Denotes when units need to be stationary for a duration before the weapon is ready to aim.

* `duration`\
Time required to set up the weapon before it can be fired.

* `has_instant_setup`\
What is this?

#### `suppressed`
Modifiers, typically penalties, imposed on the weapon when the wielder is suppressed or pinned.

* `pinned_burst_multiplier`\
Burst duration modifier when the wielder is pinned

* `pinned_cooldown_multiplier`\
Cooldown duration modifier when the wielder is pinned

* `pinned_reload_multiplier`\
Reload duration modifier when the wielder is pinned

* `suppressed_burst_multiplier`\
Burst duration modifier when the wielder is suppressed

* `suppressed_cooldown_multiplier`\
Cooldown duration modifier when the wielder is suppressed

* `suppressed_reload_multiplier`\
Reload duration modifier when the wielder is suppressed


#### `suppression`
Suppression characteristics the weapon inflicts.

When a squad receives suppression, they change state from normal to suppressed to pinned, with every step reducing the unit's combat effectiveness.
A squad becomes suppressed or pinned when the amount of suppression received reaches the squad's suppressed or pinned threshold,
and suppression must fall below the squad's suppressed or pinned recover threshold before they revert to the previous state.

The amount of suppression necessary to activate the suppressed or pinned state is always greater than the amount of suppression needed to
recover from the corresponding state. Ex, Riflemen become suppressed at 0.2 suppression, but need their suppression to fall under 0.15 to
recover to normal.  

* `suppression`\
Raw suppression values by range. This is always added to the squad taking fire, regardless of range, per bullet.\
Can be reduced by cover, veterancy, or abilities.
    * `distant`
    * `long`
    * `medium`
    * `short`
    
* `nearby_suppression_multiplier`\
Multiplier on suppression dealt to units around the targeted unit.

* `nearby_suppression_radius`\
Radius around the targeted unit of the suppression area of effect.

* `target_suppressed_multipliers`\
Multipliers applied to targets suppressed by this weapon.
    * `accuracy_multiplier`
    * `damage_multiplier`
    * `suppression_multiplier`

* `target_pinned_multipliers`
Multipliers applied to targets pinned by this weapon.
    * `accuracy_multiplier`
    * `damage_multiplier`
    * `suppression_multiplier`

#### `target_table`
Multipliers for the weapon when fired against different target types. Also determines the priority of each target type.
Default value for a multiplier is 1.

Target types are specified in `type_target_weapon` on entities.

* `tp_armour_allies_m10_td`
    * `accuracy_multiplier`
    * `moving_accuracy_multiplier`
    * `damage_multiplier`
    * `penetration_multiplier`
    * `rear_penetration_multiplier`
    * `suppression_multiplier`
    * `priority`
    * `disable_target`\
    Is the weapon unable to fire at this target type in any way?
    * `disable_auto_search`\
    Is the weapon unable to fire at this target type automatically? If true, can still be manually targeted unless `disable_target` is also true. 
* `tp_armour_allies_sherman`
* `tp_armour_axis_motorcycle`
* `tp_armour_axis_ostwind`
* `tp_armour_axis_panther`
* `tp_armour_axis_panther_skirts`
* `tp_armour_axis_panzeriv`
* `tp_armour_axis_panzeriv_skirts`
* `tp_armour_axis_stug`
* `tp_armour_axis_stug_skirts`
* `tp_armour_axis_tiger`
* `tp_armour_cw_churchill`
* `tp_armour_cw_cromwell`
* `tp_armour_cw_priest`
* `tp_armour_cw_stuart`
* `tp_armour_m26_pershing`
* `tp_armour_marderiii`
* `tp_armour_pe_hetzer`
* `tp_armour_pe_hummel`
* `tp_armour_pe_jagdpanther`
* `tp_base_perimeter`
* `tp_boulder`
* `tp_bridge`
* `tp_building`
* `tp_building_allies_checkpoint`
* `tp_building_axis_bunker_lite`
* `tp_building_bunker_emplacement`
* `tp_building_destructible`
* `tp_building_resource`
* `tp_building_under_construction`
* `tp_cw_emplacements`
* `tp_cw_hqs_emplaced`
* `tp_cw_hqs_mobile`
* `tp_defenses`
* `tp_defenses_under_construction`
* `tp_deftarget`
* `tp_flamethrower_proof`
* `tp_infantry`
* `tp_infantry_airborne`
* `tp_infantry_airborne_inflight`
* `tp_infantry_heroic`
* `tp_infantry_riflemen_elite`
* `tp_infantry_sniper`
* `tp_infantry_soldier`
* `tp_infantry_sp_m01`
* `tp_infantry_surrender`
* `tp_invincible`
* `tp_invincible_no_target`
* `tp_mine`
* `tp_mine_airdrop`
* `tp_object_detector_radio`
* `tp_object_metal_stone`
* `tp_object_wood`
* `tp_p47_thunderbolt`
* `tp_slit_trench`
* `tp_sp_m06_bunker_destructible`
* `tp_team_weapon`
* `tp_vehicle`
* `tp_vehicle_allies_105mm_howitzer`
* `tp_vehicle_allies_57mm_towed_gun`
* `tp_vehicle_allies_jeep`
* `tp_vehicle_allies_m3_halftrack`
* `tp_vehicle_allies_m8_greyhound`
* `tp_vehicle_axis_88mm`
* `tp_vehicle_axis_sdkfz_234_heavy_armoured_car`
* `tp_vehicle_axis_sdkfz_251_halftrack`
* `tp_vehicle_sdkfz_22x_light_armoured_car`
* `tp_vehicle_sdkfz_22x_light_armoured_car_improved`
* `tp_vehicle_civilian`
* `tp_vehicle_universal_carrier`

#### `tracking`
Weapon firing cone and traverse arc and speed characteristics.

* `fire_cone_angle`
Unsure, maybe related to possible trajectories the projectile can from straight ahead. 

* `normal`
    * `max_up`\
    Maximum amount the weapon can traverse up.
    
    * `max_down`\
    Maximum amount the weapon can traverse down.
    
    * `max_left`\
    Maximum amount the weapon can traverse left before the unit needs to turn or reposition.
    
    * `max_right`\
    Maximum amount the weapon can traverse right before the unit needs to turn or reposition.
    
    * `speed_horizontal`\
    Horizontal traverse speed. Important for tanks and crewed weapons
    
    * `speed_vertical`\
    Vertical traverse speed

---
Sources:\
[cohstats](http://hq-coh.com/stats/coh-stats.com/Info_Weapon_Statistics.html)\
[relicnews](https://web.archive.org/web/20140916064941/http://forums.relicnews.com/showthread.php?232509-How-To-Edit-Weapon-Stats-*finished*)

---
#### Copy pasted notes on DPS:
damage is reload freq * burst duration * rof * acc * damage, basically total bullet \* acc \* damage

time is reload freq * burst duration + (reload freq - 1) * cooldown + reload

dps = damage/time , this is for auto for semis/single you only need cooldown

ready aim time only applies after models select a target or re target after their target dies.

Wind up and down affects singles after each shot (maybe also for semis) for autos it happens after every reload cycle.

https://community.companyofheroes.com/discussion/231279/a-guide-to-d-p-s-basics

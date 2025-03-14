import math

def apply_attack_boost(raw, bonus_raw, ab_level):
    # raw: raw attack value
    # bonus_raw: bonus raw attack value (food, powercharm, etc.)
    # ab_level: attack boost level
    if ab_level == 1:
        total_raw = raw + 3
    elif ab_level == 2:
        total_raw = raw + 5
    elif ab_level == 3:
        total_raw = raw + 7
    elif ab_level == 4:
        total_raw = raw*1.02 + 8
    elif ab_level >= 5:
        total_raw = raw*1.04 + 9
    else:
        total_raw = raw
    total_raw = total_raw + bonus_raw
    return total_raw


def apply_critical_boost(crit_boost_level):
    # crit_boost_level: critical boost level
    crit_mod = 1.25 + (crit_boost_level * 0.03)
    crit_mod = min(crit_mod, 1.4) # Keeps value below 1.4 (max CB buff)
    crit_mod = max(crit_mod, 1.25) # Keeps value above 1.25 (min crit modifier)
    return crit_mod

def calc_effective_crit_mod(crit_mod, affinity):
    # applies affinity chance to crit proc
    # prop_of_crit = % of chance to proc a crit
    # prop_of_norm = % of chance of a normal hit
    prop_of_crit = affinity / 100
    prop_of_norm = 1 - prop_of_crit
    crit_dmg = prop_of_crit * crit_mod
    norm_dmg = prop_of_norm * 1
    effective_crit_mod = crit_dmg + norm_dmg
    return effective_crit_mod

def calc_total_dmg(raw, bonus_raw, affinity, ab_level, cb_level):
    # MH adds 0.1 to any damage value and then rounds it down, pushing 0.9 values up
    total_raw = apply_attack_boost(raw, bonus_raw, ab_level)
    crit_mod = apply_critical_boost(cb_level)
    effective_crit_mod = calc_effective_crit_mod(crit_mod, affinity) # Returns the effective modifier taking affinity in consideration
    total_dmg = (total_raw * effective_crit_mod) + 0.1
    return math.floor(total_dmg) # Needed to round down after 0.1 round up

def dmg_comparator(raw, bonus_raw, affinity, ab_level_a, cb_level_a, ab_level_b, cb_level_b):
    damage_a = calc_total_dmg(raw, bonus_raw, affinity, ab_level_a, cb_level_a)
    damage_b = calc_total_dmg(raw, bonus_raw, affinity, ab_level_b, cb_level_b)
    damage_diff = round((damage_a - damage_b) / damage_a, 2) # Provides difference between damages in a percentile, rounded up with 2 decimals
    comparator = damage_a, damage_b, damage_diff
    return comparator

# If you want to test it yourself just replace the 'Comparison' numbers in the constructor below, ignore the rest
# raw = weapon raw damage (without the bloat values, you dog)
# bonus_raw = extra raw dmg from food, charms etc.
# affinity = your weapon affinity (yes, it can be negative, although not optimal)
# ab_level_a and b = Attack Boost level
# cb_level_a and b = Critical Boost level

if __name__ == "__main__":
    print(f'Total Raw Damage: {apply_attack_boost(100, 5, 0)}')
    print(f'Critical Modifier: {apply_critical_boost(0)}')
    print(f'Effective crit modifier: {calc_effective_crit_mod(1.25, 0)}')
    print(f'Total dmg: {calc_total_dmg(100, 3, 20, 5, 3)}')
    print(f'Comparison: {dmg_comparator(raw = 100,
                                        bonus_raw = 3,
                                        affinity = 20,
                                        ab_level_a = 5,
                                        cb_level_a = 3,
                                        ab_level_b = 3,
                                        cb_level_b = 5
                                        )}')

import math

import calc


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
    # min keeps value below 1.4
    # max keeps value above 1.25
    crit_mod = 1.25 + (crit_boost_level * 0.03)
    crit_mod = min(crit_mod, 1.4)
    crit_mod = max(crit_mod, 1.25)
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
    effective_crit_mod = calc_effective_crit_mod(crit_mod, affinity)
    total_dmg = (total_raw * effective_crit_mod) + 0.1
    return math.floor(total_dmg)

if __name__ == "__main__":
    print(f'Total Raw Damage: {apply_attack_boost(100, 5, 5)}')
    print(f'Critical Modifier: {apply_critical_boost(5)}')
    print(f'Effective crit modifier: {calc_effective_crit_mod(1.25, 0)}')
    print(f'Total dmg: {calc_total_dmg(100, 3, 100, 5, 0)}')
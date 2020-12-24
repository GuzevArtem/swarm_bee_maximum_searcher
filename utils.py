import random

def check_extents(min_extent, max_extent):
    if len(min_extent) != len(max_extent):
        raise ValueError ('Extents should have equal dimensions size. Size min: ' + str(len(min_extent)) + ' != size max: ' + str(len(max_extent)))
 
    if len(min_extent) == 0 or len(max_extent) == 0:
        raise ValueError ('Extents should have dimensions bigger then 0.')

    for min, max in zip(min_extent, max_extent):
        if min > max:
            raise ValueError ('Value min should be less or equal to value max: ' + str(min) + ' should be less or equal to ' + str(max))

def check_is_greater(value, lower_extent, error_str = 'Value should be greater then {}, but was: {}'):
    if value <= lower_extent:
        raise ValueError (error_str.format(lower_extent, value))

def lerp(alpha, min_extent, max_extent):
    #check_extents(min_extent, max_extent)
    val = []
    for min, max in zip(min_extent, max_extent):
        val.append(alpha*(max-min)+min)
    return val

def get_rand_value_in_range(min_extent, max_extent):
    #check_extents(min_extent, max_extent)
    val = []
    for min, max in zip(min_extent, max_extent):
        val.append(random.random()*(max-min)+min)
    return val

def length(min_extent, max_extent):
    val = 0.0
    for min, max in zip(min_extent, max_extent):
        val += (max-min)**2
    return val



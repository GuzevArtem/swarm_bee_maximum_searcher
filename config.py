import utils

min_extent = [-100, -100]
max_extent = [100, 100]
scouts = 10
best_zones_bees = 15
selected_zones_bees = 5
best_zones_count = 2
selected_zones_count = 3
zone_size = 10
max_iterations = 5000
max_iterations_stale = 100
zone_shrink_factor = 100 # 2 / (factor ** 2) == percents of size left for each dimension of coordinates

def function(x, coefs = [-2, -2, -2], powers = [2, 2]): #function
    res = 0.0 if len(coefs) < 1 else coefs[0]
    i = 0
    for val in x:
        partial = 0.0
        
        if i < len(coefs)-1:
            partial += coefs[i+1]* (val ** (1 if i >= len(powers) else powers[i]) )
        else:
            partial += val

        res += partial
        i+=1
    return res

#checking configuration values input
utils.check_extents(min_extent, max_extent)
utils.check_is_greater(scouts, 0)
utils.check_is_greater(best_zones_bees, 0)
utils.check_is_greater(selected_zones_bees, 0)
utils.check_is_greater(best_zones_count, 0)
utils.check_is_greater(selected_zones_count, 0)
utils.check_is_greater(zone_size, 0)
utils.check_is_greater(max_iterations, 1)
utils.check_is_greater(max_iterations_stale, 1)
utils.check_is_greater(zone_shrink_factor, 1)

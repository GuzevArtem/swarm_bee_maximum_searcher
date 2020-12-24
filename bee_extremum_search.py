import config
import model
import utils
import statistic

class BeeFinder:
    """ Search function maximum using bee algorithm, assuming maximum value is single """

    def __init__(self, function):
        self.best_value = None
        self.best_value_pos = None
        self.function = function
        self.scout_bees = []
        self.worker_bees = []
        self.best_zones = []
        self.selected_zones = []
        self.iteration = 0
        self.stale_iteration = 0

    def spawn_scout_bees(self, count, min_extent, max_extent):
        """ creates batch of bees with function value in given extents """
        new_bees = []
        for i in range(count):
            pos = utils.get_rand_value_in_range(min_extent, max_extent)
            value = self.function(pos)
            bee = model.Bee(pos, value)
            new_bees.append(bee)
        self.scout_bees += new_bees

    def spawn_worker_bees_in_zone(self, zone, count):
        """ creates batch of bees with function value in given zone and updates best_bee in zone if possible """
        self.worker_bees = self.worker_bees + zone.spawn_workers(count, self.function)
        return zone.best_bee

    def create_zone_around_bee(self, bee, size, min_extent, max_extent):
        """ creates zone of given size around provided bee, but not bigger then provided extents """
        spawn_zone_min = [min(x-size, min_x) for x, min_x in zip(bee.pos, min_extent)]
        spawn_zone_max = [max(x+size, max_x) for x, max_x in zip(bee.pos, max_extent)]
        return model.Zone(spawn_zone_min, spawn_zone_max, bee)

    def spawn_worker_bees_around_scout_bee(self, bee, count, size, min_extent, max_extent):
        """ creates zone of given size around provided bee, but not bigger then provided extents
       and creates batch of bees with function value in given zone and updates best_bee in zone if possible """
        zone = self.create_zone_around_bee(bee, size, min_extent, max_extent)
        return self.spawn_worker_bees_in_zone(zone, count)

    def select_zones(self, zones, count_best, count_candidates):
        """ sorts zones and pick first count_best of them as best, next count_candidates as selected and updates global best"""
        sorted_zones = sorted(zones, reverse = True, key=lambda zone: zone.best_bee.value)
        best_zones = []
        selected_zones = []
        for i in range(config.best_zones_count):
            best_zones.append(sorted_zones[i])
        for i in range(config.best_zones_count, config.best_zones_count + config.selected_zones_count):
            selected_zones.append(sorted_zones[i])

        self.best_zones = best_zones
        self.selected_zones = selected_zones

        #update global best
        if self.best_value < best_zones[0].best_bee.value:
            self.best_value = best_zones[0].best_bee.value
            self.best_value_pos = best_zones[0].best_bee.pos

        return best_zones, selected_zones

    def init(self):
        """ initialized scout bees and prepares zones """
        self.spawn_scout_bees(config.scouts, config.min_extent, config.max_extent)

        # initialize best_value
        for bee in self.scout_bees:
            if self.best_value is None or self.best_value < bee.value:
                self.best_value = bee.value
                self.best_value_pos = bee.pos

        zones = [self.create_zone_around_bee(bee, config.zone_size, config.min_extent, config.max_extent) for bee in self.scout_bees ]
        # initialize zones
        self.select_zones(zones, config.best_zones_count, config.selected_zones_count)

    def iterate(self):
        """ single algorithm iteration, return False if stop criteria reached """
        #reset values
        self.scout_bees = []
        self.worker_bees = []

        created_zones = 0

        for zone in self.best_zones:
            self.spawn_worker_bees_in_zone(zone, config.best_zones_bees)
            statistic.history.get('zone_size')[created_zones].append(utils.length(zone.min, zone.max))
            #update zone
            if zone.best_bee.pos == zone.bees[0].pos:
                zone.shrink(config.zone_shrink_factor)
            else:
                zone.move(zone.best_bee.pos)
            #prepare for next iteration
            zone.shrink(config.zone_shrink_factor)
            zone.recall_bees()
            created_zones += 1

        for zone in self.selected_zones:
            self.spawn_worker_bees_in_zone(zone, config.selected_zones_count)
            statistic.history.get('zone_size')[created_zones].append(utils.length(zone.min, zone.max))
            #update zone
            if zone.best_bee.pos == zone.bees[0].pos:
                zone.shrink(config.zone_shrink_factor)
            else:
                zone.move(zone.best_bee.pos)
            #prepare for next iteration
            zone.recall_bees()
            created_zones += 1

        self.spawn_scout_bees(config.scouts - created_zones, config.min_extent, config.max_extent)

        all_zones = self.best_zones + self.selected_zones

        #create new search zones
        for bee in self.scout_bees:
            zone = self.create_zone_around_bee(bee, config.zone_size, config.min_extent, config.max_extent)
            all_zones.append(zone)

        #update global max
        prev_max_pos = self.best_value_pos
        self.select_zones(all_zones, config.best_zones_count, config.selected_zones_count)
        
        if prev_max_pos == self.best_value_pos:
            self.stale_iteration += 1
        else:
            self.stale_iteration = 0

        #statistics
        statistic.history.get('max_value').append(self.best_value)

        average_value = 0.0
        for zone in all_zones:
            average_value += zone.best_bee.value
        average_value /= len(all_zones)
        statistic.history.get('avarage_value').append(average_value)

        #update iteration
        solver.iteration += 1

        #stop criteria
        if self.iteration >= config.max_iterations or self.stale_iteration >= config.max_iterations_stale:
            return False

        return True


import matplotlib.pyplot as plt

#main
solver = BeeFinder(lambda x: config.function(x))
solver.init()
while solver.iterate():
    print("Iteration:", solver.iteration, "with value:", solver.best_value, "at:", solver.best_value_pos)
    pass
print("Total iteration passed:", solver.iteration )
print("best value:", solver.best_value, "at:", solver.best_value_pos)

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('Bee statistics')
ax1.plot(statistic.history['max_value'], '.-')
ax1.set_ylabel('maximum value ever')
ax2.plot(statistic.history['avarage_value'], '.-')
ax2.set_xlabel('iteration')
ax2.set_ylabel('Average value')

fig, axes = plt.subplots(config.best_zones_count, 1)
fig.suptitle('Best zones size statistics')
for i in range(config.best_zones_count):
    axes[i].plot(statistic.history['zone_size'][i], '.-')
    axes[i].set_ylabel('zone size')
axes[i].set_xlabel('iteration')

fig, axes = plt.subplots(config.selected_zones_count, 1)
fig.suptitle('Selected zones size statistics')
for i in range(config.selected_zones_count):
    axes[i].plot(statistic.history['zone_size'][config.best_zones_count + i], '.-')
    axes[i].set_ylabel('zone size')
axes[i].set_xlabel('iteration')

plt.show()

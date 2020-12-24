import utils

class Bee:
    def __init__(self, pos, value):
        self.pos = pos
        self.value = value


class Zone:
    def __init__(self, min, max, best_bee):
        self.min = min
        self.max = max
        self.bees = [best_bee]
        self.best_bee = best_bee

    def spawn_workers(self, count, function):
        for i in range(count):
            pos = utils.get_rand_value_in_range(self.min, self.max)
            val = function(pos)
            bee = Bee(pos, val)
            if val > self.best_bee.value:
                self.best_bee = bee
            self.bees.append(bee)
        return self.bees

    def recall_bees(self):
        self.bees = [self.bees[0]] #left scout

    def shrink(self, factor = 2):
        alpha = 1.0/(2*factor);
        self.min = utils.lerp(alpha, self.min, self.max)
        self.max = utils.lerp(1.0 - alpha, self.min, self.max)

    def move(self, new_center_pos):
        old_center = [ min_x + (max_x-min_x)/2 for min_x, max_x in zip(self.min, self.max)]
        offset = [ new_x - old_x for new_x, old_x in zip(new_center_pos, old_center)]

        self.min = [max(min_x+x, min_x) for x, min_x in zip(offset, self.min)]
        self.max = [min(max_x+x, max_x) for x, max_x in zip(offset, self.max)]

        self.bees = [ self.best_bee ] #worker is a new scout now

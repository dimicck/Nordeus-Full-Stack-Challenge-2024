class Island:
    island_counter = 0
    islands = {}

    def mark_field(self, field):
        # field = [height, island_id]
        field.island_id = self.id
        self.height_sum += field.height
        self.field_count += 1

    def __init__(self):
        Island.island_counter += 1
        self.id = Island.island_counter
        self.height_sum = 0
        self.field_count = 0
        self.islands[self.id] = self

    def average_height(self):
        return self.height_sum / self.field_count

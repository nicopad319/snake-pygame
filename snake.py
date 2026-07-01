from constants import WIDTH, HEIGHT

class Snake:
    def __init__(self):
        self.segments = [(WIDTH // 4, HEIGHT // 2)] #snake begins on left side of grid
    
    def move(self, direction):
        head_x, head_y = self.segments[0]
        if direction == 'w':
            new_head = (head_x, head_y - 1)
        elif direction == 's':
            new_head = (head_x, head_y + 1)
        elif direction == 'a':
            new_head = (head_x - 1, head_y)
        elif direction == 'd':
            new_head = (head_x + 1, head_y)
        else: 
            return  # Invalid direction, do nothing
        self.segments.insert(0, new_head)  # add new head to the front
        self.segments.pop()  # remove the last segment to simulate movement

    def grow(self):
        tail = self.segments[-1]
        self.segments.append(tail)  # Add a new segment at the tail position

    def get_length(self):
        return len(self.segments)
    
    def head_position(self):
        return self.segments[0]
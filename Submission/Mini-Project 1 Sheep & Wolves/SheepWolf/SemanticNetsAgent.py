import copy


class SemanticNetsAgent:

    def __init__(self):
        """
        This is the constructor method, which initializes the object.
        It sets the number of sheep and wolves on both sides of the river and keeps track of which side the agent is on.
        """
        self.ls = self.lw = self.rs = self.rw = 0  # Sheep and Wolves on Left and Right
        self.boat_side = 0  # 0: Left, 1: Right
        self.moves = []
        self.prior_state = None

    def __eq__(self, other):
        """ Check state equality, Overriding __eq__ is to compare states in the BFS algorithm.
        It's necessary to check if two states are the same based on the number of sheep and wolves on
        each side of the river and which side the boat is on """
        return all(getattr(self, attr) == getattr(other, attr) for attr in ['ls', 'lw', 'rs', 'rw', 'boat_side'])

    def __hash__(self):
        """Combine with __eq__ to ensure that two states are considered the same.
        Therefore, BFS will not revisit states that it has already seen"""
        return hash((self.ls, self.lw, self.boat_side, self.rs, self.rw))

    def is_valid_state(self):
        """ Check the current state for validity. """
        if any(x < 0 for x in [self.ls, self.lw, self.rs, self.rw]):
            return False
        if (self.ls and self.ls < self.lw) or (self.rs and self.rs < self.rw):
            return False
        return True

    def is_goal_state(self):
        """ Check for the goal state, goal state means sheep and wolf are transferred from left to right and the
        boat is on right side."""
        return self.boat_side == 1 and self.ls == self.lw == 0

    def move_animals(self, num_of_sheep, num_of_wolf, direction):
        """
        Move the animals from one side to the other.
        Direction +1: left --> right
        Direction -1: right --> left.
        """
        self.ls += direction * -num_of_sheep
        self.lw += direction * -num_of_wolf
        self.rs += direction * num_of_sheep
        self.rw += direction * num_of_wolf

    def generate_next_states(self):
        """
        Generate possible next states from the current state.
        """
        next_states = []

        for num_of_sheep in range(3):
            for num_of_wolf in range(max(0, 1 - num_of_sheep), 3 - num_of_sheep):
                next_state = copy.deepcopy(self)
                next_state.prior_state = self
                next_state.boat_side ^= 1

                direction = 1 if self.boat_side == 0 else -1  # Set direction based on the boat side
                next_state.move_animals(num_of_sheep, num_of_wolf, direction)  # Move animals

                if next_state.is_valid_state():
                    next_state.moves.append((num_of_sheep, num_of_wolf))
                    next_states.append(next_state)
        return next_states

    # referred bfs from geeksforgeeks https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
    def breadth_first_search(self):
        """
        Perform Breadth-First Search to find the shortest path to a goal state
        """
        if self.is_goal_state():
            return self
        # use a set to keep track of states that have already examined. The set avoid re-visiting
        visited = set()
        queue = [self]
        while queue:
            current_state = queue.pop(0)  # changes to .pop() will change the search algorithm from BFS to DFS,
            if current_state.is_goal_state():
                return current_state
            visited.add(current_state)
            for next_state in current_state.generate_next_states():
                if next_state not in visited and next_state not in queue:
                    queue.append(next_state)
        return None

    def solve(self, initial_sheep, initial_wolves):
        # Add your code here! Your solve method should receive
        # the initial number of sheep and wolves as integers,
        # and return a list of 2-tuples that represent the moves
        # required to get all sheep and wolves from the left
        # side of the river to the right.
        #
        # If it is impossible to move the animals over according
        # to the rules of the problem, return an empty list of
        # moves.
        """
        Solve the river crossing problem using BFS and return a list of moves.
        :param initial_sheep: Initial number of sheep on the left side.
        :param initial_wolves: Initial number of wolves on the left side.
        :return: List of 2-tuples representing the moves to get all animals to the right, or empty list if not possible.
        """
        self.ls, self.lw = initial_sheep, initial_wolves
        if not self.is_valid_state():
            return []

        goal_state = self.breadth_first_search()
        if not goal_state:
            return []
        return goal_state.moves


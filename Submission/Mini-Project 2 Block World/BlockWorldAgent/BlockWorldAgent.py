import copy


class BlockWorldAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    @staticmethod
    def goal_state_block_to_index(goal_state):
        """
        Creates a dictionary that maps each block in the goal state to its position within its respective stack.
        :param goal_state: A list of lists representing the desired block arrangement.
        :return: Dictionary mapping each block to its position in its stack.
        """
        goal_state_block_index_dict = {}
        for stack in goal_state:
            for position, block in enumerate(stack):
                goal_state_block_index_dict[block] = position
        return goal_state_block_index_dict

    @staticmethod
    def grab_first_state(queue):
        """Removes and returns the first state from the queue."""
        return queue.pop(0)

    @staticmethod
    def _is_new_state(state, visited):
        """Checks if the state has not been visited before."""
        return state not in visited

    @staticmethod
    def _add_to_visited(state, visited):
        """Marks a state as visited by adding it to the visited list."""
        visited.append(sorted(state))

    def bfs_tree(self, queue, goal_state, goal_state_index_dict):
        """
        Implements the Breadth-First Search (BFS) algorithm to generate a tree of visited states.
        It keeps exploring the possible moves until the goal state is reached or all possibilities are exhausted.

        :param queue: List of states yet to be explored.
        :param goal_state: The desired block arrangement to reach.
        :param goal_state_index_dict: Dictionary mapping each block in the goal state to its position.
        :return: The final state after BFS traversal, if the goal state is reached.
        """
        visited = []
        while queue:
            current_state = self.grab_first_state(queue)
            current_blocks = current_state[0]
            if self._is_new_state(current_blocks, visited):
                self._add_to_visited(current_blocks, visited)
                if current_blocks == goal_state:
                    return current_state
                self.generate_sub_states(queue, visited, current_state, goal_state_index_dict, goal_state)

    @staticmethod
    def get_shortest_path(bfs_tree):
        """
        This method backtracks from the final state (goal state) to the initial state through the tree generated by BFS.
        It extracts the sequence of moves that lead to the goal state.
        :param bfs_tree: The final state node in the BFS tree.
        :return: A list of moves leading to the goal state.
        """
        moves_to_goal_state = []
        while bfs_tree and bfs_tree[2]:
            moves_to_goal_state.insert(0, bfs_tree[1])
            bfs_tree = bfs_tree[2]
        return moves_to_goal_state

    @staticmethod
    def possible_moves(top_blocks_on_each_stack, top_block):
        """
        Given a list of the top blocks on each stack and a specific block, this method returns all possible moves for that block.
        A block can either be moved to the table or on top of another block.
        :param top_blocks_on_each_stack: List of the top blocks on each stack.
        :param top_block:The block for which possible moves are to be determined.
        :return: A list of tuples representing all possible moves for the selected block.
        """
        return [(top_block, target_move) if top_block != target_move else (top_block, 'Table')
                for target_move in top_blocks_on_each_stack]

    @staticmethod
    def map_bottom_to_blocks_stacked_on_top(cur_block_arrangement):
        """
        Returns a dictionary of the current state, where the block at the bottom of a stack maps to a list of blocks stacked on top of it.
        :param cur_block_arrangement: A list of lists representing the current block arrangement.
        :return: Dictionary mapping each base block to the blocks stacked on top of it.
        """
        return {stack[0]: stack[1:] for stack in cur_block_arrangement if stack}

    @staticmethod
    def get_base_block_for(state_dict, block):
        """
        Given a state dictionary generated by map_bottom_to_stacked_blocks and a specific block, this method returns the base block on which the given block is stacked.
        :param state_dict: Dictionary mapping each base block to the blocks stacked on top of it.
        :param block: The block for which the base block needs to be determined.
        :return: The base block on which the given block is stacked.
        """
        return next((base_block for base_block, stacked_blocks in state_dict.items() if block in stacked_blocks), None)

    def calculate_state_score(self, current_state, goal_state_indices, goal_state):
        """
        Calculates a weight for a given state based on its closeness to the goal state.
        The weight is calculated by comparing the position of blocks in the current state to their position in the goal state.
        A higher weight indicates the state is closer to the goal.

        :param current_state: A list of lists representing the current block arrangement.
        :param goal_state_indices: A dictionary mapping each block to its position in the goal state.
        :param goal_state: A list of lists representing the desired block arrangement.
        :return: The weight of the current state based on its closeness to the goal state.
        """
        score = 0
        current_state_mapping = self.map_bottom_to_blocks_stacked_on_top(current_state)
        goal_state_mapping = self.map_bottom_to_blocks_stacked_on_top(goal_state)

        for stack_index, stack in enumerate(current_state):
            for block_index, block in enumerate(stack):
                correct_index = goal_state_indices[block]
                # Check if the block is in the correct position and on the correct base block
                is_correct_position = correct_index == block_index
                is_correct_base = self.get_base_block_for(current_state_mapping, block) == self.get_base_block_for(
                    goal_state_mapping, block)

                score += block_index if is_correct_position and is_correct_base else -block_index
        return score

    def generate_sub_states(self, queue, visited, state, goal_state_index_dict, goal_state):
        """
        For a given state, this method generates all possible sub-states based on the blocks that can be moved.
        For each generated sub-state, it calculates a weight indicating how close the sub-state is to the goal state.
        Among all possible sub-states, the one with the highest weight (most promising one) is appended to the queue for further exploration.
        :param queue: The queue of states to be explored.
        :param visited: The list of already visited states.
        :param state: The current state being explored.
        :param goal_state_index_dict: A dictionary mapping each block to its position in the goal state.
        :param goal_state: The desired block arrangement.
        :return: None
        """
        current_arrangement = state[0]
        for stack in current_arrangement:
            if stack:
                top_block = stack[-1]
                possible_moves = self.possible_moves([s[-1] for s in current_arrangement], top_block)
                block_possible_state = []
                for each_move in possible_moves:
                    destination = each_move[1]
                    stack_wo_top_block = stack[0:stack.index(top_block)]
                    another_stack_in_state = [s for s in current_arrangement if s != stack]
                    if destination == 'Table':
                        another_stack_in_state_copy = copy.copy(another_stack_in_state)
                        another_stack_in_state_copy.append([top_block])
                        if len(stack_wo_top_block) > 0:
                            another_stack_in_state_copy.append(stack_wo_top_block)
                        sub_states_to_queue_table = [sorted(another_stack_in_state_copy), each_move, state]
                        current_state_score = self.calculate_state_score(another_stack_in_state_copy, goal_state_index_dict, goal_state)
                        block_possible_state.append((sub_states_to_queue_table, current_state_score))
                    else:
                        for single_stack in another_stack_in_state:
                            single_stack_copy = copy.copy(single_stack)
                            if destination in single_stack_copy:
                                copy_of_another_stack_in_state = copy.copy(another_stack_in_state)
                                copy_of_another_stack_in_state.remove(single_stack_copy)
                                single_stack_copy.append(each_move[0])
                                copy_of_another_stack_in_state.append(single_stack_copy)
                                if len(stack_wo_top_block) > 0:
                                    copy_of_another_stack_in_state.append(stack_wo_top_block)
                                sub_states_to_queue_table2 = [sorted(copy_of_another_stack_in_state), each_move, state]
                                current_state_score2 = self.calculate_state_score(
                                    copy_of_another_stack_in_state, goal_state_index_dict, goal_state)
                                block_possible_state.append((sub_states_to_queue_table2, current_state_score2))
                block_possible_state.sort(key=lambda x: x[1])
                if sorted(block_possible_state[-1][0][0]) not in visited:
                    queue.append(block_possible_state[-1][0])
                possible_moves.clear()

    def solve(self, initial_arrangement, goal_arrangement):
        """
        Given an initial arrangement of blocks and a goal arrangement, this method finds a sequence of moves to reach the goal arrangement from the initial one.
        :param initial_arrangement:
        :param goal_arrangement:
        :return:
        """
        initial_state = [initial_arrangement, None, None]
        goal_state = sorted(goal_arrangement)
        goal_state_index_dict = self.goal_state_block_to_index(goal_state)
        queue = [initial_state]
        tree_of_visited_states = self.bfs_tree(queue, goal_state, goal_state_index_dict)
        optimal_moves = self.get_shortest_path(tree_of_visited_states)
        return optimal_moves


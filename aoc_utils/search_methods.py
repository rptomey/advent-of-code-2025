import functools
import collections
import sys

# If needed, change recursion limit for deep graphs
# sys.setrecursionlimit(10_000)

def dfs(start_state, get_neighbors, is_goal, count_mode=True):
    """
    A reusable DFS (depth first search) helper.
    
    Args:
        start_state: The initial tuple/object representing where you are.
        get_neighbors: A function(state) -> return list of valid next states.
        is_goal: A function(state) > return bool (True if this state solves the puzzle).
        count_mode: If True, returns TOTAL paths. If False, returns ANY valid path (bool).

    Returns:
        int: total valid paths (count_mode == True)
        OR
        bool: valid path exists (count_mode == False)
    """

    @functools.cache
    def search(state):
        # Check if we reached the goal
        if is_goal(state):
            return 1 if count_mode else True
        
        # Recursion
        total = 0
        for next_state in get_neighbors(state):
            result = search(next_state)

            if count_mode:
                total += result
            elif result:    # If we just need one valid path and have found it
                return True
            
        return total if count_mode else False
    
    # Start the search and return the overall result
    return search(start_state)

def bfs(start_state, get_neighbors, is_goal):
    """
    A reusable BFS (breadth first search) helper for finding the SHORTEST path.
    
    Args:
        start_state: The initial tuple/object representing where you are.
        get_neighbors: A function(state) -> return list of valid next states.
        is_goal: A function(state) > return bool (True if this state solves the puzzle).

    Returns:
        int: minimum number of steps to reach goal (-1 if unreachable)
    """

    # Start a queue that stores tuples of (current_state, step_count)
    queue = collections.deque([(start_state, 0)])

    # Store a set of states that we've already visited to prevent loops and redundant processing
    visited = {start_state}

    while queue:
        current_state, steps = queue.popleft()  # Oldest first (FIFO)

        if is_goal(current_state):
            return steps
        
        for next_state in get_neighbors(current_state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, steps+1))

    # If goal was never reached and queue is empty
    return -1
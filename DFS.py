import time
import tracemalloc

DIRECTIONS = [
    (-1, 0, "UP"),
    (1, 0, "DOWN"),
    (0, -1, "LEFT"),
    (0, 1, "RIGHT")
]
#
def find_positions(maze):
    start, goal = None, None
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'G':
                goal = (r, c)
    return start, goal

def solve_dfs_tailored(maze, case_num=1, case_name=""):
    
    # 1. START TIMING & MEMORY TRACKING 
    tracemalloc.start()
    start_time = time.perf_counter()

    # Included in timing: Scanning grid for 'S' and 'G'
    start, goal = find_positions(maze)
    if start is None or goal is None:
        tracemalloc.stop()
        print(f"ERROR: Case {case_num} missing 'S' or 'G'\n")
        return

    rows, cols = len(maze), len(maze[0])
    
    stack = [(start, 0)]
    in_stack = {start}  
    visited = set()
    closed_list = []
    parent = {}
    
    step = 0
    goal_found = False
    trace_steps = []

    # Included in timing: DFS search loop
    while stack:
        current, depth = stack.pop()
        in_stack.remove(current)  
        
        if current in visited:
            continue
            
        step += 1
        visited.add(current)
        closed_list.append(current)
        
        if current == goal:
            goal_found = True
            trace_steps.append((step, current, depth, [], list(stack), True))
            break
            
        pushed = []
        for dr, dc, name in DIRECTIONS:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#':
                pos = (nr, nc)
                if pos not in visited and pos not in in_stack:
                    parent[pos] = current
                    stack.append((pos, depth + 1))
                    in_stack.add(pos)
                    pushed.append((pos, name))

        trace_steps.append((step, current, depth, pushed, list(stack), False))

    
    # 2. STOP TIMING & MEMORY TRACKING (SEARCH & SETUP COMPLETE)
    end_time = time.perf_counter()
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time_ms = (end_time - start_time) * 1000
    memory_used_kb = peak_memory / 1024

  
    path = []
    if goal_found:
        curr = goal
        while curr in parent:
            path.append(curr)
            curr = parent[curr]
        path.append(start)
        path.reverse()

    # 3. PRINT OUTPUTS
    print("\n" + "=" * 50)
    print(f" {case_name.upper()}")
    print("=" * 50)
    
    print("\n   Original Maze:\n")
    for row in maze:
        print("   ", " ".join(row))
    print()

    for s_num, curr, d_val, push_list, stack_snap, is_goal in trace_steps:
        print(f"Step {s_num:02d} | Exploring Node {curr} (Depth {d_val})")
        if is_goal:
            print("        └─> GOAL REACHED!\n")
        else:
            if push_list:
                formatted_pushed = [f"{pos} ({name})" for pos, name in push_list]
                print(f"        Pushed : {', '.join(formatted_pushed)}")
            stack_nodes = [n for n, d in reversed(stack_snap)]
            print(f"        Stack  : {stack_nodes}\n")

    # Final report
    print("-" * 50)
    print(f"   FINAL: {case_name}")
    print("-" * 50)
    
    if goal_found:
        sol_maze = [row[:] for row in maze]
        for r, c in path:
            if sol_maze[r][c] not in ('S', 'G'):
                sol_maze[r][c] = '*'
        
        print("\n   Final Solved Maze:\n")
        for row in sol_maze:
            print("   ", " ".join(row))
            
        print(f"\n   Final Path         : {' -> '.join(map(str, path))}")
        print(f"   Status             : SOLVED")
        print(f"   Path Cost (Steps) : {len(path) - 1}")
        print(f"   Nodes Explored     : {len(closed_list)}")
        print(f"   Time Taken         : {execution_time_ms:.4f} ms")
        print(f"   Memory Used        : {memory_used_kb:.2f} KB\n")
    else:
        print(f"\n   Status             : FAILED (Unreachable Goal)")
        print(f"   Nodes Explored     : {len(closed_list)}")
        print(f"   Time Taken         : {execution_time_ms:.4f} ms")
        print(f"   Memory Used        : {memory_used_kb:.2f} KB\n")


# TEST CASES
maze1 = [
    [".",".",".",".","G"],
    [".",".",".",".","."],
    [".",".",".",".","."],
    [".",".",".",".","."],
    ["S",".",".",".","."]
]

maze2 = [
    [".","S","#",".","."],
    [".","#",".","#","."],
    [".",".",".",".","."],
    ["#",".","#",".","."],
    [".",".",".",".","G"]
]

maze3 = [
    [".","#","#","#","#","#","#"],
    [".","S",".",".","#",".","#"],
    ["#","#","#",".","#",".","#"],
    ["#",".",".",".",".",".","#"],
    ["#",".","#","#","#",".","#"],
    ["#",".",".",".","#",".","."],
    ["#","#","#",".","#","#","G"]
]

maze4 = [
    [".",".",".",".",".",".",".","."],
    ["S",".",".","#",".",".",".","."],
    [".",".",".","#",".",".",".","."],
    [".",".",".","#",".",".",".","."],
    [".",".",".",".",".",".",".","G"],
    [".",".",".",".",".",".",".","."]
]

maze5 = [
    [".","#","#","#","#","#","#","#","#"],
    [".",".",".",".",".",".",".","#","."],
    ["#","#",".","#","#","#",".","#","."],
    ["#",".",".",".",".",".","#",".","#"],
    ["#",".","#","#",".",".",".","#","#"],
    ["#",".",".","#","S","#",".",".","#"],
    ["#","#",".",".","#","#","#","#","#"],
    ["#",".",".",".",".",".",".",".","G"]
]

maze6 = [
    [".",".",".","G"],
    [".","#",".","."],
    [".","#",".","."],
    ["S",".",".","."]
]

maze7 = [
    [".","#","#","#","G"],
    [".",".",".",".","."],
    ["#","#","#","#","."],
    [".",".",".",".","."],
    [".","S",".",".","."]
]

maze8 = [
    [".",".","#",".","G"],
    [".","#","S","#","."],
    [".","#",".","#","."],
    [".",".",".",".","."],
    ["#","#","#","#","#"]
]

maze9 = [
    [".",".",".","#","."],
    ["#","#",".","#","."],
    ["S",".",".",".","."],
    [".","#","#","#","."],
    [".",".",".",".","G"]
]

maze10 = [
    ["S",".","#",".","."],
    ["#",".","#",".","#"],
    ["#",".",".",".","#"],
    ["#","#","#",".","#"],
    [".",".",".",".","G"]
]

all_cases = [
    ("Maze 1", maze1),
    ("Maze 2", maze2),
    ("Maze 3", maze3),
    ("Maze 4", maze4),
    ("Maze 5", maze5),
    ("Maze 6", maze6),
    ("Maze 7", maze7),
    ("Maze 8", maze8),
    ("Maze 9", maze9),
    ("Maze 10", maze10)
]

if __name__ == "__main__":
    for num, (name, maze) in enumerate(all_cases, 1):
        solve_dfs_tailored(maze, case_num=num, case_name=name)

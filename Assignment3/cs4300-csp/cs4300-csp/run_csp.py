from cs4300_csp_parser import parse_cs4300
from cs4300_csp import solve_backtracking, solve_backtrackingOG
import time

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python run_csp.py <problem.csp>")
        sys.exit(1)
    csp = parse_cs4300(sys.argv[1])
    any_sol = False
    print("With Heuristic:")
    start = time.perf_counter()
    for i, sol in enumerate(solve_backtracking(csp), 1):
        any_sol = True
        print(f"Solution #{i}: {sol}")
    if not any_sol:
        print("No solutions.")

    end = time.perf_counter()

    print(f"Total time: {end - start}")

    print()
    print()

    print("Without Heuristic:")
    start = time.perf_counter()
    for i, sol in enumerate(solve_backtrackingOG(csp), 1):
        any_sol = True
        print(f"Solution #{i}: {sol}")
    if not any_sol:
        print("No solutions.")

    end = time.perf_counter()

    print(f"Total time: {end - start}")

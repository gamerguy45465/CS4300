from cs4300_csp_parser import parse_cs4300
from cs4300_csp import solve_backtracking

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python run_csp.py <problem.csp>")
        sys.exit(1)
    csp = parse_cs4300(sys.argv[1])
    print(csp)
    any_sol = False
    for i, sol in enumerate(solve_backtracking(csp), 1):
        any_sol = True
        print(f"Solution #{i}: {sol}")
        #print(sol['X11'], sol['X12'], sol['X13'], sol['X14'])
        #print(sol['X21'], sol['X22'], sol['X23'], sol['X24'])
        #print(sol['X31'], sol['X32'], sol['X33'], sol['X34'])
        #print(sol['X41'], sol['X42'], sol['X43'], sol['X44'])
        #print()
    if not any_sol:
        print("No solutions.")

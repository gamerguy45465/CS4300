#!/usr/bin/env python3

import sys
from agent import build_agent
import model
import numpy as np

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py \"<your question about a city to visit.>\"")
        return
    query = sys.argv[1]
    dates, start_times, end_times, titles, locations, descriptions, urls, categories = model.start_pandas()
    agent = build_agent(verbose=2)
    print("Query:", query)
    result = agent.run(query)
    print("\n=== Final Answer ===\n", result)

if __name__ == "__main__":
    main()

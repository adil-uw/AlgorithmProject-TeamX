# main.py
# Main driver for running max-flow algorithms on any input graph.
import time
import os
from read_graph import read_graph
from Algorithms.ford_fulkerson import fordFulkMaxFlow             #ADIL
from Algorithms.scaling_ford_fulkerson import max_flow_scaling    #AAYUSH
from Algorithms.preflow_push import max_flow_preflow              #LAKSHMAN  
# ---------------------------------------------------------------


def choose_algorithm():
    while True:
        print("\nChoose Algorithm:")
        print("1. Ford–Fulkerson (DFS)")
        print("2. Scaling Ford–Fulkerson")
        print("3. Preflow–Push")
        print("B. Back")
        print("Q. Quit")

        choice = input("Enter choice: ").strip().lower()

        if choice in ("1", "2", "3"):
            return choice
        if choice == "b":
            return None
        if choice == "q":
            exit()

        print("Invalid option. Try again.")


def choose_graph_file():
    while True:
        print("\nChoose Graph Type:")
        print("1. Bipartite")
        print("2. Mesh")
        print("3. Random")
        print("4. Fixed-degree")
        print("B. Back")
        print("Q. Quit")

        t = input("Enter choice: ").strip().lower()

        if t == "b":
            return None
        if t == "q":
            exit()

        if t not in ("1", "2", "3", "4"):
            print("Invalid option. Try again.")
            continue

        if t == "1":
            folder = "Inputgraphs/Bipartite/"
        elif t == "2":
            folder = "Inputgraphs/Mesh/"
        elif t == "3":
            folder = "Inputgraphs/Random/"
        else:
            folder = "Inputgraphs/Fixed/"

        # ---------- FILE SELECTION LOOP ----------
        while True:
            print(f"\nEnter file name inside {folder}")
            print("Type B to go back, Q to quit.")
            filename = input("File name (with .txt): ").strip()

            if filename.lower() == "b":
                break   # go back to graph type menu
            if filename.lower() == "q":
                exit()

            full_path = folder + filename

            if os.path.exists(full_path):
                return full_path

            print("\nERROR: File not found.")
            print("Please enter the filename again, or type B to go back, Q to quit.")



def main():
    print("========== MAX FLOW PROJECT ==========")

    # ------------------ MAIN SELECTION LOOP ------------------
    while True:
        algo_choice = choose_algorithm()
        if algo_choice is None:
            continue   # go back to menu

        graph_path = choose_graph_file()
        if graph_path is None:
            continue   # go back

        # we have both algorithm + graph → break loop
        break
    # --------------------------------------------------------

    print(f"\nLoading graph: {graph_path}")
    n, edges, s, t = read_graph(graph_path)
    print(f"Graph loaded: {n} nodes, {len(edges)} edges")
    print(f"Source ID: {s}   Sink ID: {t}")

    # ---------- Algorithm Selection ----------
    if algo_choice == "1":
        algo_name = "Ford–Fulkerson (DFS)"
        print("\n[INFO] Ford–Fulkerson selected.")
        algo = fordFulkMaxFlow                     #ADIL ALGO CALLED HERE
    elif algo_choice == "2":
        algo_name = "Scaling Ford–Fulkerson"
        print("\n[INFO] Scaling FF selected.")
        print("*****************Algorithm NOT IMPLEMENTED YET")
        algo = max_flow_scaling                #AAYUSH ALGO CALLED HERE
    else:
        algo_name = "Preflow–Push"
        print("\n[INFO] Preflow–Push selected.")
        print("*****************Algorithm NOT IMPLEMENTED YET")
        algo = max_flow_preflow                 #LAKSHMAN ALGO CALLED HERE
        

    print(f"\nRunning {algo_name}...\n")
    
    start = time.time()
    maxflow = algo(n, edges, s, t)
    end = time.time()

    print("====================================\n")
    print(f"Algorithm: {algo_name}")
    print(f"Graph file: {graph_path}")
    print(f"Total nodes: {n}")
    print(f"Total edges: {len(edges)}")
    print(f"Source (s): {s}")
    print(f"Sink (t):   {t}")
    print("Max Flow:   ", maxflow)
    print(f"Runtime:    {end - start:.6f} seconds")
    print("====================================\n")

if __name__ == "__main__":
    main()

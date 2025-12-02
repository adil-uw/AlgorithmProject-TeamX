# read_graph.py

from typing import Dict, List, Tuple

Edge = Tuple[int, int, int]   # (u, v, capacity)


def read_graph(path: str) -> Tuple[int, List[Edge], int, int]:
    """
    Reads ANY graph input file in the format:
        <u_label> <v_label> <capacity>

    Node labels may be:
        "s", "t", "1", "5", "l3", "r10", "v7", "(2,5)"

    Returns:
        n      -> total number of nodes (int)
        edges  -> list of (u, v, capacity) using INTEGER node IDs
        s      -> integer ID of source node 's'
        t      -> integer ID of sink node 't'
    """

    label_to_id: Dict[str, int] = {}
    edges: List[Edge] = []
    next_id = 0

    def get_id(label: str) -> int:
        nonlocal next_id
        if label not in label_to_id:
            label_to_id[label] = next_id
            next_id += 1
        return label_to_id[label]

    with open(path, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) != 3:
                raise ValueError(f"Invalid line in {path}: {line}")

            u_label, v_label, cap_str = parts
            u = get_id(u_label)
            v = get_id(v_label)
            c = int(cap_str)

            edges.append((u, v, c))

    if "s" not in label_to_id or "t" not in label_to_id:
        raise ValueError(f"Graph file {path} must contain both 's' and 't' labels.")

    n = next_id
    s = label_to_id["s"]
    t = label_to_id["t"]

    return n, edges, s, t

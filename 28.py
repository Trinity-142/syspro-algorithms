from typing import List, Dict



def reversed_graph(adj: Dict) -> Dict:
    res = {}
    for key, values in adj.items():
        for value in values:
            if value in res:
                res[value].append(key)
            else:
                res[value] = [key]
    return res


def kosaraju(vertices: List[str], adj: Dict) -> List:
    visited = set()
    timings = []
    time = 0
    reversed_adj = reversed_graph(adj)

    def dfs1(vertex: str):
        nonlocal time
        visited.add(vertex)
        if vertex in reversed_adj:
            for nxt in reversed_adj[vertex]:
                if nxt not in visited:
                    dfs1(nxt)
        timings.append(vertex)
        time += 1

    for vertex in vertices:
        if vertex not in visited:
            dfs1(vertex)

    visited = set()
    res = []

    def dfs2(vertex: int, scc: List):
        visited.add(vertex)
        if vertex in adj:
            for nxt in adj[vertex]:
                if nxt not in visited:
                    dfs2(nxt, scc)
        scc.append(vertex)

    for vertex in reversed(timings):
        if vertex not in visited:
            scc = []
            dfs2(vertex, scc)
            res.append(scc)

    return res


def recursive_calls(SCCs: List, adj: Dict):
    print("Recursive calls in functions:")
    for scc in SCCs:
        if len(scc) == 1:
            func = scc[0]
            if (func in adj and adj[func][0] != func) or func not in adj:
                print(f"{func}: False")
            else:
                print(f"{func}: True")
        else:
            for func in scc:
                print(f"{func}: True")


tests = [(["foo", "bar", "baz", "qux"],
          {
             "foo": ["bar", "baz", "qux"],
             "bar": ["baz", "foo", "bar"],
             "qux": ["qux"]
          }),
         (["A", "B", "C"],
          {
             "A": ["B"],
             "B": ["C"],
             "C": ["A"]
          }),
         (["X", "Y", "Z"],
          {
             "X": ["Y"],
             "Y": ["X", "Z"],
          }),
         (["one", "two", "three"],
          {
             "one": ["two", "one"],
             "two": ["three"],
             "three": ["one"]
          }),
         (["alpha", "beta", "gamma"],
          {
             "alpha": ["beta"],
             "beta": ["gamma"],
          })]

if __name__ == "__main__":
    for vertices, adj in tests:
        SCCs = kosaraju(vertices, adj)
        print(f"List of strongly connected components: {SCCs}")
        print(f"Maximum recursive component has {max(len(SCC) for SCC in SCCs)} functions")
        recursive_calls(SCCs, adj)
        print("-" * 50)

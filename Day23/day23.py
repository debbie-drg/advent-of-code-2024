import sys
import heapq


class Node:
    def __init__(self, idx: str, neighbour: str) -> None:
        self.idx = idx
        self.neighbours = {neighbour}

    def __hash__(self) -> int:
        return self.idx.__hash__()

    def add_neighbour(self, neighbour: str):
        self.neighbours.add(neighbour)


class NetworkGraph:
    def __init__(self, pairs: list[str]) -> None:
        self.nodes = {}
        self.triplets = set()
        for pair in pairs:
            idx1, idx2 = pair.split("-")
            self.add_nodes(idx1, idx2)
            self.check_triplets(idx1, idx2)

    def add_nodes(self, idx1: str, idx2: str):
        if idx1 not in self.nodes:
            self.nodes[idx1] = Node(idx1, idx2)
        else:
            self.nodes[idx1].add_neighbour(idx2)
        if idx2 not in self.nodes:
            self.nodes[idx2] = Node(idx2, idx1)
        else:
            self.nodes[idx2].add_neighbour(idx1)

    def check_triplets(self, idx1: str, idx2: str):
        for neighbour in self.nodes[idx1].neighbours:
            if neighbour in self.nodes[idx2].neighbours:
                self.triplets.add(frozenset([idx1, idx2, neighbour]))

    def count_triplets_starting_with(self, starts_with: str) -> int:
        count = 0
        for triplet in self.triplets:
            for item in triplet:
                if starts_with == item[0]:
                    count += 1
                    break
        return count

    def all_connected(self, nodes: set):
        return all(
            [
                node_2 in self.nodes[node_1].neighbours
                for node_1 in nodes
                for node_2 in nodes
                if node_1 < node_2
            ]
        )

    def get_password(self) -> str:
        neighbour_lists = [
            self.nodes[node].neighbours.union({node}) for node in self.nodes
        ]
        queue = [(-len(neighbours), neighbours) for neighbours in neighbour_lists]
        while queue:
            priority, nodes = heapq.heappop(queue)
            if self.all_connected(nodes):
                return ",".join(sorted(nodes))
            for node in nodes:
                heapq.heappush(queue, (priority + 1, nodes - {node}))
        return ""


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    network_pairs = open(file_name).read().strip().split("\n")
    network_graph = NetworkGraph(network_pairs)
    triplet_count = network_graph.count_triplets_starting_with("t")
    print(f"The number of triplets with a computer starting with t is {triplet_count}")
    print(f"The password is {network_graph.get_password()}")

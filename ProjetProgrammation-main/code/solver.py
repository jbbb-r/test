from grid import Grid
import numpy as np

class Solver:
    """
    A solver class based on greedy method.

    Attributes: 
    -----------
    grid: Grid
        The grid
    pairs: list[tuple[tuple[int]]]
        A list of pairs, each being a tuple ((i1, j1), (i2, j2))
    """

    def __init__(self, grid : Grid):
        """
        Initializes the solver.

        Parameters: 
        -----------
        grid: Grid
            The grid
        """
        self.grid = grid
        self.pairs = list()

    def score(self):
        """
        Computes the of the list of pairs in self.pairs
        """
        score = np.sum([self.grid.cost(((i1, j1), (i2, j2))) for ((i1, j1), (i2, j2)) in self.pairs])
        taken = [cell for pair in self.pairs for cell in pair]
        score += np.sum([self.grid.value[i][j] for i in range(self.grid.n) for j in range(self.grid.m) if (i, j) not in taken and not self.grid.is_forbidden(i, j)])
        return score
    
    def run(self):
        """
        Greed algorithm returning the best pairs in a list. Naive algorithm.
        """
        taken = []
        for i in range(self.grid.n): # O(n)
            for j in range(self.grid.m): # O(m)
                if (i, j) not in taken and not self.grid.is_forbidden(i, j): # If cell (i, j) is not already taken O(n)
                    for neighbor in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                        if 0 <= neighbor[0] < self.grid.n and 0 <= neighbor[1] < self.grid.m: # Not on the edge
                            if neighbor not in taken and self.grid.is_valid_pair((i, j), neighbor): # If neighbor is compatible and not taken yet 
                                self.pairs.append(((i, j), neighbor))
                                taken.append((i, j))
                                taken.append(neighbor)
                                break
        # Greedy Algorithm has a complexity dominated by O(n^2*m)   

class SolverMatching:
    """
    A solver class. 

    Attributes: 
    -----------
    grid: Grid
        The grid
    pairs: list[tuple[tuple[int]]]
        A list of pairs, each being a tuple ((i1, j1), (i2, j2))
    """
        
    def __init__(self, grid : Grid):
        super().__init__(grid)
        self.graph = self.grid.to_bipartite_graph()
    
    def ford_fulkerson(self):
        matching = {}

        def bfs(start, visited):
            """
            """
            queue = [start]
            visited.add(start)

            while queue:
                cell = queue.pop(0)
                for neighbor in self.graph[cell]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        if neighbor not in matching:
                            # Mettre à jour le matching
                            matching[neighbor] = cell
                            matching[cell] = neighbor
                            return True
            return False

        # Trouver un matching maximal
        for cell in self.graph['even']:
            if cell not in matching:
                bfs(cell, set())

        # Convertir le matching en liste de paires
        pairs = [(cell, matching[cell]) for cell in matching if cell in self.graph['even']]
        return pairs

    
    def score(self):
        return super().score() # Calling score methods from SolverGreedy
    
    def run(self):
        self.pairs = self.find_matching()


class SolverEmpty(Solver):
    def run(self):
        pass





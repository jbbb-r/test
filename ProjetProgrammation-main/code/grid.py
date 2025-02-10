"""
This is the grid module. It contains the Grid class and its associated methods.
"""
import numpy as np
import matplotlib.pyplot as plt

class Grid():
    """
    A class representing the grid. 

    Attributes: 
    -----------
    n: int
        Number of lines in the grid
    m: int
        Number of columns in the grid
    color: list[list[int]]
        The color of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    value: list[list[int]]
        The value of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    colors_list: list[char]
        The mapping between the value of self.color[i][j] and the corresponding color
    """
    

    def __init__(self, n, m, color=[], value=[]):
        """
        Initializes the grid.

        Parameters: 
        -----------
        n: int
            Number of lines in the grid
        m: int
            Number of columns in the grid
        color: list[list[int]]
            The grid cells colors. Default is empty (then the grid is created with each cell having color 0, i.e., white).
        value: list[list[int]]
            The grid cells values. Default is empty (then the grid is created with each cell having value 1).
        
        The object created has an attribute colors_list: list[char], which is the mapping between the value of self.color[i][j] and the corresponding color
        """
        self.n = n
        self.m = m
        if not color:
            color = [[0 for j in range(m)] for i in range(n)]            
        self.color = color
        if not value:
            value = [[1 for j in range(m)] for i in range(n)]            
        self.value = value
        self.colors_list = ['w', 'r', 'b', 'g', 'k']

    def __str__(self): 
        """
        Prints the grid as text.
        """
        output = f"The grid is {self.n} x {self.m}. It has the following colors:\n"
        for i in range(self.n): 
            output += f"{[self.colors_list[self.color[i][j]] for j in range(self.m)]}\n"
        output += f"and the following values:\n"
        for i in range(self.n): 
            output += f"{self.value[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: n={self.n}, m={self.m}>"

    def plot(self): 
        """
        Plots a visual representation of the grid.
        """
        fig, ax = plt.subplots()
        cmap = {0: 'white', 1: 'red', 2: 'blue', 3: 'green', 4: 'black'}
        grid_colors = np.array([[cmap[self.color[i][j]] for j in range(self.m)] for i in range(self.n)])
        ax.set_xticks(np.arange(self.m + 1) - 0.5, minor=True)
        ax.set_yticks(np.arange(self.n + 1) - 0.5, minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
        ax.set_xticks([])
        ax.set_yticks([])
        for i in range(self.n):
            for j in range(self.m):
                ax.add_patch(plt.Rectangle((j, self.n - i - 1), 1, 1, color=grid_colors[i, j]))
                ax.text(j + 0.5, self.n - i - 0.5, str(self.value[i][j]), ha='center', va='center', fontsize=12)
        plt.show()


    def is_forbidden(self, i, j):
        """
        Returns True is the cell (i, j) is black and False otherwise
        """
        return (self.color[i][j] == 4) # black is coded as 4

    def cost(self, pair):
        """
        Returns the cost of a pair
 
        Parameters: 
        -----------
        pair: tuple[tuple[int]]
            A pair in the format ((i1, j1), (i2, j2))

        Output: 
        -----------
        cost: int
            the cost of the pair defined as the absolute value of the difference between their values
        """
        (i1, j1), (i2, j2) = pair[0], pair[1]
        return abs(self.value[i1][j1] - self.value[i2][j2]) # 


    def is_valid_pair(self, cell1, cell2):
        """
       Check if a pairs is valid regarding of the game's rules
        """
        (i1, j1), (i2, j2) = cell1, cell2
        if self.is_forbidden(i1, j1) or self.is_forbidden(i2, j2):
            return False
        color1, color2 = self.color[i1][j1], self.color[i2][j2]
        if color1 == 0 or color2 == 0:
            return True # White being compatible with every cell : any pair with white is valid
        if color1 == color2:
            return True  # Same colors are compatible
        if (color1, color2) in [(1, 2), (2, 1)]:
            return True  # Red and blue are compatible with each other
        return False

    def all_pairs(self):
        """
        Returns a list of all valid pairs in the grid
        """
        pairs = []
        for i in range(self.n):
            for j in range(self.m):
                for neighbor in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                    if 0 <= neighbor[0] < self.n and 0 <= neighbor[1] < self.m: # Checking if the cell exist
                        if self.is_valid_pair((i, j), neighbor) and ((i, j), neighbor) not in pairs: # We avoid duplicates
                            pairs.append(((i, j), neighbor))
        return pairs
    
    def parity(self, cell):
        (i, j) = cell
        if (i + j % 2 == 0): return "even" 
        else: return "odd"
    
    def to_bipartite_graph(self):
        """
        Returns a bipartite graph version of the grid, i.e., creates a graph of the grid with two sets of even cells, odd cells.
        The graph already contains the valid pairs as edges.
        Parameters: None
        Result: A graph G stored as a dict type with two underdict even and odd.
        """
        G = {
            'even': {},
            'odd': {}
        } # Preparing the two sets of edges.

    # Adding edges with color and adjacency constraints
        for i in range(self.n):
            for j in range(self.m):

                if self.color[i][j] != 4:  # Ignoring black cells

                    parity = self.parity((i, j))
                    for ni, nj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]: # Neighbors
                        if 0 <= ni < self.n and 0 <= nj < self.m:  # If existing cell
                            if self.is_valid_pair((i, j), (ni, nj)):  # Constraints
                                nparity = self.parity((ni, nj))
                                if (i, j) not in G[parity]:
                                    G[parity][(i, j)] = [] # Creating the edges if not existing
                                if (ni, nj) not in G[nparity]:
                                    G[nparity][(ni, nj)] = [] # Creating the edges if not existing
                                G[parity][(i, j)].append((ni, nj)) 
                                G[nparity][(ni, nj)].append((i, j)) # Non-oriented graph
        return G


    @classmethod
    def grid_from_file(cls, file_name, read_values=False): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "n m" 
            - next n lines contain m integers that represent the colors of the corresponding cell
            - next n lines [optional] contain m integers that represent the values of the corresponding cell
        read_values: bool
            Indicates whether to read values after having read the colors. Requires that the file has 2n+1 lines

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            color = [[] for i_line in range(n)]
            for i_line in range(n):
                line_color = list(map(int, file.readline().split()))
                if len(line_color) != m: 
                    raise Exception("Format incorrect")
                for j in range(m):
                    if line_color[j] not in range(5):
                        raise Exception("Invalid color")
                color[i_line] = line_color

            if read_values:
                value = [[] for i_line in range(n)]
                for i_line in range(n):
                    line_value = list(map(int, file.readline().split()))
                    if len(line_value) != m: 
                        raise Exception("Format incorrect")
                    value[i_line] = line_value
            else:
                value = []

            grid = Grid(n, m, color, value)
        return grid



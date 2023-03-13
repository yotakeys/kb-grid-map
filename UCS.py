from source import Environment

class Node():
    def __init__(self, coord: tuple, parent, action: int, gx: int):
        self.coord = coord
        self.parent = parent
        self.action = action

        self.gx = gx

class Frontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def findMinNode(self, explored):
        min = 1000000
        min_node = self.frontier[0]
        for node in self.frontier:
            f = node.gx
            if f < min and node.coord not in explored:
                min = f
                min_node = node
        return min_node
        
    def remove(self, explored):
        if len(self.frontier) == 0:
            raise Exception("Empty frontier")
        else:  
            minNode = self.findMinNode(explored)
            if minNode is not None:
                self.frontier.remove(minNode)
                return minNode
            return None

    def length(self):
        return len(self.frontier)

class UCS():
    def __init__(self,
                searched = 9, 
                shortest = 5) -> None:

        self.env = Environment()
        self.minimum_steps = 0
        self.wall = self.env.wall
        self.path = self.env.path
        self.start = self.env.start
        self.goal = self.env.goal
        self.searched = searched
        self.shortest = shortest

        self.frontier = Frontier()
        self.explored = []
        
        self.map = self.env.grid_map
        self.ylen = len(self.map)
        self.xlen = len(self.map[0])

        self.find_start_goal()
        self.start_node = Node(self.start_index, None, None, 0)

        self.explored.append(self.start_index)
        
    def find_start_goal(self) -> None:
        for i in range(self.ylen):
            for j in range(self.xlen):
                if self.map[i][j] == self.start:
                    self.start_index = (i, j)
                if self.map[i][j] == self.goal:
                    self.goal_index = (i, j)
    
        
    def inside(self, i, j) -> bool:
        if ((i >= 0 and i < self.ylen) and (j >= 0 and j < self.xlen)):
            if self.map[i][j] != self.wall:
                if ((i, j) not in self.explored):
                    return True
        return False

    def print_map(self, show_explored = False):
        for i in self.map:
            if show_explored:
                print("".join(str(i)))
            else:
                print("".join(str(i)).replace(self.searched, self.path))

    def search(self, node: Node):
        self.explored.append(node.coord)
        
        if node.coord == self.goal_index:
            self.minimum_steps = node.gx
            parent_node = node.parent
            while parent_node.parent != None:
                i, j = parent_node.coord
                self.map[i][j] = self.shortest

                tmp = parent_node
                parent_node = tmp.parent
            return

        i, j = node.coord
        if self.map[i][j] != self.start:
            self.map[i][j] = self.searched

        if self.inside(i-1, j):
            tmp = Node((i-1, j), node, "up", node.gx + 1)
            self.frontier.add(tmp)
        if self.inside(i, j+1):
            tmp = Node((i, j+1), node, "right", node.gx + 1)
            self.frontier.add(tmp)
        if self.inside(i+1, j):
            tmp = Node((i+1, j), node, "down", node.gx + 1)
            self.frontier.add(tmp)
        if self.inside(i, j-1):
            tmp = Node((i, j-1), node, "left", node.gx + 1)
            self.frontier.add(tmp)
        
        searched_node = self.frontier.remove(self.explored)
        
        if searched_node is not None:
            self.search(searched_node)

if __name__ == "__main__":
    
    ucs = UCS()

    ucs.search(ucs.start_node)
    ucs.print_map(show_explored = True)
    print("Cost Solved :", ucs.minimum_steps+1)
    print("Node Explored :",len(ucs.explored)-1)
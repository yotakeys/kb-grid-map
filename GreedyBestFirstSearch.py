from source import Environment
import math

class Node():
    def __init__(self, coord: tuple, parent, action: int, hx: float):
        self.coord = coord
        self.parent = parent
        self.action = action
        self.hx = hx

class Frontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def findMinNode(self, explored):
        min = 1000000
        min_node = self.frontier[0]
        for node in self.frontier:
            if node.hx < min  and node.coord not in explored:
                min = node.hx
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

class GreedyBestFS():
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
        x1,y1 = self.start_index
        x2,y2 = self.goal_index
        self.start_node = Node(self.start_index, None, None, self.countHx(x1,x2,y1,y2))

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
                if not ((i, j) in self.explored):
                    return True
        return False

    def print_map(self, show_explored = False):
        for i in self.map:
            if show_explored:
                print("".join(str(i)))
            else:
                print("".join(str(i)).replace(self.searched, self.path))

    def countHx(self, x1,x2,y1,y2):
        d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return d

    def search(self, node: Node):
        self.explored.append(node.coord)
        
        if node.coord == self.goal_index:
            parent_node = node.parent
            steps = 1
            while parent_node.parent != None:
                i, j = parent_node.coord
                self.map[i][j] = self.shortest
                steps += 1

                tmp = parent_node
                parent_node = tmp.parent

            self.minimum_steps = steps
            return

        i, j = node.coord
        
        if self.map[i][j] != self.start:
            self.map[i][j] = self.searched

        if self.inside(i-1, j):
            x2,y2 = self.goal_index
            tmp = Node((i-1, j), node, "up", self.countHx(i-1,j,x2,y2))
            self.frontier.add(tmp)
        if self.inside(i, j+1):
            x2,y2 = self.goal_index
            tmp = Node((i, j+1), node, "right", self.countHx(i,j+1,x2,y2))
            self.frontier.add(tmp)
        if self.inside(i+1, j):
            x2,y2 = self.goal_index
            tmp = Node((i+1, j), node, "down", self.countHx(i+1,j,x2,y2))
            self.frontier.add(tmp)
        if self.inside(i, j-1):
            x2,y2 = self.goal_index
            tmp = Node((i, j-1), node, "left", self.countHx(i,j-1,x2,y2))
            self.frontier.add(tmp)

        searched_node = self.frontier.remove(self.explored)
        
        if searched_node is not None:
            self.search(searched_node)

if __name__ == "__main__":
    
    greedyBestFS = GreedyBestFS()

    greedyBestFS.search(greedyBestFS.start_node)
    greedyBestFS.print_map(show_explored = True)
    print(greedyBestFS.minimum_steps)
    print(len(greedyBestFS.explored))
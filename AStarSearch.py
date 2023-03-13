from source import Environment
import math

class Node():
    def __init__(self, coord: tuple, parent, action: int, hx: float, gx: int):
        self.coord = coord
        self.parent = parent
        self.action = action
        self.hx = hx
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
            f = node.hx + node.gx
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

class AStarSearch():
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
        self.start_node = Node(self.start_index, None, None, self.countHx(x1,x2,y1,y2), 0)

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

    def countHx(self, x1,x2,y1,y2):
        d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return d

    def search(self, node: Node):
        self.explored.append(node.coord)
        
        if node.coord == self.goal_index:
            self.minimum_steps = node.gx
            return

        i, j = node.coord
        if self.map[i][j] != self.start:
            self.map[i][j] = self.searched

        if self.inside(i-1, j):
            x2,y2 = self.goal_index
            tmp = Node((i-1, j), node, "up", self.countHx(i-1,j,x2,y2), node.gx + 1)
            self.frontier.add(tmp)
        if self.inside(i, j+1):
            x2,y2 = self.goal_index
            tmp = Node((i, j+1), node, "right", self.countHx(i,j+1,x2,y2), node.gx + 1)
            self.frontier.add(tmp)
        if self.inside(i+1, j):
            x2,y2 = self.goal_index
            tmp = Node((i+1, j), node, "down", self.countHx(i+1,j,x2,y2), node.gx + 1)
            self.frontier.add(tmp)
        if self.inside(i, j-1):
            x2,y2 = self.goal_index
            tmp = Node((i, j-1), node, "left", self.countHx(i,j-1,x2,y2), node.gx + 1)
            self.frontier.add(tmp)
        
        searched_node = self.frontier.remove(self.explored)
        
        if searched_node is not None:
            self.search(searched_node)

if __name__ == "__main__":
    
    aStarSearch = AStarSearch()

    aStarSearch.search(aStarSearch.start_node)
    aStarSearch.print_map(show_explored = True)
    print(aStarSearch.minimum_steps)
    # count=0
    # for row in aStarSearch.map:
    #     for c in row:
    #         if c == 1:
    #             count +=1
    # print(count)
    print(len(aStarSearch.explored))
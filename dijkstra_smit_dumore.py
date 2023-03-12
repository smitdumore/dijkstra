import heapq
import sys
import numpy as np
import cv2
import time
import math
sys.setrecursionlimit(100000)


tab_height = 250
tab_width = 600

def wall(x,y,clearance):
    if ((x >= (tab_width - clearance)) or (y >= (tab_height - clearance)) or (x <= clearance) or (y <= clearance)):
        return True, x,y
    return False, None

def rect_bottom(x,y,clearance):
    if ((y >= 0) and (x <= (tab_height - 100 + clearance)) and (x >= (100 - clearance)) and (y <= (100 + clearance))):
        return True, x,y
    return False, None

def rect_top(x,y,clearance):
    if (y <= tab_height) and (x >= (100 - clearance)) and (y >= (tab_height - 100 - clearance)) and (x <= (tab_height - 100 + clearance)): 
        return True, x,y
    return False, None

def hexagon(x,y, clearance):
    # inequalities equation of hexagon edges 
    # ratio of the radius of a circumscribed circle to the length of the side of a regular hexagon
    a = 1 / math.sqrt(3) 

    if( (y <= (-a*x + clearance + 37321/100)) and \
        (y >= (a*x - clearance - 12321/100)) and \
        (y >= (-a*x - clearance + 22321/100)) and \
        (y <= (a*x + clearance + 2679/100)) and \
        (x <= (clearance + 7299/20)) and \
        (x >= (- clearance + 235))) :
        
            return True, x,y
    return False, None
        
def triangle(x,y,clearance):
    # slope of isoceles edges
    m = math.tan(1.107)

    if  (x >= (2*230 - clearance)) and\
        (y <= (-m*x + clearance + 1145)) and \
        (y >= (m*x - clearance - 895)):
            return True, x,y
    return False, None

def get_inquality_obstacles(clearance):
    
    obstacle_xy_list = []

    for x in range(tab_width + 1):
        for y in range(tab_height + 1):
            
            if(wall(x,y, clearance)[0]):
                obstacle_xy_list.append((x,y))
            elif (rect_top(x,y, clearance)[0]):
                obstacle_xy_list.append((x,y))
            elif (rect_bottom(x,y,clearance)[0]):
                obstacle_xy_list.append((x,y))
            elif (hexagon(x,y,clearance)[0]):
                obstacle_xy_list.append((x,y))
            elif (triangle(x,y,clearance)[0]):
                obstacle_xy_list.append((x,y))

    return obstacle_xy_list

class Dijkstra:
    def __init__(self, start, goal, obstacles):
        self.start = start
        self.goal = goal
        self.obstacles = obstacles
        
        self.heap = []
        self.came_from = {}
        self.cost_so_far = {}
        self.visited = []
        
    def search(self):

        heapq.heappush(self.heap, (0, self.start))
        self.came_from[self.start] = None
        self.cost_so_far[self.start] = 0

        while self.heap:
            current = heapq.heappop(self.heap)[1]

            print("searching", current)

            self.visited.append(current)

            if current == self.goal:
                print("Goal found")
                self.backtrack()
                break

            for next in self.neighbors(current):

                if next[0] in self.visited:
                    continue
                
                edge_cost = next[1]
                new_cost = self.cost_so_far[current] + edge_cost

                if next[0] not in self.cost_so_far or new_cost < self.cost_so_far[next[0]]:         
                    self.cost_so_far[next[0]] = new_cost
                    priority = new_cost
                    heapq.heappush(self.heap, (priority, next[0]))
                    self.came_from[next[0]] = current

        return
        
    
    def backtrack(self):
        path = []
        current = self.goal
        while current != self.start:
            path.append(current)
            current = self.came_from[current]
        path.append(self.start)
        path.reverse()

        visualise(self.obstacles, self.visited, path)
        return path
    
    def neighbors(self, coord):
        sucessors = []
        sucessors.append(self.move_north(coord))
        sucessors.append(self.move_south(coord))
        sucessors.append(self.move_east(coord))
        sucessors.append(self.move_west(coord))
        sucessors.append(self.move_northeast(coord))
        sucessors.append(self.move_southeast(coord))
        sucessors.append(self.move_northwest(coord))
        sucessors.append(self.move_southwest(coord))
        
        valid_sucessors = []
        for n in sucessors:
            if n[0] not in self.obstacles and\
                    0 <= n[0][0] and n[0][0] < tab_width and\
                            0 <= n[0][1] and n[0][1] < tab_height:
                
                valid_sucessors.append(n)

        return valid_sucessors
    
    def move_north(self, coord):
        x, y = coord
        neighbor = (x, y - 1)
        cost = 1 
        return neighbor, cost 

    def move_south(self, coord):
        x, y = coord
        neighbor = (x, y + 1)
        cost = 1 
        return neighbor, cost

    def move_east(self, coord):
        x, y = coord
        neighbor = (x + 1, y)
        cost = 1 
        return neighbor, cost

    def move_west(self, coord):
        x, y = coord
        neighbor = (x - 1, y)
        cost = 1 
        return neighbor, cost

    def move_northeast(self, coord):
        x, y = coord
        neighbor = (x + 1, y - 1)
        cost = 1.4
        return neighbor, cost

    def move_southeast(self, coord):
        x, y = coord
        neighbor = (x + 1, y + 1)
        cost = 1.4
        return neighbor, cost

    def move_northwest(self, coord):
        x, y = coord
        neighbor = (x - 1, y - 1)
        cost = 1.4
        return neighbor, cost

    def move_southwest(self, coord):
        x, y = coord
        neighbor = (x - 1, y + 1)
        cost = 1.4 
        return neighbor, cost



def visualise(obstacle_points, visited, path):
    
    White = (255, 255, 255)
    Blue = (255, 0, 0)
    Green = (0, 255, 0)
    Red = (0, 0, 255)

    # Create a black background image
    img = np.zeros((tab_height, tab_width, 3), np.uint8)

    # Visualise padded obstacles
    obstacle_points = get_inquality_obstacles(5)
    for point in obstacle_points:
        cv2.rectangle(img, (point[0], point[1]), (point[0]+1, point[1]+1), White, -1)
    
    # Visualise original obstacles
    obstacle_points = get_inquality_obstacles(0)
    for point in obstacle_points:
        cv2.rectangle(img, (point[0], point[1]), (point[0]+1, point[1]+1), Blue, -1)

    # Visited
    for point in visited:
        cv2.rectangle(img, (point[0], point[1]), (point[0]+1, point[1]+1), Green, -1)
        cv2.imshow("Dijkstra", img)
        cv2.waitKey(1)

    # Path
    for point in path:
        cv2.rectangle(img, (point[0], point[1]), (point[0]+1, point[1]+1), Red, -1)
        cv2.imshow("Dijkstra", img)
        cv2.waitKey(1)
    
    #cv2.destroyAllWindows()
    time.sleep(5)
    cv2.waitKey(100)


def main():

    # Generate obstacles with clearance of '5'
    occupied = get_inquality_obstacles(5)

    # Get start pos from user
    start_x = int(input("Enter start x coordinate: "))
    start_y = int(input("Enter start y coordinate: "))
    # Change origin
    start_y = tab_height - start_y
    start = (start_x, start_y)
    
    if start in occupied:
        print("start position occupied. Please enter a valid position and run code again.")
        return
    elif 0 < start[0] and start[0] >= tab_width and 0 < start[1] and start[1] >= tab_height:
        print("start position out of bounds. Please enter a valid position and run code again.")
        return
        
    # get goal pos from user
    goal_x = int(input("Enter goal x coordinate: "))
    goal_y = int(input("Enter goal y coordinate: "))
    # Change origin
    goal_y = tab_height - goal_y
    goal = (goal_x, goal_y)

    if goal in occupied:
        print("goal position occupied. Please enter a valid position and run code again.")
        return
    elif 0 < goal[0] and goal[0] >= tab_width and 0 < goal[1] and goal[1] >= tab_height:
        print("goal position out of bounds. Please enter a valid position and run code again.")
            
            
    ############
    # Dijkstra #
    ############
    obj = Dijkstra(start, goal, occupied)
    obj.search()
    print("---program ended---")

if __name__ == "__main__":
    main()
    
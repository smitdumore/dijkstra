import heapq
import sys
import math
import pygame
import numpy as np
sys.setrecursionlimit(100000)

clearance = 5
k=2
tab_height = 250
tab_width = 600


def obstacle_space(x,y):

    c = 0

    # square
    y_c = 50
    x_c = 150
    s = 50

    # circle
    x_circ = 30
    y_circ = 30
    r_circ = 10
    
    # rhombus
    x2_c, y2_c = 470, 70 
    s2 = 10

    # rhombus
    #if abs(x - x2_c) / s2 + abs(y - y2_c) / s2 <= 1:
        #c=1
    
    # circle
    if ((x-math.ceil(x_circ))**2+math.ceil(y -(y_circ))**2-math.ceil(r_circ)**2)<=0:
        c=1
    
    # square
    if(y <= y_c + s/2 and y >= y_c - s/2 and x <= x_c + s/2 and x >= x_c - s/2):
        c = 1

    return c

def obs():
    obs_space = []
    for i in range(0,tab_height):
        for j in range(0,tab_width):
            q = obstacle_space(i,j)
            if q == 1:
                obs_space.append(tuple((i,j)))
    return obs_space


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

        self.vis(path, self.visited)
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
            if obstacle_space(n[0][0], n[0][1]) == 0 and\
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
    
    def vis(self, path, visited):
        
        pygame.init()

        #Defining the colors
        Black = [0, 0, 0]
        red = [255, 0, 0]
        Blue = [0, 100, 255]
        White = [255, 255, 255]

        #Height and Width of Display
        SIZE = [600,250]
        window = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("OUTPUT")
        surface = pygame.Surface(SIZE)
        
        clock = pygame.time.Clock()

        surface.fill(Black)

        #print("size --------------------------", len(occupied))
        #Printing the obstacles
       # my_list = np.array(visited)
       # visited = my_list*k
       # my_list1 = np.array(path)
       # path = my_list1*k

        #my_list2 = np.array(occupied)
        #occupied = my_list2*k
        

            #Printing the visited nodes
        for i in visited:
            pygame.draw.rect(surface, White, [i[0], tab_height - i[1],k,k])
            window.blit(surface,(0,0))
            pygame.display.update()
        #pygame.display.flip()

            #Printing the path
        for j in path:
            pygame.draw.rect(surface, red, [j[0], tab_height - j[1], k,k])
            window.blit(surface,(0,0))
            pygame.display.update()
        #pygame.display.flip()

        # for i in occupied:
        #     pygame.draw.rect(surface, Blue, [i[0],tab_height - i[1],k,k])
        #     #pygame.draw.rect(surface, Blue, [150,150,50,50])
        #     window.blit(surface,(0,0))
        #     pygame.display.update()
        #pygame.display.flip()

        window.blit(surface,(0,0))

        done = False
        while not done:
            for event in pygame.event.get():   
                if event.type == pygame.QUIT:  
                    done = True   

            pygame.display.flip()
            clock.tick(20)

        pygame.quit()






def main():

    #generate obstacles
    occupied = obs()

    # get start pos from user
    start_x = int(input("Enter start x coordinate: "))
    start_y = int(input("Enter start y coordinate: "))
    start = (start_x, start_y)
    
    if obstacle_space(start[0], start[1]) == 1:
        print("start position occupied. Please enter a valid position and run code again.")
        return
    elif 0 < start[0] and start[0] >= 600 and 0 < start[1] and start[1] >= 250:
        print("start position out of bounds. Please enter a valid position and run code again.")
        return
        
    # get goal pos from user
    goal_x = int(input("Enter goal x coordinate: "))
    goal_y = int(input("Enter goal y coordinate: "))
    goal = (goal_x, goal_y)

    if obstacle_space(goal[0], goal[1]) == 1:
        print("goal position occupied. Please enter a valid position and run code again.")
        return
    elif 0 < goal[0] and goal[0] >= 600 and 0 < goal[1] and goal[1] >= 250:
        print("goal position out of bounds. Please enter a valid position and run code again.")
            
            
    ############
    # Dijkstra #
    ############
    obj = Dijkstra(start, goal, occupied)
    obj.search()
    print("---program ended---")

if __name__ == "__main__":
    main()
    
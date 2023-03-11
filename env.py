#!/usr/bin/python3
import pygame

def create_map():
    
    pygame.init()

    # tab dimensions
    TAB_WIDTH = 600
    TAB_HEIGHT = 250

    # Create the Pygame window
    window = pygame.display.set_mode((TAB_WIDTH, TAB_HEIGHT))
    pygame.display.set_caption("Map")

    # Define the colors
    BACKGROUND_COLOR = pygame.Color("red")
    OBSTACLE_COLOR = pygame.Color("black")
    CLEARANCE_COLOR = pygame.Color("white")

    # Create the surface for the obstacle course
    surface = pygame.Surface((TAB_WIDTH, TAB_HEIGHT))
    # Fill the surface with the background color
    surface.fill(BACKGROUND_COLOR)

    obstacles = []
    obstacles.append(pygame.draw.rect(surface,CLEARANCE_COLOR,(30-5,TAB_HEIGHT-50-175-5,170+10,170+10)))
    obstacles.append(pygame.draw.circle(surface,CLEARANCE_COLOR,(260,TAB_HEIGHT-60),55))
    obstacles.append(pygame.draw.rect(surface,CLEARANCE_COLOR,(260-5,TAB_HEIGHT-140-70-5,190+10,70+10)))
    obstacles.append(pygame.draw.rect(surface,CLEARANCE_COLOR,(470-5,TAB_HEIGHT-30-200-5,70+10,200+10)))

    # Draw the obstacles on the surface
    obstacles.append(pygame.draw.rect(surface, OBSTACLE_COLOR, (30, TAB_HEIGHT-50-170 ,170 ,170)))  #x-coordinate, y-coordinate,width and height
    obstacles.append(pygame.draw.circle(surface, OBSTACLE_COLOR, (260,TAB_HEIGHT-60),50))
    obstacles.append(pygame.draw.rect(surface, OBSTACLE_COLOR, (260,TAB_HEIGHT-140-70,190,70)))
    obstacles.append(pygame.draw.rect(surface, OBSTACLE_COLOR, (470,TAB_HEIGHT-30-200 ,70 ,200))) 

    # Blit the surface onto the Pygame window
    window.blit(surface, (0, 0))

    obstacle_space = []

    for obstacle in obstacles:
         for x in range(obstacle.left, obstacle.right):
             for y in range(obstacle.bottom, obstacle.top, -1):  # reverse y-coordinate to start from bottom left
                obstacle_space.append((x, y))
    
    for x in range(0,TAB_WIDTH):
        for y in range(0, TAB_HEIGHT):
            if(x>=25 and x<=205 and y>= 45 and y<=225):
                obstacle_space.append([x,TAB_HEIGHT-y])  # reverse y-coordinate to start from bottom left
            elif(((x-260)**2 + (y-60)**2) <= 55**2):
                obstacle_space.append([x,TAB_HEIGHT-y])  # reverse y-coordinate to start from bottom left
            elif(x>=255 and x<=455 and y>=135 and y<=215):
                obstacle_space.append([x,TAB_HEIGHT-y])  # reverse y-coordinate to start from bottom left
            elif(x>=465 and x<=545 and y>=25 and y<=235):
                obstacle_space.append([x,TAB_HEIGHT-y])  # reverse y-coordinate to start from bottom left
    
    pygame.quit()
    return obstacle_space 


if __name__ == "__main__":
    map = create_map()

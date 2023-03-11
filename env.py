#!/usr/bin/python3
import pygame

def create_map():
    
    pygame.init()

    
    map_width = 600
    map_height = 250
   
    window = pygame.display.set_mode((map_width, map_height))
    pygame.display.set_caption("Map")

    bg_color = pygame.Color("black")
    obs_color = pygame.Color("red")
    padding_color = pygame.Color("white")

    # Create the surface for the obstacle course
    surface = pygame.Surface((map_width, map_height))
    surface.fill(bg_color)

    rect_x, rect_y, rect_width, rect_height = 30, 50, 170, 170
    circle_x, circle_y, circle_radius = 260, 60, 55
    rect2_x, rect2_y, rect2_width, rect2_height = 260, 140, 190, 70
    rect3_x, rect3_y, rect3_width, rect3_height = 470, 30, 70, 200
    clearance = 10

    obstacles = []

    # Add obstacles to the list
    obstacles.append(pygame.draw.rect(surface, padding_color, (rect_x-clearance, rect_y-clearance, rect_width+2*clearance, rect_height+2*clearance)))
    obstacles.append(pygame.draw.circle(surface, padding_color, (circle_x, circle_y), circle_radius+clearance))
    obstacles.append(pygame.draw.rect(surface, padding_color, (rect2_x-clearance, rect2_y-clearance, rect2_width+2*clearance, rect2_height+2*clearance)))
    obstacles.append(pygame.draw.rect(surface, padding_color, (rect3_x-clearance, rect3_y-clearance, rect3_width+2*clearance, rect3_height+2*clearance)))

    # Draw the obstacles on the surface
    obstacles.append(pygame.draw.rect(surface, obs_color, (rect_x, rect_y, rect_width, rect_height)))
    obstacles.append(pygame.draw.circle(surface, obs_color, (circle_x, circle_y), circle_radius))
    obstacles.append(pygame.draw.rect(surface, obs_color, (rect2_x, rect2_y, rect2_width, rect2_height)))
    obstacles.append(pygame.draw.rect(surface, obs_color, (rect3_x, rect3_y, rect3_width, rect3_height)))

    # Blit the surface onto the Pygame window
    window.blit(surface, (0, 0))

    obstacle_space = []

    for obstacle in obstacles:
         for x in range(obstacle.left, obstacle.right):
             for y in range(obstacle.bottom, obstacle.top, -1):
                obstacle_space.append((x, y))
    
    # Check for collision with obstacles
    for x in range(0,map_width):
        for y in range(0, map_height):
            if x >= rect_x-clearance and x <= rect_x+rect_width+clearance and y >= rect_y-clearance and y <= rect_y+rect_height+clearance:
                obstacle_space.append([x,map_height-y])
            elif (x - circle_x)**2 + (y - circle_y)**2 <= (circle_radius+clearance)**2:
                obstacle_space.append([x,map_height-y])
            elif x >= rect2_x-clearance and x <= rect2_x+rect2_width+clearance and y >= rect2_y-clearance and y <= rect2_y+rect2_height+clearance:
                obstacle_space.append([x,map_height-y])
            elif x >= rect3_x-clearance and x <= rect3_x+rect3_width+clearance and y >= rect3_y-clearance and y <= rect3_y+rect3_height+clearance:
                obstacle_space.append([x,map_height-y])


    pygame.quit()
    return obstacle_space 


if __name__ == "__main__":
    map = create_map()

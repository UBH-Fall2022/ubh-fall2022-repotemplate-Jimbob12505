import pygame
import sys
import math
import pygame_gui
from button import Button

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

colours = {
    'white': (255,255,255),
    'black': (0,0,0),
    'yellow': (255, 255, 0),
    'blue': (100,149,237),
    'red': (188, 39, 50),
    'grey': (80, 78, 81),
}

pygame.init()


font = pygame.font.SysFont('comicsans', 16)

width = 1080
height = 800

window = pygame.display.set_mode((width,height))

pygame.display.set_caption('Main')

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


class Planets:
    au = 149.6e6 * 1000 # astronomical unit
    G = 6.67428e-11 # Gravitational Constant
    scale = 250 / au # 1 astronomical unit is 100 pixels
    time_interval = 3600 * 24# Num of seconds in an earth day

    def __init__(self, x,y, radius, colour, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.velocity_x = 0
        self.velocity_y = 0
    
    def draw(self, window):
        x = self.x * self.scale + width/2
        y = self.y * self.scale + height/2 

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x,y = point
                x = x * self.scale + width/2
                y = y * self.scale + height/2
                updated_points.append((x,y))
            pygame.draw.lines(window, self.colour, False, updated_points, 2)

        pygame.draw.circle(window, self.colour, (x,y), self.radius)

        if not self.sun:
            distance_text = font.render(f'{round(self.distance_to_sun/1000, 1)}km', 1, colours['white']) 
            window.blit(distance_text, (x - distance_text.get_width()/2,y - distance_text.get_height()/2)) 

    def attract(self, dif):
        dif_x, dif_y = dif.x, dif.y
        distance_x = dif_x - self.x
        distance_y = dif_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if dif.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * dif.mass / distance**2 # F = G m1m2/r^2 formula

        angle = math.atan2(distance_y, distance_x)
        force_x = math.cos(angle) * force
        force_y = math.sin(angle) * force
        return force_x, force_y
    
    def update_position(self, planets):
        t_force_x = t_force_y = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attract(planet)
            t_force_x += fx
            t_force_y += fy
        
        self.velocity_x += t_force_x / self.mass * self.time_interval # F = ma
        self.velocity_y += t_force_y / self.mass * self.time_interval

        self.x += self.velocity_x * self.time_interval
        self.y += self.velocity_y * self.time_interval
        self.orbit.append((self.x, self.y))


def main():
    run = True
    cap = pygame.time.Clock()

    sun = Planets(0,0, 30, colours['yellow'],1.98892*10**30)
    sun.sun = True

    mercury = Planets(0.387*Planets.au, 0, 8, colours['grey'], 3.30*10**23)
    mercury.velocity_y = -47.5 * 1000

    venus = Planets(0.723*Planets.au, 0, 14, colours['white'], 4.8685*10**24)
    venus.velocity_y = -35.02 * 1000

    earth = Planets(-1*Planets.au, 0,16, colours['blue'], 5.9742*10**24)

    earth.velocity_y  = 29.783 * 1000

    mars = Planets(-1.524 * Planets.au, 0, 12, colours['red'], 6.39 * 10**23)

    mars.velocity_y = 24.077 * 1000

    planets = [sun, mercury, venus, earth, mars]
 
    while run: 

        cap.tick(60) # max fps of 60
        window.fill(colours['black'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(window)

        pygame.display.update()
    pygame.quit()


def custom():


    run = True
    cap = pygame.time.Clock()

    temp = []

    sun = Planets(0,0, 30, colours['yellow'],1.98892*10**30)
    sun.sun = True

    planets = [sun]
    
    num_planets = input('Enter number of planets (1 to 5): ' + bcolors.WARNING+ 'NOTE: I was hoping to finish this function by submission date but currently it only works with one planet. You can still try inputing 1 and seeing the orbit of that planet. ' + bcolors.ENDC + ' : ' )
    i = 0

    while i < int(num_planets):

        radius = input('Enter the radius of planet ' + str(i+1) + ': ')
        mass = input('Enter the mass of planet ' + str(i+1) + ': ')
        yvelocity = input('Enter the velocity in the y direction of planet ' + str(i+1) + bcolors.WARNING + '. Enter a number between 1 and 50; value will be multiplied by a 1000' + bcolors.ENDC + ' : ')

        radius = float(radius)
        mass = float(mass)
        yvelocity = float(yvelocity)

        planet_info = {
            'radius': float(radius),
            'mass': float(mass),
            'y_velocity': float(yvelocity)
        }

        temp.append(planet_info)
        i+=1 
    
    for dict in temp:
        planet = Planets(0.387*Planets.au, 0, radius, colours['white'], mass)
        planet.velocity_y = yvelocity * 1000
        planets.append(planet)

    while run: 

        cap.tick(60) # max fps of 60
        window.fill(colours['black'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(window)

        pygame.display.update()
    pygame.quit()

def main_menu():
    while True:
        window.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(800, 800))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="DEFAULT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="CUSTOM", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    custom()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
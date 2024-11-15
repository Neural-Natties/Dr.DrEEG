import pygame
from time import sleep

# Macros
screen_width = 600
screen_height = 400
segment_color = pygame.Color("red")
segment_width = 20
segment_height = 50

# Classes
class Segment:

    # Initialize segment object
    def __init__(self, surface, color, pivot, next=None):
        
        # Set attributes
        self.next = next
        self.surface = surface
        self.angle = 0

        # Compute starting points
        self.pivot_x, self.pivot_y = pivot
        left = self.pivot_x - (0.5 * segment_width)
        top = self.pivot_y - segment_height

        # Draw object
        self.rect = (left, top, segment_width, segment_height)
        pygame.draw.rect(surface, color, self.rect)

    # Update position
    def update(self):

        # Get mouse position
        x, y = pygame.mouse.get_pos()

        if self.rect.x != x:




class Game:

    # Initialize game object
    def __init__(self, surface):
        self.surface = surface
        self.bg_color = pygame.Color("black")
        self.fps = 60
        self.game_clock = pygame.time.Clock()
        self.shutdown = False
        segment = Segment(surface, segment_color, (screen_width // 2, screen_height))
        pygame.display.update()

    def run(self):
        # Game loop
        while not self.shutdown:
            self.handle_events()
            self.draw()

    def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT or event.type == pygame.KEYUP:
            self.shutdown = True 

    def draw(self):
        # Re-draw all elements

        # Clear display
        self.surface.fill(self.bg_color)


# Functions
def main():

    # Set up pygame
    pygame.init()
    surface = pygame.display.set_mode((screen_width, screen_height))

    # Create game object
    game = Game(surface)

    # Run game
    game.run()

    # Sleep and end
    pygame.quit()

main()
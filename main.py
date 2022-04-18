import pygame
import multiprocessing

pygame.init()

SIZE = WIDTH, HEIGHT = 750, 750
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2

class Entity:
    def __init__(self):
        self.surface = pygame.Surface((50, 50))
        self.surface.fill('white')
        self.rect = self.surface.get_rect(center=(100, 100))

    def update(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.rect.move_ip(0, -1)
        if key[pygame.K_s]:
            self.rect.move_ip(0, 1)
        if key[pygame.K_a]:
            self.rect.move_ip(-1, 0)
        if key[pygame.K_d]:
            self.rect.move_ip(1, 0)

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

class Screen:
    def __init__(self, index, position, color):
        self.index = index
        self.color = color
        self.surface = pygame.Surface((HALF_WIDTH, HALF_HEIGHT))
        self.surface.fill(color)
        self.rect = self.surface.get_rect(topleft=position)

        self._selected = False

    @property
    def selected(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self):
        self.surface.fill(self.color)
        if self.selected:
            rect = self.surface.get_rect()
            pygame.draw.rect(self.surface, 'white', rect, 10)

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


def draw_to_all_screens(window, screens, objects):
    window.fill('black')
    for screen in screens:
        screen.update()
        if screen.selected:
            for obj in objects:
                obj.update()
                obj.draw(screen.surface)
        screen.draw(window)

def main():
    window = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    player = Entity()

    screen_one = Screen(0, (0, 0), 'red')
    screen_two = Screen(1, (HALF_WIDTH, 0), 'green')
    screen_three = Screen(0, (0, HALF_HEIGHT), 'yellow')
    screen_four = Screen(0, (HALF_WIDTH, HALF_HEIGHT), 'cyan')

    all_screens = [screen_one, screen_two, screen_three, screen_four]
    all_objects = [player]

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        draw_to_all_screens(window, all_screens, all_objects)
        pygame.display.update()
        pygame.display.set_caption(f"FPS: {clock.get_fps():.0f}")

def do_multiprocessing():
    for _ in range(4):
        multiprocessing.Process(target=main).start()

if __name__ == '__main__':
    #main()
    do_multiprocessing()

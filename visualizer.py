import pygame

class Visualizer():
    WIDTH = 600
    HEIGHT = 800

    def __init__(self, skirace=None):
        pygame.init()
        pygame.display.set_mode((Visualizer.WIDTH, Visualizer.HEIGHT))
        pygame.display.set_caption('RAISR')
        pygame.quit()

if __name__ == '__main__':
    vis = Visualizer()

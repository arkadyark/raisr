import pygame
import os
import time
import random
from skirace import *
from heuristics import *
from search import *
from physics import dt

class Visualizer():
    WIDTH = 600
    HEIGHT = 800

    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE =  (  0,   0, 255)
    GREEN = (  0, 255,   0)
    RED =   (255,   0,   0)
    D_GREEN=( 43, 111,  48)
    BROWN  =( 91,  69,  27)

    SCALE = 17

    TRACE = []

    def __init__(self, skirace=None):
        pygame.init()
        gameDisplay = pygame.display.set_mode((Visualizer.WIDTH, Visualizer.HEIGHT))
        pygame.display.set_caption('RAISR')
        font = pygame.font.SysFont('Sans', 32)

        self.N = 5
        Visualizer.SCALE = self.getScale(skirace) - 1
        self.t = 0

        gameExit = False
        go = False
        (racer_coords, speeds, x_bounds) = self.getRacerCoordsAndXBounds(skirace)
        while not gameExit and len(racer_coords) != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    go = True
            gameDisplay.fill(Visualizer.WHITE)
            self.drawRace(gameDisplay, skirace.all_gates)
            self.drawTrees(gameDisplay, x_bounds)
            if go:
                curr_pos = racer_coords.pop()
                curr_v = speeds.pop()
                self.drawRacer(gameDisplay, curr_pos)
                self.drawTrace(gameDisplay, curr_pos)
                text = font.render("{number:.{digits}f} seconds".format(number=self.t, digits=2), True, Visualizer.RED, Visualizer.WHITE)
                text2 = font.render("{number:.{digits}f} km/h".format(number=curr_v*3.6, digits=2), True, Visualizer.RED, Visualizer.WHITE)
                self.t += round(dt/self.N, 2)
                gameDisplay.blit(text, (0, 0))
                gameDisplay.blit(text2, (0, 32))
                pygame.display.update()
                time.sleep(dt/self.N - 0.011)
            else:
                pygame.display.update()

        time.sleep(5)
        pygame.quit()

    def drawTrees(self, gameDisplay, x_bounds):
        size = 8
        x_left = x_bounds[0]
        x_right = x_bounds[1]
        random.seed(2)
        for x in range(40, 300, 20):
            for y in range(0, Visualizer.HEIGHT, size*3):
                self.drawTree(gameDisplay, [x_left - random.random()*20 - x, y - random.random()*20], size)
                self.drawTree(gameDisplay, [x_right + random.random()*20 + x, y + - random.random()*20], size)

    def drawTree(self, gameDisplay, pos, size):
        pygame.draw.polygon(gameDisplay, Visualizer.D_GREEN, [[pos[0]+size, pos[1]+size], [pos[0]-size, pos[1]+size],[pos[0], pos[1]-size//2]])
        pygame.draw.rect(gameDisplay, Visualizer.BROWN, [pos[0] - (size/4), pos[1]+size, (size/2), size*3 // 4])

    def drawRacer(self, gameDisplay, pos):
        pygame.draw.circle(gameDisplay, Visualizer.BLACK , pos, 5)

    def drawRace(self, gameDisplay, gates):
        COLORS = [Visualizer.RED, Visualizer.BLUE]
        for gate_idx in range(len(gates) - 1):
            gate = [coord * Visualizer.SCALE for coord in list(gates[gate_idx])]
            # xcord centered around center of display
            gate[0] = Visualizer.WIDTH // 2 + gate[0]
            pygame.draw.circle(gameDisplay, COLORS[gate_idx % 2], gate, 3)
        min_x = (min(g[0] for g in gates) - 2.5) * Visualizer.SCALE + Visualizer.WIDTH // 2
        max_x = (max(g[0] for g in gates) + 2) * Visualizer.SCALE + Visualizer.WIDTH // 2
        pygame.draw.line(gameDisplay, Visualizer.RED, (min_x, gates[-1][1] * Visualizer.SCALE), (max_x, gates[-1][1] * Visualizer.SCALE), 5)

    def drawTrace(self, gameDisplay, pos):
        Visualizer.TRACE.append(pos)
        if len(Visualizer.TRACE) >= 2:
            for pt_idx in range(len(Visualizer.TRACE)-1):
                pt1 = Visualizer.TRACE[pt_idx]
                pt2 = Visualizer.TRACE[pt_idx+1]
                pygame.draw.line(gameDisplay, Visualizer.GREEN, pt1, pt2, 1)

    def interpolate(self, n, start, end):
        pts = []
        dist_x = (end[0] - start[0])
        dist_y = (end[1] - start[1])
        for i in range(1, n):
            pts.append( (round(start[0]+i/n*dist_x), round(start[1]+i/n * dist_y)) )
        pts.append(end)
        return pts

    def getScale(self, skirace):
        #start_y = skirace.all_gates[0][1]
        end_y = skirace.all_gates[-1][1]
        return Visualizer.HEIGHT // end_y

    def getRacerCoordsAndXBounds(self, skirace):
        racer_coords = [(round(Visualizer.WIDTH // 2 + skirace.pos[0]*Visualizer.SCALE), round(skirace.pos[1]*Visualizer.SCALE)) ]
        vs = [skirace.v]
        parent = skirace.parent
        x_left_bound = Visualizer.WIDTH // 2
        x_right_bound = Visualizer.WIDTH // 2
        while parent:
            prev_pos = racer_coords[-1]
            next_x = round(Visualizer.WIDTH // 2 + parent.pos[0]* Visualizer.SCALE)
            next_y = round(parent.pos[1]*Visualizer.SCALE)
            next_pos = (next_x, next_y)
            pts = self.interpolate(self.N, prev_pos, next_pos)
            racer_coords += pts
            for i in range(self.N):
                vs.append(parent.v)
            #update bounds
            if next_x < x_left_bound:
                x_left_bound = next_x
            if next_x > x_right_bound:
                x_right_bound = next_x

            parent = parent.parent
        return (racer_coords, vs, (x_left_bound, x_right_bound))

if __name__ == '__main__':
    skirace = set_race(5, ((0, 5), (0, 10), (0, 15), (0, 20), (0, 26), (-8, 32), (-2, 38), (-4, 44), (2, 50)))
    weight = 10
    final = anytime_weighted_astar(skirace, heur_fn=heur_slightly_less_dumb, weight=weight, timebound=1000)
    if final:
        vis = Visualizer(final)

    # TODO: more courses

import pygame
import random
import numpy as np
from shapely.geometry import Polygon, Point

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("레이싱 트랙 유전 알고리즘")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 게임 설정
POPULATION_SIZE = 50
GENE_LENGTH = 300
MUTATION_RATE = 0.01
FPS = 90
TIME_LIMIT = 8  # 8초 제한

# 레이싱 트랙 설정
TRACK_OUTER = [(100, 100), (900, 100), (900, 500), (100, 500)]
TRACK_INNER = [(200, 200), (800, 200), (800, 400), (200, 400)]
START = (150, 300)
FINISH = (850, 300)

track_polygon = Polygon(TRACK_OUTER, [TRACK_INNER])

def random_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

class Car:
    def __init__(self):
        self.x, self.y = START
        self.angle = 0
        self.speed = 0
        self.genes = np.random.uniform(-1, 1, (GENE_LENGTH, 2))  # [steering, acceleration]
        self.fitness = 0
        self.alive = True
        self.color = random_color()
        self.width = 20
        self.height = 10
        self.distance_traveled = 0

    def move(self, step):
        if step < len(self.genes) and self.alive:
            steering, acceleration = self.genes[step]
            self.angle += steering * 0.2
            self.speed += acceleration * 0.5
            self.speed = max(0, min(self.speed, 10))  # 속도 제한 증가

            new_x = self.x + self.speed * np.cos(self.angle)
            new_y = self.y + self.speed * np.sin(self.angle)

            if track_polygon.contains(Point(new_x, new_y)):
                self.distance_traveled += ((new_x - self.x)**2 + (new_y - self.y)**2)**0.5
                self.x, self.y = new_x, new_y
            else:
                self.alive = False

    def draw(self):
        rotated_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(rotated_surface, self.color, (0, 0, self.width, self.height))
        rotated_surface = pygame.transform.rotate(rotated_surface, -np.degrees(self.angle))
        rect = rotated_surface.get_rect(center=(self.x, self.y))
        screen.blit(rotated_surface, rect.topleft)

def create_population():
    return [Car() for _ in range(POPULATION_SIZE)]

def fitness(car):
    distance_to_finish = ((car.x - FINISH[0])**2 + (car.y - FINISH[1])**2)**0.5
    if car.alive:
        # 완주한 경우 추가 보상
        if distance_to_finish < 10:  # 결승선에 매우 가까운 경우
            car.fitness = 10000 + (TIME_LIMIT - car.time) * 100  # 빠른 완주에 대한 보상
        else:
            car.fitness = 1000 - distance_to_finish + 0.25 * car.distance_traveled
    else:
        car.fitness = car.distance_traveled

    # 음수 피트니스 방지
    car.fitness = max(0, car.fitness)

    return car.fitness

def tournament_selection(population, tournament_size=3):
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        selected.append(max(tournament, key=lambda x: x.fitness))
    return selected

def crossover(parent1, parent2):
    child = Car()
    for i in range(GENE_LENGTH):
        if random.random() < 0.5:
            child.genes[i] = parent1.genes[i]
        else:
            child.genes[i] = parent2.genes[i]
    return child

def adaptive_mutation(car, generation):
    mutation_rate = MUTATION_RATE * (1 - generation / 100)  # 세대가 지날수록 돌연변이율 감소
    for gene in car.genes:
        if random.random() < mutation_rate:
            gene[0] += random.uniform(-0.5, 0.5)
            gene[1] += random.uniform(-0.5, 0.5)
            gene[0] = max(-1, min(gene[0], 1))
            gene[1] = max(-1, min(gene[1], 1))

def create_next_generation(population, generation):
    new_population = []
    
    # 적합도에 따라 부모 선택
    selected = tournament_selection(population)
    
    while len(new_population) < POPULATION_SIZE:
        parent1, parent2 = random.sample(selected, 2)
        child = crossover(parent1, parent2)
        adaptive_mutation(child, generation)
        new_population.append(child)
    
    return new_population

def draw_track():
    pygame.draw.polygon(screen, WHITE, TRACK_OUTER)
    pygame.draw.polygon(screen, BLACK, TRACK_INNER)
    pygame.draw.circle(screen, GREEN, START, 10)
    pygame.draw.circle(screen, RED, FINISH, 10)

def main():
    population = create_population()
    generation = 1
    clock = pygame.time.Clock()
    
    running = True
    while running:
        start_time = pygame.time.get_ticks()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(BLACK)
            draw_track()
            
            alive_cars = [car for car in population if car.alive]
            
            if not alive_cars or (pygame.time.get_ticks() - start_time) / 1000 > TIME_LIMIT:
                for car in population:
                    fitness(car)
                population = create_next_generation(population, generation)
                generation += 1
                print(f"Generation: {generation}, Best Fitness: {max(car.fitness for car in population)}")
                break
            
            for car in alive_cars:
                car.move(min((pygame.time.get_ticks() - start_time) // (1000 // FPS), GENE_LENGTH - 1))
                car.draw()
            
            pygame.display.flip()
            clock.tick(FPS)
        
        if generation > 50:
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()

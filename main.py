import pygame
import random
import math
from collections import Counter
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent / "assets"

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rescue the Hostage - Local Search")

# Colors
WHITE = (240, 248, 255)
RED = (255, 69, 0)      # Hostage color
BLUE = (30, 144, 255)   # Player color
LIGHT_GREY = (211, 211, 211) # Background grid color
FLASH_COLOR = (50, 205, 50) # Victory flash color
BUTTON_COLOR = (50, 205, 50) # Button color
BUTTON_TEXT_COLOR = (255, 255, 255) # Button text color

# Load images for player, hostage, and walls
player_image = pygame.image.load(str(ASSETS_DIR / "AI1.png"))
hostage_image = pygame.image.load(str(ASSETS_DIR / "AI2.png"))

wall_images = [
    pygame.image.load(str(ASSETS_DIR / "AI3.png")),
    pygame.image.load(str(ASSETS_DIR / "AI4.png")),
    pygame.image.load(str(ASSETS_DIR / "AI5.png")),
]

# Resize images to fit the grid
wall_images = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in wall_images]
player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))
hostage_image = pygame.transform.scale(hostage_image, (TILE_SIZE, TILE_SIZE))

# Constants for recent positions
MAX_RECENT_POSITIONS = 10
GENERATION_LIMIT = 50
MUTATION_RATE = 0.1

# Function to generate obstacles
def generate_obstacles(num_obstacles):
    obstacles = []
    while len(obstacles) < num_obstacles:
        new_obstacle = [random.randint(0, COLS-1), random.randint(0, ROWS-1)]
        if new_obstacle not in obstacles:  # Make sure obstacles are not overlapping
            obstacles.append(new_obstacle)
    obstacle_images = [random.choice(wall_images) for _ in obstacles]
    return obstacles, obstacle_images

# Function to start a new game
def start_new_game():
    global player_pos, hostage_pos, recent_positions, obstacles, obstacle_images
    obstacles, obstacle_images = generate_obstacles(20)
    recent_positions = []

    # Generate player and hostage positions with a larger distance
    while True:
        player_pos = [random.randint(0, COLS-1), random.randint(0, ROWS-1)]
        hostage_pos = [random.randint(0, COLS-1), random.randint(0, ROWS-1)]
        distance = math.dist(player_pos, hostage_pos)
        if distance > 8 and player_pos not in obstacles and hostage_pos not in obstacles:
            break

# Function to move the player closer to the hostage using Hill Climbing algorithm
def hill_climbing(player, hostage, obstacles):
    global recent_positions

    def calculate_distance(pos):
        return abs(pos[0] - hostage[0]) + abs(pos[1] - hostage[1])
    moves = []
    if(player[0] < COLS - 1):
        moves.append([player[0]+1,player[1]])
    if(player[0] > 0):
        moves.append([player[0]-1,player[1]])
    if(player[1] < ROWS - 1):
        moves.append([player[0], player[1]+1])
    if(player[1] > 0):
        moves.append([player[0], player[1]-1])
    for i in range (len(moves) -1, -1, -1):
        if moves[i] in obstacles:
            moves.remove(moves[i])
            continue

                    

    distance = calculate_distance(player)
    better_move = False
    best_move = moves[0]
    for move in moves:
        move_dist = calculate_distance(move)
        if move_dist < distance and not in_loop(recent_positions, move):
            better_move = True
            distance = move_dist
            best_move = move
    if better_move:
        return best_move
    else:
        return random_move(player, obstacles)

 
temperature = 100  # Initial temperature

# Function for Simulated Annealing
def simulated_annealing(player, hostage, obstacles):
    cooling_rate = 0.99
    global temperature
    
    def acceptance_probability(old_cost, new_cost, temp):
        return math.exp((new_cost - old_cost)/ temp)

    def calculate_distance(pos):
        return abs(pos[0] - hostage[0]) + abs(pos[1] - hostage[1])
    next = random_move(player, obstacles)
    #if (in_loop(recent_positions, next)):
     #   return random_move(player, obstacles)
    temperature *= cooling_rate
    if(calculate_distance(next) - calculate_distance(player) < 0):
        return next
    if(temperature > 1 and acceptance_probability(calculate_distance(player), calculate_distance(next), temperature) > random.random()):
        return next
    else:
        moves = []
        if(player[0] < COLS - 1):
            moves.append([player[0]+1,player[1]])
        if(player[0] > 0):
            moves.append([player[0]-1,player[1]])
        if(player[1] < ROWS - 1):
            moves.append([player[0], player[1]+1])
        if(player[1] > 0):
            moves.append([player[0], player[1]-1])
                    
        for i in range (len(moves) -1, -1, -1):
            if moves[i] in obstacles:
                moves.remove(moves[i])
                continue

        for move in moves:
            if(calculate_distance(move) < calculate_distance(player)):
                return player

            
        return random_move(player, obstacles)





    
generated_path = []
count = 0 
# Function for Genetic Algorithm
def genetic_algorithm(player, hostage, obstacles):
    population_size = 40
    generations = 100
    global MUTATION_RATE
    MUTATION_RATE = 0.1

    # Fitness function
    def fitness(individual):
        """
        counts = Counter(map(tuple, individual))
        repeated = sum(count - 1 for count in counts.values() if count > 1)
        similarity = (repeated / len(individual)) * 100
        return 10000-len(individual)-similarity
        """
        return 1000 - sum(math.dist(coordination, hostage) for coordination in individual)/10

    # Generate random population
    def generate_population():
        population = []
        for i in range (population_size):
            individual = [player]
        
            while(individual[-1] != hostage):
                moves = []
                if(individual[-1][0] < COLS - 1):
                    moves.append([individual[-1][0]+1,individual[-1][1]])
                if(individual[-1][0] > 0):
                    moves.append([individual[-1][0]-1,individual[-1][1]])
                if(individual[-1][1] < ROWS - 1):
                    moves.append([individual[-1][0],individual[-1][1]+1])
                if(individual[-1][1] > 0):
                    moves.append([individual[-1][0], individual[-1][1]-1])
                            
                for i in range (len(moves) -1, -1, -1):
                    if moves[i] in obstacles:
                        moves.remove(moves[i])
                        continue
                not_loop =list(filter((lambda a : not in_loop(individual, a)), moves))
                if len(individual) > 2 and individual[-2] in not_loop:
                    not_loop.remove(individual[-2])
                if not_loop:
                    individual.append(random.choice(not_loop))
                else:
                    individual.append(random.choice(moves))
                
                #individual.append(random.choice(moves))
                """
                if (len(individual)> 10000):
                    individual.clear()
                    individual = [player]
                """
            population.append(individual)
        return population

    # Crossover function
    def crossover(parent1, parent2):
        point1 = 0
        point2 = 0
        for i in parent1[len(parent1)//2:-2]:
            if i in parent2[len(parent1)//2:-2]:
                point1 = parent1.index(i)
                point2 = parent2.index(i)
                return [parent1[:point1]+parent2[point2:], parent2[:point2]+parent1[point1:]]
        
        for i in parent1[1:len(parent1)//2]:
            if i in parent2[1:len(parent1)//2]:
                point1 = parent1.index(i)
                point2 = parent2.index(i)
                return [parent1[:point1]+parent2[point2:], parent2[:point2]+parent1[point1:]]
        MUTATION_RATE = 0.2
        return [parent1,parent2]
                

    # Mutation function

    def mutate(individual):
        point = random.randint(1, len(individual) -1)
        mutated = individual[:point]
        while(mutated[-1] != hostage):
                moves = []
                if(mutated[-1][0] < COLS - 1):
                    moves.append([mutated[-1][0]+1,mutated[-1][1]])
                if(mutated[-1][0] > 0):
                    moves.append([mutated[-1][0]-1,mutated[-1][1]])
                if(mutated[-1][1] < ROWS - 1):
                    moves.append([mutated[-1][0], mutated[-1][1]+1])
                if(mutated[-1][1] > 0):
                    moves.append([mutated[-1][0], mutated[-1][1]-1])
                            
                for i in range (len(moves) -1, -1, -1):
                    if moves[i] in obstacles:
                        moves.remove(moves[i])
                        continue
                not_loop =list(filter((lambda a : not in_loop(mutated, a)), moves))
                if len(mutated) > 2 and mutated[-2] in not_loop:
                    not_loop.remove(mutated[-2])
                if not_loop:
                    mutated.append(random.choice(not_loop))
                else:
                    mutated.append(random.choice(moves))
                """
                if (len(mutated)>10000):
                    mutated.clear()
                    mutated = individual[:point]
                """
        return mutated
    

    global generated_path
    global count
    if generated_path:
        count+=1
        return generated_path[count]

    population = generate_population()
    weights = [fitness(i) for i in population]
    generation_count= 1

    while(generation_count<generations):
        MUTATION_RATE = 0.1
        parents = random.choices(population, weights,k =population_size)
        children = []
        
        for i in range(population_size // 2):
            children.extend(crossover(parents[i], parents[i+1]))

        similar = 0 
        for i in range(len(children)):
            for j in range(0,i):
                if i!= j and children[i] == children[j]  and len(children[i]) > math.dist(player, hostage) * 5:
                    similar += 1

        if similar > population_size/4: 
            MUTATION_RATE = 0.4

        
        for j in range(math.floor(MUTATION_RATE * population_size)):
            r=random.randint(0, len(children) - 1)
            children[r] = mutate(children[r])
        
        population = children
        
        weights = [fitness(i) for i in population]
        generation_count+=1
    population.sort(key = fitness, reverse=True)
    generated_path = population[0]
    return population[0][0]
        
            
    

#Objective: Check if the player is stuck in a repeating loop.
def in_loop(recent_positions, player):
    if(len(recent_positions) > 20):
        return recent_positions.count(player) > 2
    return recent_positions.count(player) > 1

#Objective: Make a random safe move to escape loops or being stuck.
def random_move(player, obstacles):
    moves = []
    if(player[0] < COLS - 1):
        moves.append([player[0]+1,player[1]])
    if(player[0] > 0):
        moves.append([player[0]-1,player[1]])
    if(player[1] < ROWS - 1):
        moves.append([player[0], player[1]+1])
    if(player[1] > 0):
        moves.append([player[0], player[1]-1])
        
    for i in range (len(moves) -1, -1, -1):
        if moves[i] in obstacles:
            moves.remove(moves[i])
            continue
    return random.choice(moves)

#Objective: Update the list of recent positions. 
def store_recent_position(recent_positions, new_player_pos, max_positions=MAX_RECENT_POSITIONS):
    if (new_player_pos == player_pos):
        return
    if(len(recent_positions) == max_positions):
        recent_positions.remove(recent_positions[0])
    recent_positions.append(new_player_pos)

# Function to show victory flash
def victory_flash():
    for _ in range(5):
        screen.fill(FLASH_COLOR)
        pygame.display.flip()
        pygame.time.delay(100)
        screen.fill(WHITE)
        pygame.display.flip()
        pygame.time.delay(100)

# Function to show a button and wait for player's input
def show_button_and_wait(message, button_rect):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, BUTTON_TEXT_COLOR)
    button_rect.width = text.get_width() + 20
    button_rect.height = text.get_height() + 10
    button_rect.center = (WIDTH // 2, HEIGHT // 2)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    screen.blit(text, (button_rect.x + (button_rect.width - text.get_width()) // 2,
                       button_rect.y + (button_rect.height - text.get_height()) // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

# Function to get the algorithm choice from the player
def get_algorithm_choice():
    print("Choose an algorithm:")
    print("1: Hill Climbing")
    print("2: Simulated Annealing")
    print("3: Genetic Algorithm")

    while True:
        choice = input("Enter the number of the algorithm you want to use (1/2/3): ")
        if choice == "1":
            return hill_climbing
        elif choice == "2":
            return simulated_annealing
        elif choice == "3":
            return genetic_algorithm
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

# Main game loop
running = True
clock = pygame.time.Clock()
start_new_game()
button_rect = pygame.Rect(0, 0, 0, 0)

# Get the algorithm choice from the player
chosen_algorithm = get_algorithm_choice()
m =0
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Perform the chosen algorithm step
    new_player_pos = chosen_algorithm(player_pos, hostage_pos, obstacles)
    m += 1

    if chosen_algorithm != genetic_algorithm:
        # Check for stuck situations
        if new_player_pos == player_pos or in_loop(recent_positions, new_player_pos):
            # Perform a random move when stuck
            new_player_pos = random_move(player_pos, obstacles)

    # Update recent positions
    store_recent_position(recent_positions, new_player_pos)
    # Update player's position
    player_pos = new_player_pos

    # Draw the grid background
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, LIGHT_GREY, rect, 1)

    # Draw obstacles
    for idx, obs in enumerate(obstacles):
        obs_rect = pygame.Rect(obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(obstacle_images[idx], obs_rect)

    # Draw player
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(player_image, player_rect)

    # Draw hostage
    hostage_rect = pygame.Rect(hostage_pos[0] * TILE_SIZE, hostage_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(hostage_image, hostage_rect)

    # Check if player reached the hostage
    if player_pos == hostage_pos:
        print("Hostage Rescued!")
        #print(m)
        victory_flash()  # Show the victory flash
        show_button_and_wait("New Game", button_rect)
        m = 0
        temperature = 100
        generated_path =[]
        count = 0
        start_new_game()

    # Update the display
    pygame.display.flip()
    clock.tick(10)  # Lower frame rate for smoother performance

pygame.quit()

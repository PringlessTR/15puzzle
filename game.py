import pygame
import random
import time
import math

pygame.init()

WIDTH, HEIGHT = 400, 500 
TILE_SIZE = 100 
ANIMATION_SPEED = 20 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("15 Puzzle Game")

# Colors
BACKGROUND_COLOR = (50, 50, 50)
TILE_COLOR = (255, 165, 0)
TILE_BORDER_COLOR = (255, 140, 0)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (34, 139, 34)
BUTTON_TEXT_COLOR = (255, 255, 255)

font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 36)

start_time = None
end_time = None

fireworks_particles = []

def is_solvable(sequence):
    one_d_list = [x for x in sequence if x != 0]
    inversions = 0
    for i in range(len(one_d_list)):
        for j in range(i+1, len(one_d_list)):
            if one_d_list[i] > one_d_list[j]:
                inversions += 1
    grid_2d = [sequence[i:i+4] for i in range(0, 16, 4)]
    for row in range(4):
        for col in range(4):
            if grid_2d[row][col] == 0:
                blank_row_from_bottom = 4 - row
                break
    if (blank_row_from_bottom % 2 == 0 and inversions % 2 == 1) or (blank_row_from_bottom % 2 == 1 and inversions % 2 == 0):
        return True
    return False

def create_grid():
    numbers = list(range(1, 16)) + [0]
    random.shuffle(numbers)
    if not is_solvable(numbers):
        non_zero_indices = [i for i, v in enumerate(numbers) if v != 0]
        if len(non_zero_indices) > 1:
            i1, i2 = non_zero_indices[0], non_zero_indices[1]
            numbers[i1], numbers[i2] = numbers[i2], numbers[i1]
    grid = [numbers[i:i + 4] for i in range(0, 16, 4)]
    return grid


grid = create_grid()

def draw_grid(exclude_tile=None):
    for row in range(4):
        for col in range(4):
            number = grid[row][col]
            if (row, col) != exclude_tile:
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if number != 0:
                    pygame.draw.rect(screen, TILE_COLOR, rect, border_radius=10)
                    pygame.draw.rect(screen, TILE_BORDER_COLOR, rect, 5, border_radius=10)
                    text = font.render(str(number), True, TEXT_COLOR)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

def draw_timer():
    if start_time and end_time is None:
        current_time = time.time() - start_time
        timer_text = button_font.render(f"Time: {current_time:.2f}s", True, TEXT_COLOR)
    elif end_time:
        final_time = end_time - start_time
        timer_text = button_font.render(f"Time: {final_time:.2f}s", True, TEXT_COLOR)
    else:
        timer_text = button_font.render("Time: 0.00s", True, TEXT_COLOR)
    screen.blit(timer_text, (WIDTH // 2 - 100, HEIGHT - 100))

def find_empty():
    for row in range(4):
        for col in range(4):
            if grid[row][col] == 0:
                return row, col

def move_tile(start_pos, end_pos):
    start_x, start_y = start_pos[1] * TILE_SIZE, start_pos[0] * TILE_SIZE
    end_x, end_y = end_pos[1] * TILE_SIZE, end_pos[0] * TILE_SIZE
    dx = (end_x - start_x) / ANIMATION_SPEED
    dy = (end_y - start_y) / ANIMATION_SPEED

    x, y = start_x, start_y
    for _ in range(ANIMATION_SPEED):
        x += dx
        y += dy
        screen.fill(BACKGROUND_COLOR)
        draw_grid(exclude_tile=start_pos)
        draw_timer()
        pygame.draw.rect(screen, TILE_COLOR, (x, y, TILE_SIZE, TILE_SIZE), border_radius=10)
        pygame.draw.rect(screen, TILE_BORDER_COLOR, (x, y, TILE_SIZE, TILE_SIZE), 5, border_radius=10)
        number = grid[start_pos[0]][start_pos[1]]
        text = font.render(str(number), True, TEXT_COLOR)
        text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(10)

def swap_tiles(row, col, new_row, new_col):
    move_tile((row, col), (new_row, new_col))
    grid[row][col], grid[new_row][new_col] = grid[new_row][new_col], grid[row][col]

def handle_click(pos):
    global start_time, end_time
    row, col = pos[1] // TILE_SIZE, pos[0] // TILE_SIZE
    empty_row, empty_col = find_empty()
    if (abs(row - empty_row) == 1 and col == empty_col) or (abs(col - empty_col) == 1 and row == empty_row):
        if start_time is None:
            start_time = time.time()
        swap_tiles(row, col, empty_row, empty_col)
        if check_win():
            end_time = time.time()
            fireworks()

def check_win():
    for row in range(4):
        for col in range(4):
            if grid[row][col] != 0 and grid[row][col] != row * 4 + col + 1:
                return False
    return True

def fireworks():
    global fireworks_particles
    fireworks_particles = []  
    for _ in range(5):  
        x, y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
        color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)])
        for _ in range(50):  
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            fireworks_particles.append([x, y, math.cos(angle) * speed, math.sin(angle) * speed, color])

def update_fireworks():
    for particle in fireworks_particles:
        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[2] *= 0.98 
        particle[3] *= 0.98
        pygame.draw.circle(screen, particle[4], (int(particle[0]), int(particle[1])), 3)

# Main game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    draw_timer()
    update_fireworks()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos)

pygame.quit()

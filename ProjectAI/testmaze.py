import random

def move_bot():
    pass

def get_neighbors(cell, D):
    x, y = cell
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    return [(ni, ni) for ni, ni in neighbors if 0 <= ni < D and 0 <= ni < D]


def get_open_neighbors(cell, maze):
    x,y = cell
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    valid_cells = [(nx, ny) for nx,ny in neighbors if 0 <= nx < len(maze) and 0 <= ny < len(maze) and maze[nx][ny] == 0]
    return valid_cells

def get_burning_neighbors(burning_cell, maze, cells_on_fire):
    all_burning_nrighbors = []
    valid_neighbors = get_open_neighbors(burning_cell, maze)
    for cell in valid_neighbors:
        if cell in cells_on_fire:
            all_burning_nrighbors.append(cell)
    return all_burning_nrighbors

def generate_maze(D):
    maze = [[1 for _ in range(D)] for _ in range(D)]

    start_cell = (random.randint(0, D-1), random.randint(0, D-1))
    maze[start_cell[0]][start_cell[1]] = 0

    Fringe_cells = set(get_neighbors(start_cell, D))
    valid_cells = []

    while Fringe_cells:
        potential_cells = [cell for cell in Fringe_cells if maze[cell[0]][cell[1] == 1]]
        for i in potential_cells:
            if sum([1 - maze[nx][ny] for nx, ny in get_neighbors(cell, D)]) == 1:
                valid_cells.append(i)

        if not valid_cells:
            break

        chosen_cell = random.choice(valid_cells)
        maze[chosen_cell[0]][chosen_cell[1]] = 0

        Fringe_cells.remove(chosen_cell)
        Fringe_cells.update(get_neighbors(chosen_cell, D))

    dead_ends = [(row, col) for row in range(D) for col in range(D) if maze[row][col] == 0 and sum([1 - maze[nx][ny] for nx, ny in get_neighbors((row, col), D)]) == 1]

    for dead_end in dead_ends:
        if random.random() > 0.5:
            potential_blocks = [cell for cell in get_neighbors(dead_end, D) if maze[cell[0]][cell[1]] == 1]
            if potential_blocks:
                block_to_open = random.choice(potential_blocks)
                maze[block_to_open[0]][block_to_open[1]] = 0

    return maze



# Example usage
D = 100
maze = generate_maze(D)
for row in maze:
    print(row)


game = True

cells_on_fire = set()
open_cells = []
for i in len(maze):
    for j in len(i):
        if maze[i][j] == 0:
            open_cells.append((i,j))


random_fire_starting_cell = random.randint(0, len(open_cells)-1)
firex,firey = open_cells[random_fire_starting_cell]
cells_on_fire.add(maze[firex][firey])
bot_position = random.choice([cell for cell in open_cells if cell != random_fire_starting_cell])
button_position = random.choice([cell for cell in open_cells if cell not in [random_fire_starting_cell, bot_position]])

q = (.41)

while game:
    bot_position = move_bot(bot_position, "random", maze, cells_on_fire, button_position)

    next_cells_on_fire = set()
    for cell in cells_on_fire:
        all_neighbor_cells = get_open_neighbors(cell)
        for curr_cell in all_neighbor_cells:
            if curr_cell not in cells_on_fire:
                neighbors_on_fire = get_burning_neighbors(curr_cell, maze, cells_on_fire)
                k = len(neighbors_on_fire)
                catch_probability = 1- (1 - q)**k
                if random.random() < catch_probability:
                    next_cells_on_fire.add(curr_cell)
    cells_on_fire.update(next_cells_on_fire)




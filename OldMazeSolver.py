import csv

def StartFinish():
    _start = [i for i in range(len(maze[0])) if maze[0][i] == '0']
    _end = [i for i in range(len(maze[0])) if maze[len(maze)-1][i] == '0']
    return [0, _start[0]], [len(maze) - 1, _end[0]]

#p is path
def MazeSolver():
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == 'u':
                print(f'{maze[i][j]}', end=" ")
            elif maze[i][j] == '0':
                print(f'{maze[i][j]}', end=" ")
            elif maze[i][j] == 'p':
                print(f'{maze[i][j]}', end=" ")
            else:
                print(f'{maze[i][j]}', end=" ")
        print('\n')


def Escape():
    current_cell = rat_path[len(rat_path) - 1]

    if current_cell == finish:
        return

    if maze[current_cell[0] + 1][current_cell[1]] == '0':
        maze[current_cell[0] + 1][current_cell[1]] = 'p'
        rat_path.append([current_cell[0] + 1, current_cell[1]])
        Escape()

    if maze[current_cell[0]][current_cell[1] + 1] == '0':
        maze[current_cell[0]][current_cell[1] + 1] = 'p'
        rat_path.append([current_cell[0], current_cell[1] + 1])
        Escape()

    if maze[current_cell[0] - 1][current_cell[1]] == '0':
        maze[current_cell[0] - 1][current_cell[1]] = 'p'
        rat_path.append([current_cell[0] - 1, current_cell[1]])
        Escape()

    if maze[current_cell[0]][current_cell[1] - 1] == '0':
        maze[current_cell[0]][current_cell[1] - 1] = 'p'
        rat_path.append([current_cell[0], current_cell[1] - 1])
        Escape()


    current_cell = rat_path[len(rat_path) - 1]
    if current_cell != finish:
        cell_to_remove = rat_path[len(rat_path) - 1]
        rat_path.remove(cell_to_remove)
        maze[cell_to_remove[0]][cell_to_remove[1]] = '0'


if __name__ == '__main__':
  with open('maze.txt') as csv_file:
    maze = list(csv.reader(csv_file, delimiter=','))

    start, finish = StartFinish()
    maze[start[0]][start[1]] = 'p'

    rat_path = [start]
    Escape()
    print(MazeSolver())

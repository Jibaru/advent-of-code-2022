
from collections import deque

A_VALUE = 1
Z_VALUE = 26

def bfs(matrix, goalIndex, startIndex = None):
    colSize = len(matrix)
    rowSize = len(matrix[0])

    Q = deque()
    for i in range(colSize):
        for j in range(rowSize):
            if matrix[i][j] == 1:
                if startIndex != None and (i, j) == startIndex:
                    Q.append(((i, j), 0))
                elif startIndex == None:
                    Q.append(((i, j), 0))
    
    visited = set()
    
    while Q:
        (i, j), count = Q.popleft()

        if (i, j) in visited:
            continue
        
        visited.add((i, j))

        if (i, j) == goalIndex:
            return count
        
        for dirI, dirJ in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            newI = i + dirI
            newJ = j + dirJ

            if 0 <= newI < colSize and 0 <= newJ < rowSize and matrix[newI][newJ] <= 1 + matrix[i][j]:
                Q.append(((newI, newJ), count + 1))

def parseData(data):
    matrix = [list(line) for line in data.split("\n")]
    
    colSize = len(matrix)
    rowSize = len(matrix[0])
    
    startIndex = None
    goalIndex = None
    
    for i in range(0, colSize):
        for j in range(0, rowSize):
            if matrix[i][j] == 'S':
                matrix[i][j] = A_VALUE
                startIndex = (i, j)
                continue
                
            if matrix[i][j] == 'E':
                matrix[i][j] = Z_VALUE
                goalIndex = (i, j)
                continue
            
            matrix[i][j] = ord(matrix[i][j]) - ord('a') + 1
    
    return (matrix, startIndex, goalIndex)

'''
--- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?

Your puzzle answer was 468.
'''
def solve01(data):
    matrix, startIndex, goalIndex = parseData(data)
    return bfs(matrix, goalIndex, startIndex)
    
'''
--- Part Two ---
As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^
This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?

Your puzzle answer was 459.
'''
def solve02(data):
    matrix, _, goalIndex = parseData(data)
    return bfs(matrix, goalIndex)
    
if __name__ == "__main__":
    # data = open('day-12-input.test.txt', 'r').read()
    data = open('day-12-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))

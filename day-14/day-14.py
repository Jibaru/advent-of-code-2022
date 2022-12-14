def exportMatrix(matrix):
    lines = ""
    for i in range(0, len(matrix)):
        lines += "".join(matrix[i])
        lines += "\n"
    
    f = open("matrix.txt", "w")
    f.write(lines)
    f.close()

def parseMatrix(paths):
    minX = 9999999
    maxX = -1
    
    minY = 9999999
    maxY = -1
    
    rocks = set()
    
    for path in paths:
        prev = path[0]
        prev[0] = int(prev[0])
        prev[1] = int(prev[1])
        
        minX = min(minX, prev[0])
        minY = min(minY, prev[1])
        
        maxX = max(maxX, prev[0])
        maxY = max(maxY, prev[1])
        
        rocks.add((prev[0], prev[1]))
    
        for i in range(1, len(path)):
            curr = path[i]
            curr[0] = int(curr[0])
            curr[1] = int(curr[1])
            
            minX = min(minX, curr[0])
            minY = min(minY, curr[1])
            
            maxX = max(maxX, curr[0])
            maxY = max(maxY, curr[1])
            
            if prev[0] == curr[0]:
                mn = min(prev[1], curr[1])
                mx = max(prev[1], curr[1])
                for y in range(mn, mx + 1):
                    rocks.add((prev[0], y))
            if prev[1] == curr[1]:
                mn = min(prev[0], curr[0])
                mx = max(prev[0], curr[0])
                for x in range(mn, mx + 1):
                    rocks.add((x, prev[1]))

            prev = curr
    
    matrix = [["." for _2 in range(minX, maxX + 1)] for _ in range(0, maxY + 1)]
    
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            if (j + minX, i) in rocks:
                matrix[i][j] = '#'
                
    return (matrix, minX, maxX, minY, maxY) 

def printIndexes(matrix, minX):
    for i in range(0, len(matrix)):
        line = []
        for j in range(0, len(matrix[i])):
            line.append(f"'({i},{j + minX})")
        print(" ".join(line))
 
def canGoDown(matrix, x, y):
    return matrix[x + 1][y] == '.'
    
def canGoLeft(matrix, x, y):
    return matrix[x + 1][y - 1] == '.'
    
def canGoRight(matrix, x, y):
    return matrix[x + 1][y + 1] == '.'

def isOut(matrix, x, y):
    return x >= len(matrix) or x < 0 or y >= len(matrix[0]) or y < 0

def isOutDown(matrix, x, y):
    return isOut(matrix, x + 1, y)

def isOutLeft(matrix, x, y):
    return isOut(matrix, x + 1, y - 1)

def isOutRight(matrix, x, y):
    return isOut(matrix, x + 1, y + 1)

'''
--- Day 14: Regolith Reservoir ---
The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the waterfall itself, and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the cave! If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will come in handy here. You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures made of rock.

Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path, where x represents distance to the right and y represents distance down. Each path appears as a single line of text in your scan. After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path consists of three straight lines. (Specifically, the first path consists of a line of rock from 498,4 through 498,6 and another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:


  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.
Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes to rest. A unit of sand is large enough to fill one tile of air in your scan.

A unit of sand always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move diagonally one step down and to the left. If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as long as it is able to do so, at each step trying to move down, then down-left, then down-right. If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source.

So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.
The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.
After a total of five units of sand have come to rest, they form this pattern:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.
After a total of 22 units of sand:

......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.
Finally, only two more units of sand can possibly come to rest:

......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.
Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom, falling into the endless void. Just for fun, the path any new sand takes before falling forever is shown here with ~:

.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........
Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the abyss below?

Your puzzle answer was 858.
'''
def solve01(data):
    paths = [[path.split(",") for path in line.split(" -> ")] for line in data.split("\n")]
    
    matrix, _, maxX, _, _ = parseMatrix(paths)

    counter = 0
    startY = len(matrix[0]) - (maxX - 500) - 1
    x, y = 0, startY

    while True:
        while not isOutDown(matrix, x, y) and canGoDown(matrix, x, y):
            x += 1

        if isOutDown(matrix, x, y):
            break
        
        if isOutLeft(matrix, x, y):
            break
        
        if canGoLeft(matrix, x, y):
            y -= 1
            x += 1
            continue
        
        if isOutRight(matrix, x, y):
            break
        
        if canGoRight(matrix, x, y):
            y += 1
            x += 1
            continue

        matrix[x][y] = 'o'
        x, y = 0, startY
        counter += 1
    
    return counter

'''
--- Part Two ---
You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!

You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.

In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. (This is as if your scan contained one extra rock path like -infinity,11 -> infinity,11.) With the added floor, the example above now looks like this:

        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->
To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, blocking the source entirely and stopping the flow of sand into the cave. In the example above, the situation finally looks like this after 93 units of sand come to rest:

............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################
Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?

Your puzzle answer was 26845.
'''
def solve02(data):
    paths = [[path.split(",") for path in line.split(" -> ")] for line in data.split("\n")]
    
    matrix, _, maxX, _, _ = parseMatrix(paths)
    
    ORIGINAL_ROW_LENGTH = len(matrix[0])
    EXTEND = 200

    def extendMatrix():
        for row in matrix:
            for _ in range(0, EXTEND):
                row.insert(0, '.')
                row.append('.')
        
        matrix.append([])
        matrix.append([])
        
        for _ in range(len(matrix[0])):
            matrix[-2].append('.')
            matrix[-1].append('#')
    
    extendMatrix()
    
    counter = 0
    startY = (ORIGINAL_ROW_LENGTH - (maxX - 500) - 1) + EXTEND
    x, y = 0, startY

    while True:
        if matrix[0][startY] == 'o':
            break
    
        while not isOutDown(matrix, x, y) and canGoDown(matrix, x, y):
            x += 1

        if isOutDown(matrix, x, y):
            break
        
        if isOutLeft(matrix, x, y):
            break
        
        if canGoLeft(matrix, x, y):
            y -= 1
            x += 1
            continue
        
        if isOutRight(matrix, x, y):
            break
        
        if canGoRight(matrix, x, y):
            y += 1
            x += 1
            continue

        matrix[x][y] = 'o'
        x, y = 0, startY
        counter += 1

    return counter
    
if __name__ == "__main__":
    # data = open('day-14-input.test.txt', 'r').read()
    data = open('day-14-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))

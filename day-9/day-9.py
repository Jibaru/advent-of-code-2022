# prev -> RopePoint -> next
class RopePoint:
    def __init__(self, x, y, prev = None, next = None):
        self.x = x
        self.y = y
        self.next = next
        self.prev = prev
        self.visits = {}
        self.storePosition()
    
    def isHead(self):
        return self.next == None

    def isTail(self):
        return self.prev == None
    
    def isInDiagonalToTheNext(self):
        return (self.next.x != self.x) and (self.next.y != self.y)
    
    def isOverlappingToTheNext(self):
        return (self.next.x == self.x and self.next.y == self.y)

    def isTouchingTheNext(self):
        return (
            (self.next.x == self.x - 1 and self.next.y == self.y + 1) or
            (self.next.x == self.x and self.next.y == self.y + 1) or
            (self.next.x == self.x + 1 and self.next.y == self.y + 1) or
            (self.next.x == self.x + 1 and self.next.y == self.y) or
            (self.next.x == self.x + 1 and self.next.y == self.y - 1) or
            (self.next.x == self.x and self.next.y == self.y - 1) or
            (self.next.x == self.x - 1 and self.next.y == self.y - 1) or
            (self.next.x == self.x - 1 and self.next.y == self.y)
        )
        
    def move(self):
        if self.next.x == 0 and self.next.y == 0:
            return
        
        if self.isTouchingTheNext():
            return

        if self.isInDiagonalToTheNext() and not self.isTouchingTheNext():
            self.moveInDiagonal()
            return
        
        if self.isOverlappingToTheNext():
            return

        # not in diagonal and not touching
        positionOfNext = self.getDirectionOfNext()
        self.moveInTo(positionOfNext)
            
    def moveInDiagonal(self):
        x = self.x
        y = self.y
        x2 = self.next.x
        y2 = self.next.y
        
        if x2 > x and y2 > y:
            # move into up right
            self.x += 1
            self.y += 1
            
        elif x2 < x and y2 > y:
            # move into up left
            self.x -= 1
            self.y += 1
        elif x2 < x and y2 < y:
            # move into down left
            self.x -= 1
            self.y -= 1
        else:
            # move into down right
            self.x += 1
            self.y -= 1
        self.storePosition()
        
    def getDirectionOfNext(self):
        x = self.x
        y = self.y
        x2 = self.next.x
        y2 = self.next.y
        if x < x2 and y == y2:
            return "R"
        if x == x2 and y < y2:
            return "U"
        if x > x2 and y == y2:
            return "L"
        if x == x2 and y > y2:
            return "D"
        
        print(f"In diagonal!!: ({x, y}) > ({x2, y2})")

    def moveInTo(self, direction):
        '''
        Use only for head
        '''
        dirs = {
            "R": {
                "axis": "x",
                "count": 1
            },
            "L": {
                "axis": "x",
                "count": -1
            },
            "U": {
                "axis": "y",
                "count": 1
            },
            "D": {
                "axis": "y",
                "count": -1
            },
        }
        
        dir = dirs[direction]
        
        if dir["axis"] == "x":
            self.x += dir["count"]
        elif dir["axis"] == "y":
            self.y += dir["count"]
            
        self.storePosition()
    
    def storePosition(self):
        self.visits[f"{self.x},{self.y}"] = True
        
    def setNext(self, next):
        self.next = next
        
    def getTotalDifferentPositions(self):
        return len(self.visits)

'''
--- Day 9: Rope Bridge ---
This rope bridge creaks as you walk along it. You aren't sure how old it is, or whether it can even support your weight.

It seems to support the Elves just fine, though. The bridge spans a gorge which was carved out by the massive river far below you.

You step carefully; as you do, the ropes stretch and twist. You decide to distract yourself by modeling rope physics; maybe you can even figure out where not to step.

Consider a rope with a knot at each end; these knots mark the head and the tail of the rope. If the head moves far enough away from the tail, the tail is pulled toward the head.

Due to nebulous reasoning involving Planck lengths, you should be able to model the positions of the knots on a two-dimensional grid. Then, by following a hypothetical series of motions (your puzzle input) for the head, you can determine how the tail will move.

Due to the aforementioned Planck lengths, the rope must be quite short; in fact, the head (H) and tail (T) must always be touching (diagonally adjacent and even overlapping both count as touching):

....
.TH.
....

....
.H..
..T.
....

...
.H. (H covers T)
...
If the head is ever two steps directly up, down, left, or right from the tail, the tail must also move one step in that direction so it remains close enough:

.....    .....    .....
.TH.. -> .T.H. -> ..TH.
.....    .....    .....

...    ...    ...
.T.    .T.    ...
.H. -> ... -> .T.
...    .H.    .H.
...    ...    ...
Otherwise, if the head and tail aren't touching and aren't in the same row or column, the tail always moves one step diagonally to keep up:

.....    .....    .....
.....    ..H..    ..H..
..H.. -> ..... -> ..T..
.T...    .T...    .....
.....    .....    .....

.....    .....    .....
.....    .....    .....
..H.. -> ...H. -> ..TH.
.T...    .T...    .....
.....    .....    .....
You just need to work out where the tail goes as the head follows a series of motions. Assume the head and the tail both start at the same position, overlapping.

For example:

R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
This series of motions moves the head right four steps, then up four steps, then left three steps, then down one step, and so on. After each step, you'll need to update the position of the tail if the step means the head is no longer adjacent to the tail. Visually, these motions occur as follows (s marks the starting position as a reference RopePoint):

== Initial State ==

......
......
......
......
H.....  (H covers T, s)

== R 4 ==

......
......
......
......
TH....  (T covers s)

......
......
......
......
sTH...

......
......
......
......
s.TH..

......
......
......
......
s..TH.

== U 4 ==

......
......
......
....H.
s..T..

......
......
....H.
....T.
s.....

......
....H.
....T.
......
s.....

....H.
....T.
......
......
s.....

== L 3 ==

...H..
....T.
......
......
s.....

..HT..
......
......
......
s.....

.HT...
......
......
......
s.....

== D 1 ==

..T...
.H....
......
......
s.....

== R 4 ==

..T...
..H...
......
......
s.....

..T...
...H..
......
......
s.....

......
...TH.
......
......
s.....

......
....TH
......
......
s.....

== D 1 ==

......
....T.
.....H
......
s.....

== L 5 ==

......
....T.
....H.
......
s.....

......
....T.
...H..
......
s.....

......
......
..HT..
......
s.....

......
......
.HT...
......
s.....

......
......
HT....
......
s.....

== R 2 ==

......
......
.H....  (H covers T)
......
s.....

......
......
.TH...
......
s.....
After simulating the rope, you can count up all of the positions the tail visited at least once. In this diagram, s again marks the starting position (which the tail also visited) and # marks other positions the tail visited:

..##..
...##.
.####.
....#.
s###..
So, there are 13 positions the tail visited at least once.

Simulate your complete hypothetical series of motions. How many positions does the tail of the rope visit at least once?

Your puzzle answer was 6563.
'''
def solve01(data):
    seriesOfMotions = [line.split(" ") for line in data.split("\n")]
    
    tail = RopePoint(0, 0)
    head = RopePoint(0, 0, tail)
    tail.setNext(head)

    for serie in seriesOfMotions:
        direction, steps = serie[0], int(serie[1])

        for _ in range(0, steps):
            head.moveInTo(direction)
            tail.move()

    return tail.getTotalDifferentPositions()
    
'''
--- Part Two ---
A rope snaps! Suddenly, the river is getting a lot closer than you remember. The bridge is still there, but some of the ropes that broke are now whipping toward you as you fall through the air!

The ropes are moving too quickly to grab; you only have a few seconds to choose how to arch your body to avoid being hit. Fortunately, your simulation can be extended to support longer ropes.

Rather than two knots, you now must simulate a rope consisting of ten knots. One knot is still the head of the rope and moves according to the series of motions. Each knot further down the rope follows the knot in front of it using the same rules as before.

Using the same series of motions as the above example, but with the knots marked H, 1, 2, ..., 9, the motions now occur as follows:

== Initial State ==

......
......
......
......
H.....  (H covers 1, 2, 3, 4, 5, 6, 7, 8, 9, s)

== R 4 ==

......
......
......
......
1H....  (1 covers 2, 3, 4, 5, 6, 7, 8, 9, s)

......
......
......
......
21H...  (2 covers 3, 4, 5, 6, 7, 8, 9, s)

......
......
......
......
321H..  (3 covers 4, 5, 6, 7, 8, 9, s)

......
......
......
......
4321H.  (4 covers 5, 6, 7, 8, 9, s)

== U 4 ==

......
......
......
....H.
4321..  (4 covers 5, 6, 7, 8, 9, s)

......
......
....H.
.4321.
5.....  (5 covers 6, 7, 8, 9, s)

......
....H.
....1.
.432..
5.....  (5 covers 6, 7, 8, 9, s)

....H.
....1.
..432.
.5....
6.....  (6 covers 7, 8, 9, s)

== L 3 ==

...H..
....1.
..432.
.5....
6.....  (6 covers 7, 8, 9, s)

..H1..
...2..
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

.H1...
...2..
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

== D 1 ==

..1...
.H.2..
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

== R 4 ==

..1...
..H2..
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

..1...
...H..  (H covers 2)
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

......
...1H.  (1 covers 2)
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

......
...21H
..43..
.5....
6.....  (6 covers 7, 8, 9, s)

== D 1 ==

......
...21.
..43.H
.5....
6.....  (6 covers 7, 8, 9, s)

== L 5 ==

......
...21.
..43H.
.5....
6.....  (6 covers 7, 8, 9, s)

......
...21.
..4H..  (H covers 3)
.5....
6.....  (6 covers 7, 8, 9, s)

......
...2..
..H1..  (H covers 4; 1 covers 3)
.5....
6.....  (6 covers 7, 8, 9, s)

......
...2..
.H13..  (1 covers 4)
.5....
6.....  (6 covers 7, 8, 9, s)

......
......
H123..  (2 covers 4)
.5....
6.....  (6 covers 7, 8, 9, s)

== R 2 ==

......
......
.H23..  (H covers 1; 2 covers 4)
.5....
6.....  (6 covers 7, 8, 9, s)

......
......
.1H3..  (H covers 2, 4)
.5....
6.....  (6 covers 7, 8, 9, s)
Now, you need to keep track of the positions the new tail, 9, visits. In this example, the tail never moves, and so it only visits 1 position. However, be careful: more types of motion are possible than before, so you might want to visually compare your simulated rope to the one above.

Here's a larger example:

R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
These motions occur as follows (individual steps are not shown):

== Initial State ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
...........H..............  (H covers 1, 2, 3, 4, 5, 6, 7, 8, 9, s)
..........................
..........................
..........................
..........................
..........................

== R 5 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
...........54321H.........  (5 covers 6, 7, 8, 9, s)
..........................
..........................
..........................
..........................
..........................

== U 8 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
................H.........
................1.........
................2.........
................3.........
...............54.........
..............6...........
.............7............
............8.............
...........9..............  (9 covers s)
..........................
..........................
..........................
..........................
..........................

== L 8 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
........H1234.............
............5.............
............6.............
............7.............
............8.............
............9.............
..........................
..........................
...........s..............
..........................
..........................
..........................
..........................
..........................

== D 3 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
.........2345.............
........1...6.............
........H...7.............
............8.............
............9.............
..........................
..........................
...........s..............
..........................
..........................
..........................
..........................
..........................

== R 17 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
................987654321H
..........................
..........................
..........................
..........................
...........s..............
..........................
..........................
..........................
..........................
..........................

== D 10 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
...........s.........98765
.........................4
.........................3
.........................2
.........................1
.........................H

== L 25 ==

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
...........s..............
..........................
..........................
..........................
..........................
H123456789................

== U 20 ==

H.........................
1.........................
2.........................
3.........................
4.........................
5.........................
6.........................
7.........................
8.........................
9.........................
..........................
..........................
..........................
..........................
..........................
...........s..............
..........................
..........................
..........................
..........................
..........................

Now, the tail (9) visits 36 positions (including s) at least once:

..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
..........................
#.........................
#.............###.........
#............#...#........
.#..........#.....#.......
..#..........#.....#......
...#........#.......#.....
....#......s.........#....
.....#..............#.....
......#............#......
.......#..........#.......
........#........#........
.........########.........
Simulate your complete series of motions on a larger rope with ten knots. How many positions does the tail of the rope visit at least once?

Your puzzle answer was 2653.
'''
def solve02(data):
    seriesOfMotions = [line.split(" ") for line in data.split("\n")]
    tail = RopePoint(0, 0)
    head = tail
    for i in range(1, 10):
        newRopePoint = RopePoint(0, 0, head)
        head.setNext(newRopePoint)
        head = newRopePoint

    for serie in seriesOfMotions:
        direction, steps = serie[0], int(serie[1])

        for _ in range(0, steps):
            current = head
            while current != None:
                if current.isHead():
                    current.moveInTo(direction)
                else:
                    current.move()
                
                current = current.prev

    return tail.getTotalDifferentPositions()
    
if __name__ == "__main__":
    # data = open('day-9-input.test.txt', 'r').read()
    data = open('day-9-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))

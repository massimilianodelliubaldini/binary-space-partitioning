import typing
from   typing import Generic, TypeVar

import operator

T = TypeVar('T')
E = 0.000005

def floatcompare(op, a:float, b:float, eps:float) -> bool:

    if op == operator.eq:
        return a - b < eps and a - b > (-1 * eps)

    if op == operator.gt:
        return a - b > eps

    if op == operator.lt:
        return a - b < (-1 * eps)

    raise ValueError

class Node(Generic[T]):
    data : T
    
    def __init__(self, d:T):
        self.data = d

    def __str__(self):
        if type(self.data) is list:
            
            concat = 'Node: {' + str(self.data[0])
            for d in self.data[1:]:
                concat += ', ' + str(d)
            concat += '}'
            
            return concat
        else:
            return 'Node: {' + str(self.data) + '}'

class BinaryTree():
    node : 'Node'
    left : 'BinaryTree'
    right : 'BinaryTree'
    
    def __init__(self, n:'Node', l:'BinaryTree' = None, r:'BinaryTree' = None):
        self.node = n
        self.left = l
        self.right = r

    def __str__(self):
        def tostr(tree, level):
            spaces  = '   ' * level
            if not tree:
                return str(0)
            else:
                concat  = str(tree.node) + '\n'
                concat += spaces + '|__' + tostr(tree.left,  level + 1) + '\n'
                concat += spaces + '|__' + tostr(tree.right, level + 1)
                return concat
            
        return tostr(self, 0)

class Point():
    x : float
    y : float
    
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def __str__(self):
        return '{' + str(self.x) + ', ' + str(self.y) + '}'

class Line():
    p1 : 'Point'
    p2 : 'Point'
    m : float
    y0 : float 
    is_vertical : bool
    
    def __init__(self, p1:'Point', p2:'Point'):
        self.p1 = p1
        self.p2 = p2
        
        if self.p2.x - self.p1.x == 0:
            self.m = None
            self.y0 = None
            self.is_vertical = True
        else:
            self.m = (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
            self.y0 = self.p1.y - (self.m * self.p1.x)
            self.is_vertical = False

    def __str__(self):
        return 'Line: {' + str(self.p1) + ', ' + str(self.p2) + '}'
   
    def relate(self, line:'Line') -> dict:
        p1_result = None       
        p2_result = None
        
        # Front-back test on first point.
        if   floatcompare(operator.gt, line.p1.y, (self.m * line.p1.x) + self.y0, E):
            p1_result = 1
            
        elif floatcompare(operator.lt, line.p1.y, (self.m * line.p1.x) + self.y0, E):
            p1_result = -2
            
        else:
            p1_result = 0
        
        # Front-back test on second point.
        if   floatcompare(operator.gt, line.p2.y, (self.m * line.p2.x) + self.y0, E):
            p2_result = 1
            
        elif floatcompare(operator.lt, line.p2.y, (self.m * line.p2.x) + self.y0, E):
            p2_result = -2
            
        else:
            p2_result = 0
            
        # Both points are farther from origin than self.
        if p1_result + p2_result > 0:
            return { 'position':'ahead', 'backline':None, 'frontline':None }
            
        # Both points are closer to origin than self.
        if p1_result + p2_result < -1:
            return { 'position':'behind', 'backline':None, 'frontline':None }
            
        # Both points are on self.
        if p1_result + p2_result == 0:
            return { 'position':'collinear', 'backline':None, 'frontline':None }
            
        # One point is farther and the other is closer.
        if p1_result + p2_result == -1:

            # Not safe from ZeroDivisionError!
            xi = (line.y0 - self.y0) / (self.m - line.m)
            yi = (self.m * xi) + self.y0
            
            if p1_result == 1:
                return { 'position':'intersect', 'backline':Line(line.p1, Point(xi, yi)), 'frontline':Line(Point(xi, yi), line.p2) }
            else:
                return { 'position':'intersect', 'backline':Line(Point(xi, yi), line.p2), 'frontline':Line(line.p1, Point(xi, yi)) }
    
def generate_bsp_tree(lines:list) -> 'BinaryTree':

    if len(lines) == 0:
        return None

    back_list  = []
    front_list = []
    line = lines[0]
    tree = BinaryTree(Node([line]))

    for other in lines[1:]:
        relation = line.relate(other)
        
        if relation['position'] == 'ahead':
            back_list.append(other)
            
        elif relation['position'] == 'behind':
            front_list.append(other)
            
        elif relation['position'] == 'collinear':
            tree.node.data.append(other)
            
        else:
            back_list.append(relation['backline'])
            front_list.append(relation['frontline'])
            
    tree.left  = generate_bsp_tree(back_list)
    tree.right = generate_bsp_tree(front_list)

    return tree

def main():

    lines = [
    Line(
        Point( 1,  1), 
        Point( 2,  2)), 
    Line(
        Point( 4,  4), 
        Point( 7,  4)), 
    Line(        
        Point( 0, 10), 
        Point( 3,  8)), 
    Line(
        Point( 7,  4), 
        Point( 9,  5)),
    Line(
        Point( 4,  5), 
        Point( 7,  8)),
    Line(
        Point( 2,  5), 
        Point( 4,  2)),
    Line(
        Point( 2,  5), 
        Point( 3,  8)),
    Line(
        Point( 7,  4), 
        Point( 8,  0)),
    Line(
        Point( 6,  7), 
        Point( 9,  7))
    ]

    for line in lines:
        print(str(line))

    tree = generate_bsp_tree(lines)
    print()
    print(str(tree))


if __name__ == '__main__':
    main()

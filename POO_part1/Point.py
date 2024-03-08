
import matplotlib.pyplot as plt
import math

class Point(object):
    nom = "Point"
    
    def __init__(self, _abs = 0, _ord = 0):
        self.abs = _abs
        self.ord = _ord

    def translate(self, dx = 0, dy = 0):
        self.ord += dx
        self.abs += dy
    
    def distance(self, other):
        dx = self.abs - other.abs
        dy = self.ord - other.ord
        return math.sqrt(dx**2 + dy**2)
    
    def __eq__(self, other):
        return self.abs == other.abs and self.ord == other.ord
    
    def draw(self):
        plt.plot(self.abs , self.ord, 'ro')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Point')
        plt.grid(True)
        plt.show()

    def __str__(self):
        return f'({self.abs}, {self.ord})'

#---------Programme principal--------------
        
point1 = Point(3.5, 1.2)
print(point1)

point2 = Point(5,2)
print(point1 == point2)

point1.translate(1, -0.2)
print(point1)

print(point1.distance(point2))

point1.draw()



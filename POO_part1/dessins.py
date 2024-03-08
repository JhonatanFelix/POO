import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Rectangle:
    nbr = 0

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        Rectangle.nbr += 1

    def __str__(self):
        return f"Rectangle: ({self.x}, {self.y}), largeur: {self.width}, hauteur: {self.height}"

    def surface(self):
        return self.width * self.height

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def containsPoint(self, point):
        px, py = point
        return self.x <= px <= self.x + self.width and self.y <= py <= self.y + self.height

    def containsRec(self, other):
        return (self.x <= other.x) and (self.y <= other.y) and (self.x + self.width >= other.x + other.width) and (self.y + self.height >= other.y + other.height)

    def __eq__(self, other):
        return (self.x, self.y, self.width, self.height) == (other.x, other.y, other.width, other.height)

    @classmethod
    def hull(cls, rectangles):
        min_x = min(rect.x for rect in rectangles)
        min_y = min(rect.y for rect in rectangles)
        max_x = max(rect.x + rect.width for rect in rectangles)
        max_y = max(rect.y + rect.height for rect in rectangles)
        return cls(min_x, min_y, max_x - min_x, max_y - min_y)



class Dessin:
    def __init__(self):
        self.rectangles = []
        self.hullRect = None 

    def add(self, rectangle):
        self.rectangles.append(rectangle)
        if self.hullRect is None:
            self.hullRect = rectangle
        else:
            self.hullRect = Rectangle.hull([self.hullRect, rectangle])

    def surface(self):
        return sum(rect.surface() for rect in self.rectangles)

    def translate(self, dx, dy):
        for rect in self.rectangles:    
            rect.translate(dx, dy)
        if self.hullRect:
            self.hullRect.translate(dx, dy)

    def hull(self):
        self.hullRect = Rectangle.hull(self.rectangles) if self.rectangles else None
        return self.hullRect

    def visualiser(self):
        fig, ax = plt.subplots()
        for rect in self.rectangles:
            ax.add_patch(patches.Rectangle((rect.x, rect.y), rect.width, rect.height, fill=False, edgecolor='blue'))
        
        if self.hullRect:
            ax.add_patch(patches.Rectangle((self.hullRect.x, self.hullRect.y), self.hullRect.width, self.hullRect.height, fill=False, edgecolor='red', linewidth=2, linestyle='--'))
        
        plt.xlim(-10, 100) 
        plt.ylim(-10, 100)
        plt.grid(True)
        ax.set_aspect('equal')
        plt.show()
    
dessin = Dessin()
dessin.add(Rectangle(0, 0, 10, 20))
dessin.add(Rectangle(5, 5, 15, 25))
print(dessin.surface())  # Calcul de la surface totale
dessin.translate(10, 10)  # Translation de tous les rectangles
hull = dessin.hull()  # Calcul du rectangle englobant

if hull:
    print(f"Rectangle englobant: {hull}")
else:
    print("Pas de rectangle englobant.")

dessin.visualiser()
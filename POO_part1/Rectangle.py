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


rect1 = Rectangle(3.5, 1.2, 3, 2)
rect2 = Rectangle(4, 2, 2, 1)
print(rect1)
print("Surface:", rect1.surface())
rect1.translate(1, 1)
print(rect1)

point = (4, 3)
print("Le point", point, "est-il dans le rectangle?", rect1.containsPoint(point))

print("Rectangle 2 est-il dans le rectangle 1?", rect1.containsRec(rect2))

print("Nombre de rectangles créés:", Rectangle.nbr)

rect3 = Rectangle(2, 1, 4, 3)
print("Rectangle 3 est-il égal à Rectangle 1?", rect1 == rect3)

rectangles = [rect1, rect2, rect3]
hull_rectangle = Rectangle.hull(rectangles)
print("Rectangle englobant:", hull_rectangle)

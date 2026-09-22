class Bird:

    def move(self):
        print("Bird is moving")


class Sparrow(Bird):

    def move(self):
        print("Sparrow is flying")


class Penguin(Bird):

    def move(self):
        print("Penguin is walking")


birds = [
    Sparrow(),
    Penguin()
]

for bird in birds:
    bird.move()
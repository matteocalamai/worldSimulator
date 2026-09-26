class Person:
    def __init__(self, age):
        self.age = age
        self.health = 100.0
        self.energy = 100.0
        self.hunger = 0.0

    def update(self, deltaTime):

        # age
        self.age += deltaTime / 365

        # needs
        self.energy -= deltaTime * 2
        self.hunger += deltaTime * 1

        # health
        if self.hunger > 80:
            self.health -= deltaTime * 0.5

        # keep values within valid ranges
        self.energy = max(0, min(100, self.energy))
        self.hunger = max(0, min(100, self.hunger))
        self.health = max(0, min(100, self.health))

    def __repr__(self):
        return (
            f"Person("
            f"age={self.age:.2f}, "
            f"health={self.health:.2f}, "
            f"energy={self.energy:.2f}, "
            f"hunger={self.hunger:.2f}"
            f")"
        )

    def eat(self, amount):
        self.hunger -= amount
        self.hunger = max(0, self.hunger)

class World:
    def __init__(self):
        self.time = 0.0
        self.people = []
        self.food = 100.0

    def step(self, deltaTime):
        self.time += deltaTime

        for person in self.people:
            person.update(deltaTime)

            if person.hunger >= 50 and person.hunger < 80:
                self.feedPerson(person, 30)

    def feedPerson(self, person, amount):
        if self.food <= 0:
            return

        foodConsumed = min(amount, self.food)

        person.eat(foodConsumed)
        self.food -= foodConsumed



world = World()

world.people.append(Person(25))
# world.people.append(Person(42))
# world.people.append(Person(17))

print("Initial state:")
print(world.people)

# simulate 100 days
for _ in range(100):
    world.step(1)

print("\nAfter 100 days:")
print(world.people)


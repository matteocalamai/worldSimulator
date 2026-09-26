class Person:
    def __init__(self, age):
        self.age = age

    def update(self, deltaTime):
        self.age += deltaTime / 365

class World:
    def __init__(self):
        self.time = 0.0
        self.people = []

    def step(self, deltaTime):
        self.time += deltaTime

        for person in self.people:
            person.update(deltaTime)



world = World()

world.people.append(Person(25))
world.people.append(Person(42))
world.people.append(Person(17))

print("Day:", world.time)
print("Population:", len(world.people))
for person in world.people:
    print(person.age)

for _ in range(365):
    world.step(1)
# world.step(2)

print("\nDay:", world.time)
print("Population:", len(world.people))
for person in world.people:
    print(person.age)



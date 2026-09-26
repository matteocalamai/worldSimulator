class Event:
    def __init__(self, time, message):
        self.time = time
        self.message = message

    def __repr__(self):
        return f"[Day {self.time}] {self.message}"

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

    def work(self, deltaTime):
        # a person will not work if they are too tired or too hungry
        if self.hunger >= 80:
            return 0

        if self.energy <= 0:
            return 0

        # work consumes energy
        energyCost = deltaTime * 3
        self.energy -= energyCost
        self.energy = max(0, self.energy)

        # food produced is proportional to the time worked
        foodProduced = deltaTime * 2
        return foodProduced

class World:
    def __init__(self):
        self.time = 0.0
        self.people = []
        self.food = 100.0
        self.events = []

    def addEvent(self, message):
        event = Event(self.time, message)
        self.events.append(event)

    def step(self, deltaTime):
        self.time += deltaTime

        for person in self.people:
            # update people
            person.update(deltaTime)

            # work
            foodProduced = person.work(deltaTime)

            if foodProduced > 0:
                self.food += foodProduced

                self.addEvent(
                    f"Person worked and produced "
                    f"{foodProduced:.1f} food"
                )

            if person.hunger >= 50 and person.hunger < 80:
                foodConsumed = self.feedPerson(person, 30)
                
                if foodConsumed > 0:
                    self.addEvent(
                        f"Person ate {foodConsumed:.1f} food"
                    )

                
    
    def feedPerson(self, person, amount):
        if self.food <= 0:
            return 0

        foodConsumed = min(amount, self.food)

        person.eat(foodConsumed)
        self.food -= foodConsumed

        return foodConsumed

# --------------------

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

print("\nEVENTS")
print("--------------------")

for event in world.events:
    print(event)
class Event:
    def __init__(self, time, message):
        self.time = time
        self.message = message

    def __repr__(self):
        return f"[Day {self.time}] {self.message}"

class Person:
    nextID = 1

    def __init__(self, age):
        self.id = Person.nextID
        Person.nextID += 1
        
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
            f"Person #{self.id} | "
            f"Age: {self.age:.1f} | "
            f"Health: {self.health:.1f} | "
            f"Energy: {self.energy:.1f} | "
            f"Hunger: {self.hunger:.1f}"
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
                    f"Person #{person.id} worked and produced "
                    f"{foodProduced:.1f} food"
                )

            if person.hunger >= 50 and person.hunger < 80:
                foodConsumed = self.feedPerson(person, 30)
                
                if foodConsumed > 0:
                    self.addEvent(
                        f"Person #{person.id} ate "
                        f"{foodConsumed:.1f} food"
                    )

    def showStatus(self):
        print()
        print("=" * 50)
        print("WORLD")
        print("=" * 50)

        print(f"Day:        {self.time:.0f}")
        print(f"Population: {len(self.people)}")
        print(f"Food:       {self.food:.1f}")

        print()
        print("PEOPLE")
        print("-" * 50)

        for person in self.people:
            print(
                f"#{person.id:<3} "
                f"Age: {person.age:5.1f} | "
                f"Health: {person.health:5.1f} | "
                f"Energy: {person.energy:5.1f} | "
                f"Hunger: {person.hunger:5.1f}"
            )

        print("=" * 50) 

                
    
    def feedPerson(self, person, amount):
        if self.food <= 0:
            return 0

        foodConsumed = min(amount, self.food)

        person.eat(foodConsumed)
        self.food -= foodConsumed

        return foodConsumed

# --------------------

world = World()

world.people.append(Person(20))
world.people.append(Person(25))
world.people.append(Person(31))
world.people.append(Person(40))
world.people.append(Person(55))

for day in range(100):
    world.step(1)

print("PEOPLE")
print("--------------------")

for person in world.people:
    print(person)

print()
print("EVENTS")
print("--------------------")

for event in world.events:
    print(event)

print()
print(f"Food remaining: {world.food:.1f}")

world.showStatus()
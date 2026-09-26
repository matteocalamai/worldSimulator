class Event:
    def __init__(self, time, message):
        self.time = time
        self.message = message

    def __repr__(self):
        return f"[Day {self.time}] {self.message}"

class Person:
    nextID = 1

    def __init__(self, age, workEfficiency):
        self.id = Person.nextID
        Person.nextID += 1
        
        self.age = age
        self.health = 100.0
        self.energy = 100.0
        self.hunger = 0.0

        self.workEfficiency = workEfficiency

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

    def decide(self):
        if self.hunger >= 50:
            return "eat"

        if self.energy <= 20:
            return "rest"

        return "work"

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
        foodProduced = deltaTime * 2 * self.workEfficiency
        return foodProduced

    def rest(self, deltaTime):
        energyRecovered = deltaTime * 4

        self.energy += energyRecovered
        self.energy = min(100, self.energy)

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

            action = person.decide()
            self.addEvent(
                f"Person #{person.id} chose to {action}"
            )

            self.executeAction(
                person,
                action,
                deltaTime
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
                f"Hunger: {person.hunger:5.1f} | "
                f"Efficiency: {person.workEfficiency:4.1f}"
            )

        print("=" * 50) 

                
    
    def feedPerson(self, person, amount):
        if self.food <= 0:
            return 0

        foodConsumed = min(amount, self.food)

        person.eat(foodConsumed)
        self.food -= foodConsumed

        return foodConsumed

    def executeAction(self, person, action, deltaTime):
        if action == "eat":
            foodConsumed = self.feedPerson(person, 30)

            if foodConsumed > 0:
                self.addEvent(
                    f"Person #{person.id} ate "
                    f"{foodConsumed:.1f} food"
                )

        elif action == "work":
            foodProduced = person.work(deltaTime)

            if foodProduced > 0:
                self.food += foodProduced

                self.addEvent(
                    f"Person #{person.id} worked and produced "
                    f"{foodProduced:.1f} food"
                )

        elif action == "rest":
            person.rest(deltaTime)

            self.addEvent(
                f"Person #{person.id} rested"
            )

# --------------------

world = World()

world.people.append(Person(20, 0.8))
world.people.append(Person(25, 1.0))
world.people.append(Person(31, 1.2))
world.people.append(Person(40, 1.0))
world.people.append(Person(55, 0.7))

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
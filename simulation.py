from person import Person
from event import Event

class World:
    def __init__(self):
        self.time = 0.0
        self.people = []
        self.food = 20.0
        self.events = []

        self.history = []

    def getState(self, actions=None):
        state = {
            "time": self.time,
            "food": self.food,
            "population": len(self.people),
            "people": []
        }

        for person in self.people:
            personState = {
                "id": person.id,
                "age": person.age,
                "health": person.health,
                "energy": person.energy,
                "hunger": person.hunger,
                "workEfficiency": person.workEfficiency
            }

            if actions and person.id in actions:
                personState["action"] = actions[person.id]

            state["people"].append(personState)

        return state

    def addEvent(self, message):
        event = Event(self.time, message)
        self.events.append(event)

    def resolveFoodRequests(self, decisions):
        requests = {}

        for person in self.people:
            if decisions[person.id] == "eat":
                requests[person.id] = person.getFoodRequest()

        totalRequest = sum(requests.values())

        if totalRequest <= 0 or self.food <= 0:
            return

        availableFood = self.food

        for person in self.people:
            if person.id not in requests:
                continue

            share = requests[person.id] / totalRequest
            foodAmount = availableFood * share

            foodConsumed = min(foodAmount, self.food)

            person.eat(foodConsumed)
            self.food -= foodConsumed

            self.addEvent(
                f"Person #{person.id} ate "
                f"{foodConsumed:.1f} food"
            )

    def resolveActions(self, decisions, deltaTime):
        for person in self.people:
            action = decisions[person.id]

            if action == "eat":
                continue

            self.executeAction(
                person,
                action,
                deltaTime
            )

        self.resolveFoodRequests(decisions)

    def step(self, deltaTime):
        self.time += deltaTime

        # update
        for person in self.people:
            person.update(deltaTime)

        # decision
        decisions = {}
        for person in self.people:
            decisions[person.id] = person.decide(self.food)

        # resolution
        self.resolveActions(decisions, deltaTime)

        # observation
        state = self.getState(decisions)
        self.history.append(state)

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

def createWorld():
    world = World()

    world.people.append(Person(20, 0.8, 40, 0.3))
    world.people.append(Person(25, 1.0, 50, 0.6))
    world.people.append(Person(31, 1.2, 65, 0.9))
    world.people.append(Person(40, 1.0, 50, 0.5))
    world.people.append(Person(55, 0.7, 70, 0.2))

    return world


def runSimulation(world, days):
    for day in range(days):
        world.step(1)


if __name__ == "__main__":
    world = createWorld()
    runSimulation(world, 150)

    print("PEOPLE")
    print("--------------------")

#    for person in world.people:
#        print(person)

#    print()
#    print("EVENTS")
#    print("--------------------")

#    for event in world.events:
#        print(event)

#    print()
#    print(f"Food remaining: {world.food:.1f}")

    world.showStatus()
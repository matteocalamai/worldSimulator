class Person:
    nextID = 1

    def __init__(self, age, workEfficiency, hungerThreshold, hungerResilience):
        self.id = Person.nextID
        Person.nextID += 1
        
        self.age = age
        self.health = 100.0
        self.energy = 100.0
        self.hunger = 0.0

        self.workEfficiency = workEfficiency
        self.hungerThreshold = hungerThreshold
        self.hungerResilience = hungerResilience

    def update(self, deltaTime):

        # age
        self.age += deltaTime / 365

        # needs
        self.energy -= deltaTime * 2

        # health
        if self.hunger > 80:
            self.health -= deltaTime * 0.5

        # keep values within valid ranges
        self.energy = max(0, min(100, self.energy))
        self.hunger = max(0, min(100, self.hunger))
        self.health = max(0, min(100, self.health))

    def evaluateEat(self, foodAvailable):
        if not foodAvailable:
            return 0

        if self.hunger <= self.hungerThreshold:
            return 0

        hungerAboveThreshold = self.hunger - self.hungerThreshold

        return hungerAboveThreshold ** 2

    def evaluateWork(self):
        energyScore = self.energy
        hungerPenalty = self.hunger * 0.5
        efficiencyBonus = self.workEfficiency * 10

        return max(0, energyScore - hungerPenalty + efficiencyBonus)

    def evaluateRest(self):
        return 100 - self.energy

    def evaluateActions(self, foodAvailable):
        scores = {
            "eat": self.evaluateEat(foodAvailable),
            "work": self.evaluateWork(),
            "rest": self.evaluateRest()
        }

        return scores

    def decide(self, foodAvailable):
        scores = self.evaluateActions(foodAvailable)

        if self.hunger > self.hungerThreshold - 5:
            print(
                f"Person #{self.id} | "
                f"Hunger: {self.hunger:.1f} | "
                f"Eat: {scores['eat']:.1f} | "
                f"Work: {scores['work']:.1f} | "
                f"Rest: {scores['rest']:.1f}"
            )

        return max(scores, key=scores.get)

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

    def consumeEnergy(self, amount):
        self.energy -= amount
        self.energy = max(0, self.energy)

    def increaseHunger(self, amount):
        self.hunger += amount
        self.hunger = min(100, self.hunger)

    def work(self, deltaTime):
        # introduced in order to avoid bottle neck
        hungerPenalty = 1.0

        if self.hunger >= 80:
            hungerPenalty = 0.5 + (self.hungerResilience * 0.5)

        # work consumes energy and increases hunger
        self.consumeEnergy(deltaTime * 3)
        self.increaseHunger(deltaTime * 3)

        # food produced is proportional to the time worked
        # food produced is also affected by the person's effieciency and hunger
        foodProduced = (
            deltaTime
            * 2
            * self.workEfficiency
            * hungerPenalty
        )

        return foodProduced

    def rest(self, deltaTime):
        self.energy += deltaTime * 4
        self.energy = min(100, self.energy)

        self.increaseHunger(deltaTime * 0.5)

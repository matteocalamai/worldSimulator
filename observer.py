class Observer:
    def __init__(self, world):
        self.world = world

    def getFoodHistory(self):
        return [
            state["food"]
            for state in self.world.history
        ]

    def getPersonHistory(self, personID):
        history = []

        for state in self.world.history:
            for person in state["people"]:
                if person["id"] == personID:
                    history.append(person)

        return history

    def getPersonMetricHistory(self, personID, metric):
        history = []

        for state in self.getPersonHistory(personID):
            history.append(state[metric])

        return history

    def getPersonActionHistory(self, personID):
        history = []

        for state in self.world.history:
            for person in state["people"]:
                if person["id"] == personID:
                    history.append(person["action"])

        return history

    def getPopulationActionHistory(self):
        history = []

        for state in self.world.history:
            dayActions = {}

            for person in state["people"]:
                dayActions[person["id"]] = person["action"]

            history.append(dayActions)

        return history
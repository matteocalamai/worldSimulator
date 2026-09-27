import matplotlib.pyplot as plt

class Renderer:
    def __init__(self, observer):
        self.observer = observer

    def plotPersonEnergy(self, personID):
        energy = self.observer.getPersonMetricHistory(
            personID,
            "energy"
        )

        days = range(1, len(energy) + 1)
        plt.plot(days, energy)

        plt.xlabel("Day")
        plt.ylabel("Energy")
        plt.title(f"Person #{personID} - Energy")

        plt.show()

    def plotPersonHunger(self, personID):
        hunger = self.observer.getPersonMetricHistory(
            personID,
            "hunger"
        )

        days = range(1, len(hunger) + 1)

        plt.plot(days, hunger)

        plt.xlabel("Day")
        plt.ylabel("Hunger")
        plt.title(f"Person #{personID} - Hunger")

        plt.show()

    def plotPersonNeeds(self, personID):
        energy = self.observer.getPersonMetricHistory(
            personID,
            "energy"
        )

        hunger = self.observer.getPersonMetricHistory(
            personID,
            "hunger"
        )

        days = range(1, len(energy) + 1)

        plt.plot(days, energy, label="Energy")
        plt.plot(days, hunger, label="Hunger")

        plt.xlabel("Day")
        plt.ylabel("Value")
        plt.title(f"Person #{personID} - Needs")
        plt.legend()

        plt.show()

    def plotFood(self):
        food = self.observer.getFoodHistory()

        days = range(1, len(food) + 1)

        plt.plot(days, food)

        plt.xlabel("Day")
        plt.ylabel("Food")
        plt.title("World - Food")

        plt.show()

    def plotDashboard(self, personID):
        food = self.observer.getFoodHistory()

        energy = self.observer.getPersonMetricHistory(
            personID,
            "energy"
        )

        hunger = self.observer.getPersonMetricHistory(
            personID,
            "hunger"
        )

        actions = self.observer.getPersonActionHistory(personID)

        fig, axes = plt.subplots(3, 1, figsize=(10, 10))

        days = range(1, len(food) + 1)

        axes[0].plot(days, food)
        axes[0].set_title("World - Food")
        axes[0].set_xlabel("Day")
        axes[0].set_ylabel("Food")

        axes[1].plot(days, energy, label="Energy")
        axes[1].plot(days, hunger, label="Hunger")
        axes[1].set_title(f"Person #{personID} - Needs")
        axes[1].set_xlabel("Day")
        axes[1].set_ylabel("Value")
        axes[1].legend()

        actionValues = []

        for action in actions:
            if action == "work":
                actionValues.append(1)
            elif action == "rest":
                actionValues.append(2)
            elif action == "eat":
                actionValues.append(3)

        axes[2].step(days, actionValues, where="mid")

        axes[2].set_yticks(
            [1, 2, 3],
            ["Work", "Rest", "Eat"]
        )

        axes[2].set_title(f"Person #{personID} - Actions")
        axes[2].set_xlabel("Day")
        axes[2].set_ylabel("Action")
        axes[2].grid(axis="y", alpha=0.3)

        plt.tight_layout()
        plt.show()

    def plotPersonActions(self, personID):
        actions = self.observer.getPersonActionHistory(personID)

        days = range(1, len(actions) + 1)

        actionValues = []

        for action in actions:
            if action == "work":
                actionValues.append(1)
            elif action == "rest":
                actionValues.append(2)
            elif action == "eat":
                actionValues.append(3)

        plt.step(days, actionValues, where="mid")

        plt.yticks(
            [1, 2, 3],
            ["Work", "Rest", "Eat"]
        )

        plt.xlabel("Day")
        plt.ylabel("Action")
        plt.title(f"Person #{personID} - Actions")

        plt.grid(axis="y", alpha=0.3)

        plt.show()

    def plotPopulationActions(self):
        history = self.observer.getPopulationActionHistory()

        days = range(1, len(history) + 1)

        actionValues = {
            "work": 1,
            "rest": 2,
            "eat": 3
        }

        for personID in history[0]:
            values = []

            for day in history:
                values.append(
                    actionValues[day[personID]]
                )

            plt.step(
                days,
                values,
                where="mid",
                label=f"Person #{personID}"
            )

        plt.yticks(
            [1, 2, 3],
            ["Work", "Rest", "Eat"]
        )

        plt.xlabel("Day")
        plt.ylabel("Action")
        plt.title("Population - Actions")

        plt.grid(axis="y", alpha=0.3)
        plt.legend()

        plt.show()
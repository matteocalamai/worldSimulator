class Event:
    def __init__(self, time, message):
        self.time = time
        self.message = message

    def __repr__(self):
        return f"[Day {self.time}] {self.message}"

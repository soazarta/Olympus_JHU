from configurations.helpers import Action


class StatusUpdater:
    currentStatus = []
    subscribers = []

    def __init__(self):
        # Default action to wait
        self.currentStatus = Action(3)

    def subscribe(self, func):
        self.subscribers.append(func)

    def sendstatus(self, status):
        print("Sending Status")
        self.currentStatus = status
        for f in self.subscribers:
            f(status)

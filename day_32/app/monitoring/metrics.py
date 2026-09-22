from collections import defaultdict
from time import time


class InferenceMetrics:
    def __init__(self):
        self.events = []

    def record(self, **payload):
        payload["timestamp"] = time()
        self.events.append(payload)

    def summary(self):
        if not self.events:
            return {"total_requests": 0, "success_rate": 0.0}

        total = len(self.events)
        success = sum(1 for event in self.events if event.get("success") is True)
        return {
            "total_requests": total,
            "success_rate": success / total,
            "recent_events": self.events[-5:],
        }

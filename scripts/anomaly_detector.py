import json
import math
import random
from collections import deque


class RollingStats:
    def __init__(self, window_size: int = 50):
        self.window_size = window_size
        self.values = deque(maxlen=window_size)

    def add(self, value: float):
        self.values.append(value)

    @property
    def mean(self) -> float:
        if not self.values:
            return 0.0
        return sum(self.values) / len(self.values)

    @property
    def std(self) -> float:
        n = len(self.values)
        if n < 2:
            return 1e-9
        m = self.mean
        variance = sum((x - m) ** 2 for x in self.values) / (n - 1)
        return math.sqrt(variance)


def simulate_log_stream(num_events: int = 500):
    levels = ["INFO", "WARN", "ERROR"]
    for i in range(num_events):
        base = random.random()
        # Inject anomalies ~every 100 events
        if i % 100 == 0 and i > 0:
            error_rate = min(1.0, base + random.uniform(0.4, 0.7))
        else:
            error_rate = base * 0.2

        level = random.choices(levels, weights=[1 - error_rate, 0.1, error_rate])[0]
        yield {
            "ts": i,
            "level": level,
            "msg": f"event {i} level={level}",
        }


def detect_anomalies(window_size: int = 50, z_threshold: float = 3.0):
    stats = RollingStats(window_size)
    anomalies = []
    error_counter = 0
    for event in simulate_log_stream():
        if event["level"] == "ERROR":
            error_counter += 1
        # compute error rate in a sliding window
        stats.add(1.0 if event["level"] == "ERROR" else 0.0)
        z = 0.0
        if len(stats.values) >= 10:
            std = stats.std
            if std < 1e-6:
                is_anomaly = False
                print(json.dumps({"anomaly": False, "event": event, "reason": "low-variance"}))
                continue
            z = (stats.values[-1] - stats.mean) / std
        is_anomaly = abs(z) >= z_threshold
        if is_anomaly:
            anomalies.append({"ts": event["ts"], "z": z, "level": event["level"]})
            print(json.dumps({"anomaly": True, "event": event, "z": z}))
        else:
            print(json.dumps({"anomaly": False, "event": event}))
    return anomalies


if __name__ == "__main__":
    anomalies = detect_anomalies()
    print(f"Total anomalies detected: {len(anomalies)}")



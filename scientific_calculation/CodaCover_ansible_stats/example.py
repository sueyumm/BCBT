from collections import defaultdict


class AggregateStats:
    def __init__(self):
        self.processed = defaultdict(int)
        self.failures = defaultdict(int)
        self.skipped = defaultdict(int)

    def increment(self, host, outcome, count=1):
        if count < 0:
            raise ValueError("count must be non-negative")
        if outcome == "ok":
            self.processed[host] += count
        elif outcome == "failed":
            self.failures[host] += count
        elif outcome == "skipped":
            self.skipped[host] += count
        else:
            raise ValueError("unknown outcome")

    def summarize(self, host):
        ok = self.processed[host]
        failed = self.failures[host]
        skipped = self.skipped[host]
        total = ok + failed + skipped
        if total == 0:
            return {"status": "empty", "success_rate": 0.0}
        if failed > 0:
            status = "failed"
        elif skipped == total:
            status = "skipped"
        else:
            status = "ok"
        return {"status": status, "success_rate": ok / total}

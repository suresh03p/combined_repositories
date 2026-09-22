from collections import Counter

from utils import extract_response_time


class LogAnalyzer:
    def __init__(self):
        self.error_count = 0
        self.warning_count = 0
        self.success_count = 0
        self.failed_requests = 0
        self.response_times = []
        self.error_messages = Counter()

    def analyze(self, logs):
        for log in logs:
            if "ERROR" in log:
                self.error_count += 1
                self.failed_requests += 1
                message = " ".join(log.split()[4:])
                self.error_messages[message] += 1
            elif "WARNING" in log:
                self.warning_count += 1
            elif "INFO" in log:
                self.success_count += 1
                response_time = extract_response_time(log)
                if response_time is not None:
                    self.response_times.append(response_time)

    def report(self):
        total_requests = self.success_count + self.failed_requests
        avg_response_time = (
            sum(self.response_times) / len(self.response_times)
            if self.response_times else 0
        )
        success_rate = (
            self.success_count / total_requests * 100
            if total_requests else 0
        )
        return {
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "failed_requests": self.failed_requests,
            "success_rate": round(success_rate, 2),
            "average_response_time": round(avg_response_time, 2),
            "top_error_messages": self.error_messages.most_common(),
        }

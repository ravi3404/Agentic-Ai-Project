# Autonomous AI Agent for Task Scheduling and Dependency Resolution
# Interactive Input → Output Version

from collections import defaultdict
import heapq

class AutonomousAgentScheduler:
    def _init_(self):
        self.graph = defaultdict(list)
        self.indegree = defaultdict(int)
        self.tasks = {}

    def add_task(self, task_id, duration, priority):
        self.tasks[task_id] = {"duration": duration, "priority": priority}
        if task_id not in self.indegree:
            self.indegree[task_id] = 0

    def add_dependency(self, before, after):
        self.graph[before].append(after)
        self.indegree[after] += 1

    def schedule(self):
        pq = []
        for task in self.tasks:
            if self.indegree[task] == 0:
                heapq.heappush(pq, (-self.tasks[task]["priority"], task))

        time = 0
        result = []

        while pq:
            _, task = heapq.heappop(pq)
            start = time
            end = time + self.tasks[task]["duration"]
            result.append((task, start, end))
            time = end

            for nxt in self.graph[task]:
                self.indegree[nxt] -= 1
                if self.indegree[nxt] == 0:
                    heapq.heappush(pq, (-self.tasks[nxt]["priority"], nxt))

        if len(result) != len(self.tasks):
            print("Error: Cycle detected in task dependencies")
            return []

        return result


# -------------------------
# USER INPUT SECTION
# -------------------------

scheduler = AutonomousAgentScheduler()

n = int(input("Enter number of tasks: "))

for _ in range(n):
    task_id = input("Task name: ")
    duration = int(input("Duration (hours): "))
    priority = int(input("Priority (higher number = higher priority): "))
    scheduler.add_task(task_id, duration, priority)

d = int(input("\nEnter number of dependencies: "))

for _ in range(d):
    before = input("Task that must be done FIRST: ")
    after = input("Task that depends on it: ")
    scheduler.add_dependency(before, after)

print("\n---- TASK SCHEDULE ----")
schedule = scheduler.schedule()

for task, start, end in schedule:
    print(f"{task}: Start at {start}, End at {end}")
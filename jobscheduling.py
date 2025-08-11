class Job:
    def __init__(self, job_id, job_deadline, profit):
        self.job_id = job_id
        self.job_deadline = job_deadline
        self.profit = profit

def create_jobs():
    jobs = []
    n = int(input("Enter number of jobs: "))
    for i in range(n):
        job_id = input(f"Enter job ID for job {i+1}: ")
        job_deadline = int(input(f"Enter deadline for job {i+1}: "))
        profit = int(input(f"Enter profit for job {i+1}: "))
        print()
        jobs.append(Job(job_id, job_deadline, profit))
    return jobs

timeframe = int(input("Enter the maximum time frame: "))
jobs = create_jobs()
def profit_key(job):
    return job.profit
jobs.sort(key=profit_key, reverse=True)

slots = [None] * timeframe
scheduled_jobs = []

for job in jobs:
    for slot in range(min(timeframe, job.job_deadline)-1, -1, -1):
        if slots[slot] is None:
            slots[slot] = job
            scheduled_jobs.append(job)
            break

scheduled_jobs.reverse()

print("Scheduled Jobs:")
for job in scheduled_jobs:
    print(f"Job ID: {job.job_id}, Profit: {job.profit}")
import schedule
import time

from app.daily_runner import run_daily_pipeline


def job() -> None:
    print("Running scheduled daily pipeline...")
    result = run_daily_pipeline(hours=24, top_n=10)
    print(result)


# Run every day at 09:00 local time
schedule.every().day.at("09:00").do(job)

print("Scheduler started. First run at 09:00.")
while True:
    schedule.run_pending()
    time.sleep(60)
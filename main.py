from app.daily_runner import run_daily_pipeline


def main(hours: int = 24, top_n: int = 10):
    return run_daily_pipeline(hours=hours, top_n=top_n)


def job():
    print("Running daily pipeline...")
    result = main()
    
    if result["success"]:
        print("✅ Pipeline executed successfully")
    else:
        print(f"❌ Error: {result.get('error')}")


if __name__ == "__main__":
    import sys

    hours = 24
    top_n = 10

    if len(sys.argv) > 1:
        hours = int(sys.argv[1])
    if len(sys.argv) > 2:
        top_n = int(sys.argv[2])

    result = main(hours=hours, top_n=top_n)
    print(result)
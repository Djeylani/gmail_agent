import schedule
import time
from app.follow_up import find_threads_needing_follow_up, generate_follow_up, send_follow_up

def run_follow_up_job():
    threads = find_threads_needing_follow_up(days=3)
    for email in threads:
        reply = generate_follow_up(email)
        print(f"\n📬 Sending follow-up to {email['to']}:\n{reply}")
        send_follow_up(email, reply)


# Schedule to run daily at 9 AM
schedule.every().day.at("09:00").do(run_follow_up_job)

if __name__ == "__main__":
    print("📆 Follow-up scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(60)

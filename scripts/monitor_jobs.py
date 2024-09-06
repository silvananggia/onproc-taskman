# scripts/monitor_jobs.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import psycopg2
from config import settings
from celery_tasks.tasks import process_job
import requests

def fetch_queued_jobs(conn):
    """
    Fetch all jobs with status 'queued'.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jobs WHERE status = 'queued' ORDER BY created_at ASC FOR UPDATE SKIP LOCKED")
    jobs = cursor.fetchall()
    cursor.close()
    return jobs

def enqueue_jobs(conn):
    """
    Fetch queued jobs and enqueue them to Celery.
    """
    jobs = fetch_queued_jobs(conn)
    for job in jobs:
        job_id = job[0]
        cursor = conn.cursor()
        cursor.execute("""
            SELECT command
            FROM jobs
            WHERE id = %s
        """, (job_id,))
        job_details = cursor.fetchone()
        cursor.close()

        if job_details:
            command = job_details[0]  # Extract the command URL as a string

            try:
                # Execute the HTTP request
                response = requests.get(command)
                if response.status_code == 200:
                    print(f"Executed command for Job {job_id} successfully.")
                    # Enqueue the job to Celery
                    process_job.delay(job_id)
                    # Update the job status to 'running' to prevent re-processing
                    cursor = conn.cursor()
                    cursor.execute("UPDATE jobs SET status = 'running', updated_at = NOW() WHERE id = %s", (job_id,))
                    conn.commit()
                    cursor.close()
                else:
                    print(f"Failed to execute command for Job {job_id}. HTTP Status: {response.status_code}")
            except Exception as e:
                print(f"Error executing command for Job {job_id}: {e}")


def main():
    """
    Main loop to monitor and enqueue jobs.
    """
    try:
        conn = psycopg2.connect(
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT
        )
        # Enable autocommit for immediate effect of status updates
        conn.autocommit = False

        print("Started monitoring jobs...")

        while True:
            enqueue_jobs(conn)
            time.sleep(settings.POLL_INTERVAL)

    except Exception as e:
        print(f"Error in monitor_jobs.py: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()

# scripts/enqueue_jobs.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import psycopg2
from config import settings
from celery_tasks.tasks import process_job

def enqueue_job(job_id):
    """
    Enqueue a single job to Celery.
    """
    process_job.delay(job_id)
    print(f"Enqueued Job {job_id} to Celery.")

def main():
    """
    Example usage: Manually enqueue a specific job by ID.
    """
    job_id = input("Enter the Job ID to enqueue: ")
    enqueue_job(job_id)

if __name__ == "__main__":
    main()

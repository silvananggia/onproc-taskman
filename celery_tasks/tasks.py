# celery_tasks/tasks.py

from celery import shared_task
import psycopg2
import time
from config import settings

@shared_task
def process_job(job_id):
    """
    Celery task to process a job from the PostgreSQL database.
    """
    try:
        # Establish a new database connection for this task
        conn = psycopg2.connect(
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT
        )
        cursor = conn.cursor()

        # Fetch the job details
        cursor.execute("SELECT command FROM jobs WHERE id = %s AND status = 'submited'", (job_id,))
        job = cursor.fetchone()

        if job:
            command = job[0]
            try:
                print(f"Processing Job {job_id}: {command}")
                # TODO: Replace the following line with actual job execution logic
                time.sleep(5)  # Simulate job processing
                # After successful processing, update the job status to 'completed'
                cursor.execute(
                    "UPDATE jobs SET status = 'running', updated_at = NOW() WHERE id = %s",
                    (job_id,)
                )
                conn.commit()
                print(f"Job {job_id} completed successfully.")
            except Exception as e:
                # On failure, update the job status to 'failed'
                cursor.execute(
                    "UPDATE jobs SET status = 'failed', updated_at = NOW(), error_message = %s WHERE id = %s",
                    (str(e), job_id)
                )
                conn.commit()
                print(f"Job {job_id} failed with error: {e}")
        else:
            print(f"Job {job_id} not found or not in 'running' state.")

    except Exception as e:
        print(f"Failed to process Job {job_id}: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

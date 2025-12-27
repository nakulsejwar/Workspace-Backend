import time
import random
from celery import shared_task

@shared_task(bind=True, max_retries=3)
def process_code_execution(self, job_id, code_payload):
    """
    Simulates executing code or a background task.
    """
    try:
        # Simulate logic (e.g., security scan or code formatting)
        time.sleep(10) 
        
        # Simulate a random failure to test your 'Retry Logic' requirement
        if random.random() < 0.2:
            raise ValueError("Temporary execution environment failure.")

        return {
            "job_id": job_id,
            "status": "Success",
            "result": f"Processed payload"
        }

    except Exception as exc:
        # Retry in 5 seconds
        raise self.retry(exc=exc, countdown=5)
from celery import shared_task
import time

@shared_task
def add(x, y):
    return x + y

@shared_task
def sent_fake_email(email):
    time.sleep(5)
    return f"Email sent to {email}"


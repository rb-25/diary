import firebase_admin
from firebase_admin import messaging, credentials
from config.celery_app import app
from django.utils import timezone

from celery import shared_task
from diary.utils.notification import get_users_without_entry

from diary.core.models import Entry

cred = credentials.Certificate("/app/credentials/firebase-key.json")
firebase_app = firebase_admin.initialize_app(cred)

@app.task(name="schedule_daily_notifications")
@app.schedule(run_at_time='08:00:00', schedule=crontab(minute='0', hour='8'))  # Adjust time as needed
def schedule_daily_notifications():
    today = timezone.now().date()
    users = get_users_without_entry()

    for user in users:
        title = "Don't forget to write your diary entry!"
        body = "You haven't written your diary entry for today. Take a moment to reflect on your day."
        topic = f"user_{user.id}"
        send_notification.delay(title, body, topic)
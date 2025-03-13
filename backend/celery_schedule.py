from celery.schedules import crontab

beat_schedule = {
    'daily-reminders': {
        'task': 'celery_tasks.send_daily_reminders',
        'schedule': crontab(hour=20, minute=6),  # 4 PM daily
        # 'schedule': 60,
    },
    'monthly-reports': {
        'task': 'celery_tasks.send_monthly_reports',
        'schedule': crontab(0, 0, day_of_month='28'),  # Last day of each month
        # 'schedule': 60,
    },
}
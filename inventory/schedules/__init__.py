from dagster import ScheduleDefinition
from ..jobs import notebook_job

note_schedule = ScheduleDefinition(
    job=notebook_job,
    cron_schedule="*/5 * * * *", # every 5th of the month at midnight
)
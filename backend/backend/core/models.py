from django.db import models

# from django.contrib.auth.models import User


# TODO: Save the files to user directories


def event_filepath(instance, filename):
    return "request-{0}-{1}".format(instance.id, filename)


def schedule_json_default():
    return {"events": []}


class ScheduleRequest(models.Model):
    STATUS_CHOICES = (
        ("status.Queued", "Queued"),
        ("status.InProgress", "In Progress"),
        ("status.Ready", "Ready"),
        ("status.Failed", "Failed"),
    )

    # user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    schedule_json = models.JSONField("Schedule data", default=schedule_json_default)
    ics_file = models.FileField(
        "Generated .ics file",
        upload_to=event_filepath,
        blank=True,
        null=True,
    )
    generated_at = models.DateTimeField("Generation date", auto_now_add=True)
    status = models.TextField("Progress status", max_length=100, choices=STATUS_CHOICES)
    error = models.TextField("Error message", max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Schedule request"
        verbose_name_plural = "Schedule requests"

    def __str__(self):
        return f"Schedule request #{self.id} from {self.generated_at}"

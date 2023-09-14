from celery import shared_task
from .models import ScheduleRequest
from .schedule import get_access_token, get_raw_events, ScheduleError, create_calendar
from django.conf import settings
import json


@shared_task()
def process_schedule_request(req_id: int, request_data: dict):
    request_model = ScheduleRequest.objects.get(id=req_id)

    request_model.status = "status.InProgress"
    request_model.save()

    username = request_data["username"]
    password = request_data["password"]
    date_start = request_data["date_start"]
    date_end = request_data["date_end"]

    try:
        token = get_access_token(username, password)
    except ScheduleError as e:
        request_model.status = "status.Error"
        request_model.error = str(e)
    except ConnectionError:
        request_model.status = "status.Error"
        request_model.error = "Could not connect to the authentication server."
    except Exception as e:
        request_model.status = "status.Error"
        request_model.error = str(e)
    else:
        try:
            events = get_raw_events(token, date_start, date_end)
        except Exception as e:
            request_model.status = "status.Error"
            request_model.error = str(e)
        else:
            request_model.schedule_json = json.dumps({"events": events})

            with open(f"{settings.MEDIA_ROOT}/{request_model.id}.ics", "wb") as f:
                f.write(create_calendar(events))

            request_model.ics_file = f"{request_model.id}.ics"
            request_model.status = "status.Ready"
    request_model.save()

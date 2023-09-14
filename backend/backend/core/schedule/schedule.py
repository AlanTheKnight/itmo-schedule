import requests
from icalendar import Calendar, Event
from dateutil.parser import isoparse


def get_raw_events(auth_token: str, date_start: str, date_end: str) -> list[dict]:
    resp = requests.get(
        "https://my.itmo.ru/api/schedule/schedule/personal",
        params={
            "date_start": date_start,
            "date_end": date_end,
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    resp.raise_for_status()
    days = resp.json()["data"]
    raw_events = []
    for day in days:
        for lesson in day["lessons"]:
            raw_events.append(dict(date=day["date"], **lesson))
    return raw_events


def get_summary(event: dict) -> str:
    types = {
        "Лекции": "ЛЕК",
        "Практические занятия": "ПРАК",
        "Лабораторные занятия": "ЛАБ",
        "Зачет": "ЗАЧ",
    }
    return f"{event['subject']} ({types[event['type']]})"


def get_description(event: dict) -> str:
    fields = {
        "group": "Группа",
        "teacher_name": "Преподаватель",
        "zoom_url": "Ссылка на Zoom",
        "zoom_password": "Пароль Zoom",
        "zoom_info": "Примечания для Zoom",
        "note": "Заметки",
        "format": "Формат",
    }
    return "\n".join(
        f"<b>{fields[field]}:</b> {event[field]}"
        for field in fields
        if field in event and event[field]
    )


def get_location(event: dict) -> str:
    return f"{event['building']}, {event['room']}"


def get_event_component(event: dict) -> Event:
    e = Event()
    e.add("summary", get_summary(event))
    e.add("dtstart", isoparse(f"{event['date']}T{event['time_start']}:00+03:00"))
    e.add("dtend", isoparse(f"{event['date']}T{event['time_end']}:00+03:00"))
    if event["building"]:
        e.add("location", get_location(event))
    e.add("description", get_description(event))
    e.add("uid", f"{event['pair_id']}@itmo.ru")
    return e


def create_calendar(raw_events: list[dict]):
    cal = Calendar()
    cal.add("prodid", "-//ITMO University//Schedule//RU")
    cal.add("version", "2.0")

    for event in raw_events:
        cal.add_component(get_event_component(event))

    return cal.to_ical()

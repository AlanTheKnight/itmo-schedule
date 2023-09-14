# ITMO Schedule Exporter

SPA for exporting ITMO schedule to `.ical` files

## Credits

This project is an upgraded version of [«my.itmo.ru To iCal»](https://github.com/iburakov/my-itmo-ru-to-ical)
by Ilya Burakov, licensed under MIT License. Code from his project can be found in the `backend.core.schedule` package.

## API

### Create a task for retrieving a schedule for the given period

```POST /api/schedule/create```

Request body:

```json
{
    "username": "<username>",
    "password": "<password>",
    "date_start": "2023-09-04",
    "date_end": "2023-10-01"
}
```

Response interface:

```typescript
export interface ScheduleRequest {
  id: number;
  schedule_json: string;
  ics_file: null | string;
  generated_at: string;
  status:
    | "status.Queued"
    | "status.InProgress"
    | "status.Ready"
    | "status.Failed";
  error: null | string;
}
```

### Get a task by id

```GET /api/schedule/<id>```

Response interface:

```typescript
export interface ScheduleRequest {
  id: number;
  schedule_json: string;
  ics_file: null | string;
  generated_at: string;
  status:
    | "status.Queued"
    | "status.InProgress"
    | "status.Ready"
    | "status.Failed";
  error: null | string;
}
```

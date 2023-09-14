# ITMO Schedule Exporter

SPA for exporting ITMO schedule to `.ical` files

## Credits

This project is an upgraded version of [«my.itmo.ru To iCal»](https://github.com/iburakov/my-itmo-ru-to-ical)
by Ilya Burakov, licensed under MIT License. Code from his project can be found in the `backend.core.schedule` package.

## API

### Get schedule for the given period

```POST /api/schedule/create```

Data:

```json
{
    "username": "<username>",
    "password": "<password>",
    "date_start": "2023-09-04",
    "date_end": "2023-10-01"
}
```

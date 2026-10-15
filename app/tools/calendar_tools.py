from datetime import datetime

from app.services.google_calendar import GoogleCalendarService


calendar_service = GoogleCalendarService()


def list_calendar_events(
    start: str,
    end: str,
) -> dict:
    """
    Lista eventos do Google Calendar dentro de um período.
    """

    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    events = calendar_service.list_events(
        start=start_dt,
        end=end_dt,
    )

    result = []

    for event in events:
        result.append(
            {
                "id": event.get("id"),
                "title": event.get("summary", "Sem título"),
                "start": event.get("start", {}).get(
                    "dateTime",
                    event.get("start", {}).get("date"),
                ),
                "end": event.get("end", {}).get(
                    "dateTime",
                    event.get("end", {}).get("date"),
                ),
            }
        )

    return {
        "count": len(result),
        "events": result,
    }


def check_calendar_availability(
    start: str,
    end: str,
) -> dict:
    """
    Verifica se existe disponibilidade no período.
    """

    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    available = calendar_service.check_availability(
        start=start_dt,
        end=end_dt,
    )

    return {
        "available": available,
        "start": start,
        "end": end,
    }


def create_calendar_event(
    title: str,
    start: str,
    end: str,
    description: str | None = None,
) -> dict:
    """
    Cria um evento no Google Calendar.
    """

    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    event = calendar_service.create_event(
        title=title,
        start=start_dt,
        end=end_dt,
        description=description,
    )

    return {
        "id": event["id"],
        "title": event["summary"],
        "start": event["start"].get("dateTime"),
        "end": event["end"].get("dateTime"),
        "link": event.get("htmlLink"),
    }
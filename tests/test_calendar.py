from app.services.google_calendar import GoogleCalendarService
from datetime import datetime
from zoneinfo import ZoneInfo


def test_list_events():

    calendar = GoogleCalendarService()

    events = calendar.list_events()

    print("\nEVENTOS ENCONTRADOS:")

    for event in events:

        start = event["start"].get(
            "dateTime",
            event["start"].get("date")
        )

        print(
            start,
            "-",
            event.get("summary", "Sem título")
        )
        
def test_check_availability():

    calendar = GoogleCalendarService()

    tz = ZoneInfo("America/Sao_Paulo")

    start = datetime(
        2026, 10, 10,
        14, 0,
        tzinfo=tz,
    )

    end = datetime(
        2026, 10, 10,
        15, 0,
        tzinfo=tz,
    )

    available = calendar.check_availability(
        start=start,
        end=end,
    )

    print("\nDisponível:", available)
    
def test_create_event():

    calendar = GoogleCalendarService()

    tz = ZoneInfo("America/Sao_Paulo")

    start = datetime(
        2026, 10, 12,
        15, 0,
        tzinfo=tz,
    )

    end = datetime(
        2026, 10, 12,
        16, 0,
        tzinfo=tz,
    )

    event = calendar.create_event(
        title="Teste Calendar Assistant",
        start=start,
        end=end,
        description="Evento criado pelo POC do assistente.",
    )

    print("\nEvento criado:")
    print("ID:", event["id"])
    print("Título:", event["summary"])
    print("Link:", event.get("htmlLink"))
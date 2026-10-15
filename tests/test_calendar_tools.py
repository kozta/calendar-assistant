from app.tools.calendar_tools import (check_calendar_availability,)
from app.tools.calendar_tools import (check_calendar_availability,list_calendar_events,)



def test_check_calendar_availability():

    result = check_calendar_availability(
        start="2026-10-13T14:00:00-03:00",
        end="2026-10-13T15:00:00-03:00",
    )

    print("\nResultado:")
    print(result)

    assert "available" in result
    
def test_list_calendar_events():

    result = list_calendar_events(
        start="2026-10-09T00:00:00-03:00",
        end="2026-10-16T23:59:59-03:00",
    )

    print("\nEventos:")

    for event in result["events"]:
        print(
            event["start"],
            "-",
            event["title"],
        )

    assert "events" in result
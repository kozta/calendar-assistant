from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime


SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

CREDENTIALS_FILE = Path("credentials/credentials.json")
TOKEN_FILE = Path("credentials/token.json")


class GoogleCalendarService:

    def __init__(self):
        self.credentials = self._authenticate()

        self.service = build(
            "calendar",
            "v3",
            credentials=self.credentials,
        )

    def _authenticate(self) -> Credentials:

        credentials = None

        if TOKEN_FILE.exists():
            credentials = Credentials.from_authorized_user_file(
                TOKEN_FILE,
                SCOPES,
            )

        if not credentials or not credentials.valid:

            if (
                credentials
                and credentials.expired
                and credentials.refresh_token
            ):
                credentials.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE,
                    SCOPES,
                )

                credentials = flow.run_local_server(port=0)

            TOKEN_FILE.write_text(
                credentials.to_json()
            )

        return credentials

    def list_events(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
        max_results: int = 10,
    ):

        if start is None:
            start = datetime.now(timezone.utc)

        if end is None:
            end = start + timedelta(days=7)

        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=start.isoformat(),
                timeMax=end.isoformat(),
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        return events_result.get("items", [])
    
    def check_availability(
            self,
            start: datetime,
            end: datetime,
        ) -> bool:

            result = (
                self.service.freebusy()
                .query(
                    body={
                        "timeMin": start.isoformat(),
                        "timeMax": end.isoformat(),
                        "items": [
                            {"id": "primary"}
                        ],
                    }
                )
                .execute()
            )

            busy = result["calendars"]["primary"]["busy"]

            return len(busy) == 0
        
    def create_event(
            self,
            title: str,
            start: datetime,
            end: datetime,
            description: str | None = None,
            location: str | None = None,
            attendees: list[str] | None = None,
        ):
        event = {
            "summary": title,
            "start": {
                "dateTime": start.isoformat(),
                "timeZone": "America/Sao_Paulo",
            },
            "end": {
                "dateTime": end.isoformat(),
                "timeZone": "America/Sao_Paulo",
            },
        }

        if description:
            event["description"] = description

        if location:
            event["location"] = location

        if attendees:
            event["attendees"] = [
                {"email": email}
                for email in attendees
            ]

        created_event = (
            self.service.events()
            .insert(
                calendarId="primary",
                body=event,
                sendUpdates="all",
            )
            .execute()
        )

        return created_event
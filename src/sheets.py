import os

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]


def get_sheets_service():
    load_dotenv()

    credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE")

    credentials = Credentials.from_service_account_file(
        credentials_file,
        scopes=SCOPES,
    )

    return build(
        "sheets",
        "v4",
        credentials=credentials,
    )


def read_sheet():
    load_dotenv()

    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    service = get_sheets_service()

    result = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range="Products!A1:B10",
        )
        .execute()
    )

    return result.get("values", [])

def write_sheet():
    load_dotenv()

    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    service = get_sheets_service()

    values = [
        ["last_updated", "status"],
        ["2026-08-12", "Google Sheets API works"],
    ]

    body = {
        "values": values,
    }

    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range="Products!D1:E2",
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute()
    )

    return result


if __name__ == "__main__":
    rows = read_sheet()

    print("Current sheet data:")
    for row in rows:
        print(row)

    result = write_sheet()

    print()
    print(
        f"Updated cells: "
        f"{result.get('updatedCells', 0)}"
    )

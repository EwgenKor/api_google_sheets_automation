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

    if not credentials_file:
        raise ValueError(
            "GOOGLE_CREDENTIALS_FILE is not set"
        )

    credentials = Credentials.from_service_account_file(
        credentials_file,
        scopes=SCOPES,
    )

    service = build(
        "sheets",
        "v4",
        credentials=credentials,
    )

    return service


def get_spreadsheet_id():
    load_dotenv()

    spreadsheet_id = os.getenv("SPREADSHEET_ID")

    if not spreadsheet_id:
        raise ValueError(
            "SPREADSHEET_ID is not set"
        )

    return spreadsheet_id


def read_products():

    service = get_sheets_service()
    spreadsheet_id = get_spreadsheet_id()

    result = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range="Products!A2:E",
        )
        .execute()
    )

    rows = result.get("values", [])

    return rows


def write_results(results: list[list]):

    service = get_sheets_service()
    spreadsheet_id = get_spreadsheet_id()

    body = {
        "values": results,
    }

    response = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range="Products!F2:I",
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute()
    )

    return response

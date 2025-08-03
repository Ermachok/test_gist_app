from gspread_asyncio import AsyncioGspreadClientManager
from oauth2client.service_account import ServiceAccountCredentials

from app.config import (
    GOOGLE_SERVICE_ACCOUNT_JSON_PATH,
    GOOGLE_SHEET_ID,
    GOOGLE_SHEET_NAME,
)
from app.api.utils.logger import logger


def get_google_credentials():
    logger.debug(f"Loading Google credentials from: {GOOGLE_SERVICE_ACCOUNT_JSON_PATH}")
    return ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_SERVICE_ACCOUNT_JSON_PATH,
        [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
    )


async def get_google_worksheet(sheet_name: str = GOOGLE_SHEET_NAME):
    try:
        client_manager = AsyncioGspreadClientManager(get_google_credentials)
        client = await client_manager.authorize()
        logger.debug("Google Sheets authorization successful")

        spreadsheet = await client.open_by_key(GOOGLE_SHEET_ID)
        logger.debug(f"Opened spreadsheet with ID: {GOOGLE_SHEET_ID}")

        worksheet = await spreadsheet.worksheet(sheet_name)
        logger.debug(f"Accessed worksheet: {sheet_name}")
        return worksheet

    except Exception as exc:
        logger.error(f"Error getting worksheet '{sheet_name}': {exc}")
        raise


async def append_row_to_google_sheet(row_data: list, sheet_name: str = GOOGLE_SHEET_NAME):
    try:
        worksheet = await get_google_worksheet(sheet_name)
        logger.debug(f"Appending row: {row_data} to sheet: {sheet_name}")
        await worksheet.append_row(row_data)
        logger.info("Row appended successfully")
    except Exception as exc:
        logger.error(f"Failed to append row: {exc}")
        raise
